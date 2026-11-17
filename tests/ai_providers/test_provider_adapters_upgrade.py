import asyncio
import json

import httpx
import pytest

from crochet_checker.ai_providers.provider_adapters import (
    AnthropicAdapter,
    GoogleAdapter,
    OpenAICompatibleAdapter,
    ProviderCatalog,
    ProviderConfig,
    ProviderRequestError,
)


def test_provider_catalog_requires_explicit_selection_model_and_key():
    empty = ProviderCatalog.from_env({})
    assert empty.selected_ids == ()
    assert empty.providers == ()

    incomplete = ProviderCatalog.from_env({"CROCHET_CONSENSUS_PROVIDERS": "openai"})
    assert incomplete.providers == ()
    assert any(
        "openai is selected but not configured" in item
        for item in incomplete.configuration_issues
    )


def test_provider_catalog_does_not_expose_secret_and_does_not_claim_live_availability():
    env = {
        "CROCHET_CONSENSUS_PROVIDERS": "openai,anthropic",
        "OPENAI_MODEL": "explicit-test-model-a",
        "OPENAI_API_KEY": "secret-openai",
        "ANTHROPIC_MODEL": "explicit-test-model-b",
        "ANTHROPIC_API_KEY": "secret-anthropic",
    }
    catalog = ProviderCatalog.from_env(env)
    assert [item.provider_id for item in catalog.providers] == ["openai", "anthropic"]
    assert catalog.required_ids == ("openai", "anthropic")
    public = json.dumps(catalog.public_status())
    assert "secret-openai" not in public and "secret-anthropic" not in public
    assert all(
        "live availability is not probed" in item["readiness_scope"]
        for item in catalog.public_status()["providers"]
    )
    assert "secret-openai" not in repr(catalog.providers[0])


def test_catalog_reports_unknown_and_misconfigured_fallbacks_without_faking_a_provider():
    env = {
        "CROCHET_CONSENSUS_PROVIDERS": "openai,not-a-provider",
        "CROCHET_FALLBACK_MAP": "openai=deepseek",
        "OPENAI_MODEL": "primary-explicit",
        "OPENAI_API_KEY": "primary-secret",
    }
    catalog = ProviderCatalog.from_env(env)
    assert [item.provider_id for item in catalog.providers] == ["openai"]
    assert catalog.fallbacks == {}
    assert any(
        "Unknown configured provider id" in item
        for item in catalog.configuration_issues
    )
    assert any(
        "Fallback deepseek" in item and "not configured" in item
        for item in catalog.configuration_issues
    )


def test_catalog_honors_required_subset_and_explicit_fallback_configuration():
    env = {
        "CROCHET_CONSENSUS_PROVIDERS": "openai,anthropic",
        "CROCHET_REQUIRED_PROVIDERS": "openai",
        "CROCHET_FALLBACK_MAP": "openai=deepseek",
        "OPENAI_MODEL": "primary-explicit",
        "OPENAI_API_KEY": "primary-secret",
        "ANTHROPIC_MODEL": "optional-explicit",
        "ANTHROPIC_API_KEY": "optional-secret",
        "DEEPSEEK_MODEL": "fallback-explicit",
        "DEEPSEEK_API_KEY": "fallback-secret",
    }
    catalog = ProviderCatalog.from_env(env)
    assert catalog.required_ids == ("openai",)
    assert catalog.fallbacks["openai"].provider_id == "deepseek"
    assert catalog.fallbacks["openai"].required is False
    assert "fallback-secret" not in json.dumps(catalog.public_status())


def test_provider_config_rejects_unsafe_key_url_and_nonfinite_settings():
    with pytest.raises(ValueError, match="HTTPS"):
        ProviderConfig(
            "p", "openai_compatible", "model", "http://localhost/v1", api_key="secret"
        )
    with pytest.raises(ValueError, match="credentials"):
        ProviderConfig(
            "p", "openai_compatible", "model", "https://user:pass@example.test/v1"
        )
    with pytest.raises(ValueError, match="between 0 and 300"):
        ProviderConfig(
            "p",
            "openai_compatible",
            "model",
            "https://example.test/v1",
            timeout_seconds=float("nan"),
        )


def test_openai_compatible_adapter_sends_server_side_auth_and_calculates_reported_cost():
    requests = []

    async def handler(request):
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "model": "service-model",
                "choices": [{"message": {"content": '{"ok":true}'}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5},
            },
        )

    config = ProviderConfig(
        "openai",
        "openai_compatible",
        "explicit-model",
        "https://mock.test/v1",
        api_key="top-secret",
        input_cost_per_million=2.0,
        output_cost_per_million=4.0,
    )
    adapter = OpenAICompatibleAdapter(config, transport=httpx.MockTransport(handler))
    result = asyncio.run(adapter.generate("system only", "user only"))

    assert requests[0].url.path == "/v1/chat/completions"
    assert requests[0].headers["Authorization"] == "Bearer top-secret"
    body = json.loads(requests[0].content)
    assert body["model"] == "explicit-model"
    assert "temperature" not in body
    assert "top-secret" not in requests[0].content.decode()
    assert result.text == '{"ok":true}'
    assert result.reported_model == "service-model"
    assert result.attempts == 1
    assert result.estimated_cost_usd == pytest.approx(0.00004)


def test_transient_http_status_retries_and_only_final_safe_error_is_exposed(
    monkeypatch,
):
    calls = []

    async def handler(request):
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(
                429, headers={"Retry-After": "0"}, text="top-secret upstream details"
            )
        return httpx.Response(200, json={"choices": [{"message": {"content": "ok"}}]})

    async def no_sleep(_seconds):
        return None

    monkeypatch.setattr(
        "crochet_checker.ai_providers.provider_adapters.asyncio.sleep", no_sleep
    )
    config = ProviderConfig(
        "openai",
        "openai_compatible",
        "m",
        "https://mock.test/v1",
        api_key="top-secret",
        max_retries=1,
    )
    adapter = OpenAICompatibleAdapter(config, transport=httpx.MockTransport(handler))
    result = asyncio.run(adapter.generate("sys", "user"))
    assert result.attempts == 2
    assert len(calls) == 2


def test_network_timeout_is_retried_or_reported_without_response_body():
    async def handler(request):
        raise httpx.ReadTimeout("dummy timeout with no credential", request=request)

    config = ProviderConfig(
        "openai",
        "openai_compatible",
        "m",
        "https://mock.test/v1",
        api_key="test-only-dummy-key",
        timeout_seconds=0.05,
        max_retries=0,
    )
    adapter = OpenAICompatibleAdapter(config, transport=httpx.MockTransport(handler))
    with pytest.raises(ProviderRequestError) as error:
        asyncio.run(adapter.generate("sys", "user"))
    assert error.value.attempts == 1
    assert error.value.public_message() == "Provider request timed out"
    assert "test-only-dummy-key" not in error.value.public_message()


def test_persistent_provider_error_is_sanitized():
    async def handler(_request):
        return httpx.Response(401, text="top-secret request body and leaked token")

    config = ProviderConfig(
        "openai",
        "openai_compatible",
        "m",
        "https://mock.test/v1",
        api_key="top-secret",
        max_retries=0,
    )
    adapter = OpenAICompatibleAdapter(config, transport=httpx.MockTransport(handler))
    with pytest.raises(ProviderRequestError) as error:
        asyncio.run(adapter.generate("sys", "user"))
    assert "401" in error.value.public_message()
    assert "top-secret" not in error.value.public_message()
    assert "leaked token" not in str(error.value)


def test_anthropic_and_google_adapters_use_native_wire_protocols():
    requests = []

    async def handler(request):
        requests.append(request)
        if request.url.path.endswith("/v1/messages"):
            return httpx.Response(
                200,
                json={
                    "model": "anthropic-reported",
                    "content": [{"type": "text", "text": "anthropic result"}],
                    "usage": {"input_tokens": 4, "output_tokens": 6},
                },
            )
        return httpx.Response(
            200,
            json={
                "modelVersion": "google-reported",
                "candidates": [{"content": {"parts": [{"text": "google result"}]}}],
                "usageMetadata": {"promptTokenCount": 8, "candidatesTokenCount": 9},
            },
        )

    anthropic = AnthropicAdapter(
        ProviderConfig(
            "anthropic",
            "anthropic",
            "explicit-anthropic-model",
            "https://mock.test",
            api_key="anthropic-secret",
        ),
        transport=httpx.MockTransport(handler),
    )
    google = GoogleAdapter(
        ProviderConfig(
            "google",
            "google",
            "explicit-google-model",
            "https://mock.test/v1beta",
            api_key="google-secret",
        ),
        transport=httpx.MockTransport(handler),
    )
    a = asyncio.run(anthropic.generate("system", "user"))
    g = asyncio.run(google.generate("system", "user"))

    assert requests[0].url.path == "/v1/messages"
    assert requests[0].headers["x-api-key"] == "anthropic-secret"
    assert (
        requests[1].url.path == "/v1beta/models/explicit-google-model:generateContent"
    )
    assert requests[1].headers["x-goog-api-key"] == "google-secret"
    assert a.text == "anthropic result" and a.input_tokens == 4
    assert g.text == "google result" and g.output_tokens == 9
