import json
import time
from urllib.parse import urlparse

import httpx
from pydantic import ValidationError

from semidebug.config import Settings
from semidebug.llm.base import ProviderError, T


class OpenAICompatibleProvider:
    name = "live-openai-compatible"

    def __init__(self, settings: Settings, client: httpx.Client | None = None):
        if not settings.api_key or not settings.model:
            raise ProviderError("Set OPENAI_API_KEY and OPENAI_MODEL in .env for live execution")
        url = urlparse(settings.base_url)
        if url.scheme != "https" and not (
            url.scheme == "http" and url.hostname in {"localhost", "127.0.0.1"}
        ):
            raise ProviderError("API endpoint requires HTTPS (HTTP allowed only for localhost)")
        if url.username or url.password or url.query or url.fragment:
            raise ProviderError("API endpoint must not contain credentials, query or fragment")
        self.settings = settings
        self.model = settings.model
        self.client = client or httpx.Client(timeout=settings.api_timeout, follow_redirects=False)
        self.calls = self.input_tokens = self.output_tokens = 0

    def close(self):
        self.client.close()

    def generate_structured(self, request: dict, schema: type[T]) -> T:
        json_schema = schema.model_json_schema()
        response_format = (
            {"type": "json_object"}
            if self.settings.json_mode
            else {
                "type": "json_schema",
                "json_schema": {"name": schema.__name__, "strict": True, "schema": json_schema},
            }
        )
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": request["system"]
                    + "\nReturn JSON matching: "
                    + json.dumps(json_schema),
                },
                {"role": "user", "content": json.dumps(request["context"])},
            ],
            "response_format": response_format,
            "max_completion_tokens": 5000,
        }
        for retry in range(3):
            self.calls += 1
            try:
                response = self.client.post(
                    self.settings.base_url.rstrip("/") + "/chat/completions",
                    headers={"Authorization": "Bearer " + self.settings.api_key},
                    json=payload,
                )
            except httpx.TransportError as exc:
                if retry < 2:
                    time.sleep(0.25 * 2**retry)
                    continue
                raise ProviderError(f"API transport failure: {type(exc).__name__}") from None
            if response.status_code in {429, 500, 502, 503, 504} and retry < 2:
                time.sleep(0.25 * 2**retry)
                continue
            if response.is_error:
                # Do not serialize raw provider error bodies or headers (can include secrets).
                raise ProviderError(f"API HTTP {response.status_code}")
            if len(response.content) > 1_000_000:
                raise ProviderError("API response exceeds limit")
            try:
                data = response.json()
                usage = data.get("usage") or {}
                self.input_tokens += int(usage.get("prompt_tokens", 0))
                self.output_tokens += int(usage.get("completion_tokens", 0))
                choice = data["choices"][0]
                message = choice["message"]
                if message.get("refusal") or choice.get("finish_reason") != "stop":
                    raise ProviderError("Provider refused or returned incomplete output")
                return schema.model_validate_json(message["content"])
            except (AttributeError, KeyError, IndexError, TypeError, ValueError, ValidationError):
                raise ProviderError("Malformed API response or invalid structured output") from None
        raise ProviderError("API retries exhausted")
