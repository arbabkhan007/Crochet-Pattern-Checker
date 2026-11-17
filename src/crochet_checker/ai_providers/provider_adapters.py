"""Environment-driven asynchronous adapters for hosted chat providers.

API credentials remain server-side and are deliberately omitted from public
status, reports, and provider error messages. Model identifiers are never
assumed: each selected provider must be configured explicitly.
"""

from __future__ import annotations

import asyncio
import math
import os
import time
from dataclasses import dataclass, field
from datetime import timezone
from email.utils import parsedate_to_datetime
from typing import Any, Mapping
from urllib.parse import quote, urlsplit

import httpx


@dataclass(frozen=True)
class ProviderConfig:
    provider_id: str
    family: str
    model: str
    base_url: str
    api_key: str | None = field(default=None, repr=False, compare=False)
    required: bool = True
    role: str | None = None
    timeout_seconds: float = 45.0
    max_retries: int = 2
    max_tokens: int = 1800
    temperature: float | None = None
    input_cost_per_million: float | None = None
    output_cost_per_million: float | None = None

    def __post_init__(self) -> None:
        if not self.provider_id.strip() or not self.model.strip():
            raise ValueError("provider_id and explicit model id are required")
        if self.family not in {"openai_compatible", "anthropic", "google"}:
            raise ValueError(f"Unsupported provider API family: {self.family}")
        parsed = urlsplit(self.base_url)
        if parsed.scheme not in {"https", "http"} or not parsed.netloc:
            raise ValueError("Provider endpoint must be an absolute HTTP(S) URL")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError(
                "Provider endpoint must not embed credentials, query, or fragment"
            )
        if self.api_key and parsed.scheme != "https":
            raise ValueError("API-key authenticated endpoints must use HTTPS")
        if (
            not math.isfinite(self.timeout_seconds)
            or not 0 < self.timeout_seconds <= 300
        ):
            raise ValueError("timeout_seconds must be between 0 and 300")
        if not 0 <= self.max_retries <= 5:
            raise ValueError("max_retries must be between 0 and 5")
        if not 1 <= self.max_tokens <= 8192:
            raise ValueError("max_tokens must be between 1 and 8192")
        if self.temperature is not None and (
            not math.isfinite(self.temperature) or not 0 <= self.temperature <= 2
        ):
            raise ValueError("temperature must be between 0 and 2")
        for rate in (self.input_cost_per_million, self.output_cost_per_million):
            if rate is not None and (not math.isfinite(rate) or rate < 0):
                raise ValueError("token cost rates must be finite and nonnegative")

    def public_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "family": self.family,
            "model": self.model,
            "required": self.required,
            "role": self.role,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "temperature": self.temperature,
            "cost_rates_configured": self.input_cost_per_million is not None
            and self.output_cost_per_million is not None,
        }


@dataclass(frozen=True)
class ProviderAvailability:
    provider_id: str
    selected: bool
    ready: bool
    required: bool
    model: str | None
    family: str
    missing: tuple[str, ...] = ()
    fallback_for: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "selected": self.selected,
            "ready": self.ready,
            "readiness_scope": "Local environment configuration only; live availability is not probed here.",
            "required": self.required,
            "model": self.model,
            "family": self.family,
            "missing_configuration": list(self.missing),
            "fallback_for": list(self.fallback_for),
        }


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    reported_model: str | None = None
    latency_ms: int = 0
    attempts: int = 1
    estimated_cost_usd: float | None = None


class ProviderRequestError(RuntimeError):
    """Sanitized provider error; never contains request headers or response body."""

    def __init__(
        self,
        message: str,
        *,
        attempts: int,
        latency_ms: int,
        status_code: int | None = None,
    ):
        super().__init__(message)
        self.attempts = attempts
        self.latency_ms = latency_ms
        self.status_code = status_code

    def public_message(self) -> str:
        return (
            f"HTTP {self.status_code}: {self}"
            if self.status_code is not None
            else str(self)
        )


_DEFS: dict[str, dict[str, Any]] = {
    "openai": {
        "prefix": "OPENAI",
        "family": "openai_compatible",
        "base": "https://api.openai.com/v1",
        "keys": ("OPENAI_API_KEY",),
        "models": ("OPENAI_MODEL",),
        "key_required": True,
        "base_required": False,
    },
    "anthropic": {
        "prefix": "ANTHROPIC",
        "family": "anthropic",
        "base": "https://api.anthropic.com",
        "keys": ("ANTHROPIC_API_KEY",),
        "models": ("ANTHROPIC_MODEL",),
        "key_required": True,
        "base_required": False,
    },
    "google": {
        "prefix": "GOOGLE",
        "family": "google",
        "base": "https://generativelanguage.googleapis.com/v1beta",
        "keys": ("GOOGLE_API_KEY", "GEMINI_API_KEY"),
        "models": ("GOOGLE_MODEL", "GEMINI_MODEL"),
        "key_required": True,
        "base_required": False,
    },
    "xai": {
        "prefix": "XAI",
        "family": "openai_compatible",
        "base": "https://api.x.ai/v1",
        "keys": ("XAI_API_KEY",),
        "models": ("XAI_MODEL",),
        "key_required": True,
        "base_required": False,
    },
    "deepseek": {
        "prefix": "DEEPSEEK",
        "family": "openai_compatible",
        "base": "https://api.deepseek.com",
        "keys": ("DEEPSEEK_API_KEY",),
        "models": ("DEEPSEEK_MODEL",),
        "key_required": True,
        "base_required": False,
    },
    "mistral": {
        "prefix": "MISTRAL",
        "family": "openai_compatible",
        "base": "https://api.mistral.ai/v1",
        "keys": ("MISTRAL_API_KEY",),
        "models": ("MISTRAL_MODEL",),
        "key_required": True,
        "base_required": False,
    },
    "meta_llama": {
        "prefix": "LLAMA",
        "family": "openai_compatible",
        "base": None,
        "keys": ("LLAMA_API_KEY",),
        "models": ("LLAMA_MODEL",),
        "key_required": False,
        "base_required": True,
    },
    "qwen": {
        "prefix": "QWEN",
        "family": "openai_compatible",
        "base": None,
        "keys": ("QWEN_API_KEY",),
        "models": ("QWEN_MODEL",),
        "key_required": False,
        "base_required": True,
    },
    "openai_compatible": {
        "prefix": "CROCHET_COMPAT",
        "family": "openai_compatible",
        "base": None,
        "keys": ("CROCHET_COMPAT_API_KEY",),
        "models": ("CROCHET_COMPAT_MODEL",),
        "key_required": False,
        "base_required": True,
    },
}
_ALIASES = {
    "llama": "meta_llama",
    "meta": "meta_llama",
    "meta-llama": "meta_llama",
    "gemini": "google",
    "openai-compatible": "openai_compatible",
}


def canonical_provider_id(value: str) -> str:
    value = value.strip().lower()
    return _ALIASES.get(value, value)


def supported_provider_ids() -> tuple[str, ...]:
    return tuple(_DEFS)


def _first_env(env: Mapping[str, str], names: tuple[str, ...]) -> str | None:
    for name in names:
        value = env.get(name, "").strip()
        if value:
            return value
    return None


def _env_float(
    env: Mapping[str, str], name: str, default: float, maximum: float
) -> float:
    try:
        value = float(env.get(name, default))
    except (TypeError, ValueError):
        return default
    return min(maximum, max(0.0, value)) if math.isfinite(value) else default


def _optional_env_float(
    env: Mapping[str, str], name: str, maximum: float
) -> float | None:
    raw = env.get(name, "").strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    return min(maximum, max(0.0, value)) if math.isfinite(value) else None


def _env_int(env: Mapping[str, str], name: str, default: int, maximum: int) -> int:
    try:
        return min(maximum, max(0, int(env.get(name, default))))
    except (TypeError, ValueError):
        return default


def _cost(env: Mapping[str, str], name: str) -> float | None:
    try:
        value = float(env.get(name, ""))
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) and value >= 0 else None


@dataclass
class ProviderCatalog:
    selected_ids: tuple[str, ...]
    required_ids: tuple[str, ...]
    providers: tuple[ProviderConfig, ...]
    fallbacks: dict[str, ProviderConfig]
    availability: tuple[ProviderAvailability, ...]
    configuration_issues: list[str] = field(default_factory=list)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "ProviderCatalog":
        source = os.environ if env is None else env
        issues: list[str] = []
        temperature_raw = source.get("CROCHET_PROVIDER_TEMPERATURE", "").strip()
        configured_temperature = _optional_env_float(
            source, "CROCHET_PROVIDER_TEMPERATURE", 2.0
        )
        if temperature_raw and configured_temperature is None:
            issues.append(
                "CROCHET_PROVIDER_TEMPERATURE is invalid; use a finite value from 0 to 2"
            )
        selected: list[str] = []
        for raw in source.get("CROCHET_CONSENSUS_PROVIDERS", "").split(","):
            raw = raw.strip()
            if not raw:
                continue
            provider_id = canonical_provider_id(raw)
            if provider_id not in _DEFS:
                issues.append(f"Unknown configured provider id: {raw}")
            elif provider_id not in selected:
                selected.append(provider_id)

        if source.get("CROCHET_REQUIRED_PROVIDERS", "").strip():
            required: list[str] = []
            for raw in source["CROCHET_REQUIRED_PROVIDERS"].split(","):
                provider_id = canonical_provider_id(raw)
                if provider_id in selected and provider_id not in required:
                    required.append(provider_id)
                elif provider_id not in _DEFS:
                    issues.append(f"Unknown required provider id: {raw.strip()}")
                else:
                    issues.append(f"Required provider is not selected: {provider_id}")
        else:
            required = list(selected)

        fallback_pairs: dict[str, str] = {}
        used_fallbacks: set[str] = set()
        for entry in source.get("CROCHET_FALLBACK_MAP", "").split(","):
            if not entry.strip():
                continue
            if "=" not in entry:
                issues.append(
                    "Invalid CROCHET_FALLBACK_MAP entry; expected primary=fallback"
                )
                continue
            primary_raw, fallback_raw = entry.split("=", 1)
            primary, fallback = (
                canonical_provider_id(primary_raw),
                canonical_provider_id(fallback_raw),
            )
            if primary not in selected:
                issues.append(f"Fallback mapping primary is not selected: {primary}")
            elif primary not in _DEFS or fallback not in _DEFS:
                issues.append(
                    f"Invalid fallback mapping for provider: {primary_raw.strip()}"
                )
            elif fallback in selected or fallback in used_fallbacks:
                issues.append(
                    f"Fallback {fallback} is already selected or assigned; mapping ignored"
                )
            else:
                fallback_pairs[primary] = fallback
                used_fallbacks.add(fallback)

        configs: dict[str, ProviderConfig] = {}
        availability: list[ProviderAvailability] = []
        fallback_for: dict[str, list[str]] = {}
        for primary, fallback in fallback_pairs.items():
            fallback_for.setdefault(fallback, []).append(primary)
        required_set = set(required)
        for provider_id, definition in _DEFS.items():
            prefix = definition["prefix"]
            model = _first_env(source, definition["models"])
            key = _first_env(source, definition["keys"])
            base = source.get(f"{prefix}_BASE_URL", "").strip() or definition["base"]
            missing: list[str] = []
            if not model:
                missing.append(f"{prefix}_MODEL")
            if definition["key_required"] and not key:
                missing.append("API key")
            if definition["base_required"] and not base:
                missing.append(f"{prefix}_BASE_URL")
            if base:
                try:
                    parsed = urlsplit(base)
                    invalid = (
                        parsed.scheme not in {"https", "http"}
                        or not parsed.netloc
                        or bool(
                            parsed.username
                            or parsed.password
                            or parsed.query
                            or parsed.fragment
                        )
                        or bool(key and parsed.scheme != "https")
                    )
                except ValueError:
                    invalid = True
                if invalid:
                    missing.append(
                        "valid HTTPS endpoint without embedded credentials/query/fragment"
                    )
            ready = bool(model and base and not missing)
            availability.append(
                ProviderAvailability(
                    provider_id,
                    provider_id in selected,
                    ready,
                    provider_id in required_set,
                    model,
                    definition["family"],
                    tuple(missing),
                    tuple(sorted(fallback_for.get(provider_id, []))),
                )
            )
            if ready:
                configs[provider_id] = ProviderConfig(
                    provider_id=provider_id,
                    family=definition["family"],
                    model=model,
                    base_url=str(base),
                    api_key=key,
                    required=provider_id in required_set,
                    role=source.get(f"CROCHET_ROLE_{provider_id.upper()}", "").strip()
                    or None,
                    timeout_seconds=max(
                        0.1,
                        _env_float(
                            source, "CROCHET_PROVIDER_TIMEOUT_SECONDS", 45.0, 300.0
                        ),
                    ),
                    max_retries=min(
                        5, _env_int(source, "CROCHET_PROVIDER_MAX_RETRIES", 2, 5)
                    ),
                    max_tokens=max(
                        1,
                        min(
                            8192,
                            _env_int(source, "CROCHET_PROVIDER_MAX_TOKENS", 1800, 8192),
                        ),
                    ),
                    temperature=configured_temperature,
                    input_cost_per_million=_cost(source, f"{prefix}_INPUT_COST_PER_1M"),
                    output_cost_per_million=_cost(
                        source, f"{prefix}_OUTPUT_COST_PER_1M"
                    ),
                )

        providers: list[ProviderConfig] = []
        for provider_id in selected:
            if provider_id not in configs:
                detail = next(
                    item for item in availability if item.provider_id == provider_id
                )
                issues.append(
                    f"{provider_id} is selected but not configured: missing {', '.join(detail.missing)}"
                )
            else:
                providers.append(configs[provider_id])
        fallback_configs: dict[str, ProviderConfig] = {}
        for primary, fallback_id in fallback_pairs.items():
            if fallback_id not in configs:
                detail = next(
                    item for item in availability if item.provider_id == fallback_id
                )
                issues.append(
                    f"Fallback {fallback_id} for {primary} is not configured: missing {', '.join(detail.missing)}"
                )
                continue
            value = configs[fallback_id]
            fallback_configs[primary] = ProviderConfig(
                provider_id=value.provider_id,
                family=value.family,
                model=value.model,
                base_url=value.base_url,
                api_key=value.api_key,
                required=False,
                role=value.role,
                timeout_seconds=value.timeout_seconds,
                max_retries=value.max_retries,
                max_tokens=value.max_tokens,
                temperature=value.temperature,
                input_cost_per_million=value.input_cost_per_million,
                output_cost_per_million=value.output_cost_per_million,
            )
        return cls(
            tuple(selected),
            tuple(x for x in selected if x in required_set),
            tuple(providers),
            fallback_configs,
            tuple(availability),
            issues,
        )

    def public_status(self) -> dict[str, Any]:
        return {
            "selected_provider_ids": list(self.selected_ids),
            "required_provider_ids": list(self.required_ids),
            "providers": [item.to_dict() for item in self.availability],
            "configured_models": [item.public_dict() for item in self.providers],
            "fallbacks": {
                primary: config.public_dict()
                for primary, config in self.fallbacks.items()
            },
            "configuration_issues": list(self.configuration_issues),
        }


class ProviderAdapter:
    def __init__(
        self,
        config: ProviderConfig,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.config = config
        self.transport = transport

    async def generate(self, system_prompt: str, user_prompt: str) -> ProviderResponse:
        raise NotImplementedError

    async def _post(
        self, url: str, headers: dict[str, str], body: dict[str, Any]
    ) -> tuple[dict[str, Any], int, int]:
        start = time.perf_counter()
        attempts = 0
        timeout = httpx.Timeout(self.config.timeout_seconds)
        async with httpx.AsyncClient(
            timeout=timeout, transport=self.transport, follow_redirects=False
        ) as client:
            while attempts <= self.config.max_retries:
                attempts += 1
                try:
                    response = await client.post(url, headers=headers, json=body)
                except (httpx.TimeoutException, httpx.TransportError) as exc:
                    if attempts <= self.config.max_retries:
                        await asyncio.sleep(min(0.5 * 2 ** (attempts - 1), 8.0))
                        continue
                    message = (
                        "Provider request timed out"
                        if isinstance(exc, httpx.TimeoutException)
                        else "Provider transport failed"
                    )
                    raise ProviderRequestError(
                        message,
                        attempts=attempts,
                        latency_ms=int((time.perf_counter() - start) * 1000),
                    ) from None
                status = response.status_code
                if status in {408, 425, 429} or 500 <= status <= 599:
                    if attempts <= self.config.max_retries:
                        await asyncio.sleep(_retry_delay(response, attempts - 1))
                        continue
                    if status == 429:
                        message = "Provider rate limit persisted"
                    elif status == 408:
                        message = "Provider request timed out"
                    else:
                        message = "Provider service error persisted"
                    raise ProviderRequestError(
                        message,
                        attempts=attempts,
                        latency_ms=int((time.perf_counter() - start) * 1000),
                        status_code=status,
                    )
                if status >= 400:
                    raise ProviderRequestError(
                        "Provider rejected the request",
                        attempts=attempts,
                        latency_ms=int((time.perf_counter() - start) * 1000),
                        status_code=status,
                    )
                try:
                    value = response.json()
                except (ValueError, TypeError):
                    raise ProviderRequestError(
                        "Provider returned invalid JSON",
                        attempts=attempts,
                        latency_ms=int((time.perf_counter() - start) * 1000),
                        status_code=status,
                    ) from None
                if not isinstance(value, dict):
                    raise ProviderRequestError(
                        "Provider returned an unexpected response shape",
                        attempts=attempts,
                        latency_ms=int((time.perf_counter() - start) * 1000),
                        status_code=status,
                    )
                return value, attempts, int((time.perf_counter() - start) * 1000)
        raise ProviderRequestError(
            "Provider request failed",
            attempts=max(1, attempts),
            latency_ms=int((time.perf_counter() - start) * 1000),
        )

    def _make_response(
        self,
        text: str,
        usage: Mapping[str, Any],
        model: Any,
        attempts: int,
        latency: int,
    ) -> ProviderResponse:
        input_tokens = _nonnegative_int(usage.get("input_tokens"))
        output_tokens = _nonnegative_int(usage.get("output_tokens"))
        cost = None
        if (
            input_tokens is not None
            and output_tokens is not None
            and self.config.input_cost_per_million is not None
            and self.config.output_cost_per_million is not None
        ):
            value = (
                input_tokens * self.config.input_cost_per_million
                + output_tokens * self.config.output_cost_per_million
            ) / 1_000_000
            cost = value if math.isfinite(value) else None
        return ProviderResponse(
            text, input_tokens, output_tokens, _string(model), latency, attempts, cost
        )


class OpenAICompatibleAdapter(ProviderAdapter):
    async def generate(self, system_prompt: str, user_prompt: str) -> ProviderResponse:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        body = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": self.config.max_tokens,
        }
        if self.config.temperature is not None:
            body["temperature"] = self.config.temperature
        payload, attempts, latency = await self._post(
            _openai_url(self.config.base_url), headers, body
        )
        try:
            text = _content(payload["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError):
            text = ""
        if not text:
            raise ProviderRequestError(
                "Provider response contained no chat content",
                attempts=attempts,
                latency_ms=latency,
            )
        usage = payload.get("usage") if isinstance(payload.get("usage"), dict) else {}
        return self._make_response(
            text,
            {
                "input_tokens": usage.get("prompt_tokens"),
                "output_tokens": usage.get("completion_tokens"),
            },
            payload.get("model"),
            attempts,
            latency,
        )


class AnthropicAdapter(ProviderAdapter):
    async def generate(self, system_prompt: str, user_prompt: str) -> ProviderResponse:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "anthropic-version": "2023-06-01",
        }
        if self.config.api_key:
            headers["x-api-key"] = self.config.api_key
        body = {
            "model": self.config.model,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "max_tokens": self.config.max_tokens,
        }
        if self.config.temperature is not None:
            body["temperature"] = self.config.temperature
        payload, attempts, latency = await self._post(
            _anthropic_url(self.config.base_url), headers, body
        )
        text = _content(payload.get("content"))
        if not text:
            raise ProviderRequestError(
                "Provider response contained no message content",
                attempts=attempts,
                latency_ms=latency,
            )
        usage = payload.get("usage") if isinstance(payload.get("usage"), dict) else {}
        return self._make_response(text, usage, payload.get("model"), attempts, latency)


class GoogleAdapter(ProviderAdapter):
    async def generate(self, system_prompt: str, user_prompt: str) -> ProviderResponse:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.config.api_key:
            headers["x-goog-api-key"] = self.config.api_key
        generation_config = {"maxOutputTokens": self.config.max_tokens}
        if self.config.temperature is not None:
            generation_config["temperature"] = self.config.temperature
        body = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": generation_config,
        }
        payload, attempts, latency = await self._post(
            _google_url(self.config.base_url, self.config.model), headers, body
        )
        try:
            text = _content(payload["candidates"][0]["content"]["parts"])
        except (KeyError, IndexError, TypeError):
            text = ""
        if not text:
            raise ProviderRequestError(
                "Provider response contained no generated content",
                attempts=attempts,
                latency_ms=latency,
            )
        usage = (
            payload.get("usageMetadata")
            if isinstance(payload.get("usageMetadata"), dict)
            else {}
        )
        return self._make_response(
            text,
            {
                "input_tokens": usage.get("promptTokenCount"),
                "output_tokens": usage.get("candidatesTokenCount"),
            },
            payload.get("modelVersion"),
            attempts,
            latency,
        )


def create_adapter(
    config: ProviderConfig, *, transport: httpx.AsyncBaseTransport | None = None
) -> ProviderAdapter:
    cls = (
        AnthropicAdapter
        if config.family == "anthropic"
        else GoogleAdapter
        if config.family == "google"
        else OpenAICompatibleAdapter
    )
    return cls(config, transport=transport)


def _openai_url(base: str) -> str:
    value = base.rstrip("/")
    return value if value.endswith("/chat/completions") else f"{value}/chat/completions"


def _anthropic_url(base: str) -> str:
    value = base.rstrip("/")
    if value.endswith("/v1/messages"):
        return value
    return f"{value}/messages" if value.endswith("/v1") else f"{value}/v1/messages"


def _google_url(base: str, model: str) -> str:
    value = base.rstrip("/")
    escaped = quote(model, safe="-_.")
    if "{model}" in value:
        return value.replace("{model}", escaped)
    if value.endswith(":generateContent"):
        return value
    return (
        f"{value}/{escaped}:generateContent"
        if value.endswith("/models")
        else f"{value}/models/{escaped}:generateContent"
    )


def _content(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "".join(
            item
            if isinstance(item, str)
            else item.get("text", "")
            if isinstance(item, dict)
            else ""
            for item in value
        ).strip()
    if isinstance(value, dict):
        return str(value.get("text", "")).strip()
    return ""


def _nonnegative_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        result = int(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return result if result >= 0 else None


def _string(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _retry_delay(response: httpx.Response, index: int) -> float:
    value = response.headers.get("Retry-After", "").strip()
    if value:
        try:
            return max(0.0, min(float(value), 15.0))
        except ValueError:
            try:
                target = parsedate_to_datetime(value)
                if target.tzinfo is None:
                    target = target.replace(tzinfo=timezone.utc)
                return max(0.0, min(target.timestamp() - time.time(), 15.0))
            except (TypeError, ValueError, OverflowError):
                pass
    return min(0.5 * 2**index, 8.0)
