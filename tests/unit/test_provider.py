import json

import httpx
import pytest

from semidebug.config import Settings
from semidebug.llm.base import ProviderError
from semidebug.llm.provider import OpenAICompatibleProvider
from semidebug.models import PatchProposal

REQUEST = {"system": "Return a JSON patch", "context": {"sources": {}}}
VALID = {"explanation": "x", "unified_diff": "diff\n", "expected_effect": "x", "risks": []}


def provider(handler):
    return OpenAICompatibleProvider(
        Settings(api_key="test-only", model="test-model"),
        httpx.Client(transport=httpx.MockTransport(handler)),
    )


def test_structured_and_usage():
    def handler(request):
        data = json.loads(request.content)
        assert data["response_format"]["json_schema"]["strict"] is True
        assert data["response_format"]["json_schema"]["schema"]["additionalProperties"] is False
        return httpx.Response(
            200,
            json={
                "choices": [{"finish_reason": "stop", "message": {"content": json.dumps(VALID)}}],
                "usage": {"prompt_tokens": 12, "completion_tokens": 9},
            },
        )

    p = provider(handler)
    assert p.generate_structured(REQUEST, PatchProposal).explanation == "x"
    assert (p.calls, p.input_tokens, p.output_tokens) == (1, 12, 9)


@pytest.mark.parametrize(
    "data",
    [
        [],
        {},
        {"choices": [{"finish_reason": "length", "message": {"content": json.dumps(VALID)}}]},
        {"choices": [{"finish_reason": "stop", "message": {"content": '{"unified_diff": 42}'}}]},
        {"choices": [{"finish_reason": "stop", "message": {"content": "not json"}}]},
    ],
)
def test_invalid_provider_output(data):
    p = provider(lambda request: httpx.Response(200, json=data))
    with pytest.raises(ProviderError):
        p.generate_structured(REQUEST, PatchProposal)


def test_retry_and_redaction():
    p = provider(lambda request: httpx.Response(503, text="secret-should-not-leak"))
    with pytest.raises(ProviderError, match="HTTP 503") as exc:
        p.generate_structured(REQUEST, PatchProposal)
    assert p.calls == 3
    assert "secret-should-not-leak" not in str(exc.value)


def test_credentials_required():
    with pytest.raises(ProviderError):
        OpenAICompatibleProvider(Settings())
