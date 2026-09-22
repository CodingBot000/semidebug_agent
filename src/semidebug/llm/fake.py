"""Explicit scripted test double. Never reads gold, source files or case IDs."""

from semidebug.llm.base import ProviderError


class ScriptedProvider:
    name = "scripted-test-double"
    model = "not-an-ai-model"

    def __init__(self, responses: list[dict]):
        self.responses = iter(responses)
        self.calls = self.input_tokens = self.output_tokens = 0
        self.requests = []

    def generate_structured(self, request, schema):
        self.calls += 1
        self.requests.append(request)
        try:
            return schema.model_validate(next(self.responses))
        except (StopIteration, ValueError):
            raise ProviderError("Scripted response exhausted or invalid") from None
