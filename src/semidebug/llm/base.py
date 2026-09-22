from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ProviderError(RuntimeError):
    pass


class LLMProvider(Protocol):
    name: str
    model: str
    calls: int
    input_tokens: int
    output_tokens: int

    def generate_structured(self, request: dict, schema: type[T]) -> T: ...
