import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    reasoning_effort: str = "low"
    eda_runtime: str = "native"
    api_key: str = ""
    model: str = ""
    base_url: str = "https://api.openai.com/v1"
    json_mode: bool = False
    api_timeout: float = 180
    max_iterations: int = 3
    input_price: float | None = None
    cached_input_price: float | None = None
    output_price: float | None = None
    price_source: str | None = None

    @classmethod
    def from_env(cls):
        load_dotenv(dotenv_path=".env", override=False)

        def price(key):
            value = os.getenv(key)
            return float(value) if value else None

        result = cls(
            reasoning_effort=os.getenv("SEMIDEBUG_REASONING_EFFORT", "low"),
            eda_runtime=os.getenv("SEMIDEBUG_EDA_RUNTIME", "native"),
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("OPENAI_MODEL", ""),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            json_mode=os.getenv("SEMIDEBUG_JSON_MODE", "false").lower() == "true",
            api_timeout=float(os.getenv("SEMIDEBUG_API_TIMEOUT", "180")),
            max_iterations=int(os.getenv("SEMIDEBUG_MAX_ITERATIONS", "3")),
            input_price=price("SEMIDEBUG_INPUT_PRICE"),
            cached_input_price=price("SEMIDEBUG_CACHED_INPUT_PRICE"),
            output_price=price("SEMIDEBUG_OUTPUT_PRICE"),
            price_source=os.getenv("SEMIDEBUG_PRICE_SOURCE") or None,
        )
        if not 1 <= result.max_iterations <= 10 or not 0 < result.api_timeout <= 300:
            raise ValueError("Invalid iteration or API timeout limits")
        if result.eda_runtime not in {"native", "docker"}:
            raise ValueError("EDA runtime must be native or docker")
        if result.reasoning_effort not in {"low", "medium", "high", "xhigh", "max"}:
            raise ValueError("Unsupported reasoning effort")
        if any(
            price is not None and price < 0
            for price in [
                result.input_price,
                result.cached_input_price,
                result.output_price,
            ]
        ):
            raise ValueError("Token prices must be non-negative")
        return result
