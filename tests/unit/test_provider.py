import json

import httpx
import pytest

from semidebug.config import Settings
from semidebug.llm.base import ProviderError
from semidebug.llm.provider import OpenAIAPIProvider
from semidebug.models import Analysis, PatchProposal

REQUEST = {"system": "Analyze RTL", "context": {"sources": {"rtl/a.v": "x"}}}
VALID = {
    "analysis": {
        "hypotheses": [
            {
                "summary": "Boundary error",
                "likely_files": ["rtl/a.v"],
                "likely_lines": [1],
                "reasoning": "Simulation assertion",
                "confidence": 0.9,
                "evidence_ids": ["baseline:simulation"],
            }
        ]
    },
    "patch": {
        "explanation": "Fix boundary",
        "unified_diff": "diff\n",
        "expected_effect": "Correct behavior",
        "risks": [],
    },
}


def provider(handler):
    return OpenAIAPIProvider(
        Settings(api_key="test-only", model="gpt-6-sol"),
        httpx.Client(transport=httpx.MockTransport(handler)),
    )


def test_combined_structured_output_and_usage():
    def handler(request):
        data = json.loads(request.content)
        assert data["model"] == "gpt-6-sol"
        assert data["reasoning_effort"] == "low"
        assert data["response_format"]["json_schema"]["name"] == "RepairSuggestion"
        assert data["response_format"]["json_schema"]["strict"] is True
        assert data["response_format"]["json_schema"]["schema"]["additionalProperties"] is False
        return httpx.Response(
            200,
            json={
                "choices": [{"finish_reason": "stop", "message": {"content": json.dumps(VALID)}}],
                "usage": {
                    "prompt_tokens": 12,
                    "completion_tokens": 9,
                    "prompt_tokens_details": {"cached_tokens": 4},
                },
            },
        )

    p = provider(handler)
    analysis = p.generate_structured(REQUEST, Analysis)
    context = {**REQUEST["context"], "hypothesis": analysis.hypotheses[0].model_dump()}
    patch = p.generate_structured({"system": "Patch", "context": context}, PatchProposal)
    assert patch.explanation == "Fix boundary"
    assert (p.calls, p.input_tokens, p.cached_input_tokens, p.output_tokens) == (1, 12, 4, 9)


@pytest.mark.parametrize(
    "data",
    [
        [],
        {},
        {"choices": [{"finish_reason": "length", "message": {"content": json.dumps(VALID)}}]},
        {"choices": [{"finish_reason": "stop", "message": {"content": "not json"}}]},
    ],
)
def test_invalid_provider_output(data):
    p = provider(lambda request: httpx.Response(200, json=data))
    with pytest.raises(ProviderError):
        p.generate_structured(REQUEST, Analysis)


def test_retry_and_redaction():
    p = provider(lambda request: httpx.Response(503, text="secret-should-not-leak"))
    with pytest.raises(ProviderError, match="HTTP 503") as exc:
        p.generate_structured(REQUEST, Analysis)
    assert p.calls == 3
    assert "secret-should-not-leak" not in str(exc.value)


def test_cached_patch_rejects_changed_context():
    p = provider(
        lambda request: httpx.Response(
            200,
            json={
                "choices": [{"finish_reason": "stop", "message": {"content": json.dumps(VALID)}}]
            },
        )
    )
    p.generate_structured(REQUEST, Analysis)
    with pytest.raises(ProviderError, match="context changed"):
        p.generate_structured({"system": "Patch", "context": {"different": True}}, PatchProposal)


def test_credentials_required():
    with pytest.raises(ProviderError):
        OpenAIAPIProvider(Settings())
