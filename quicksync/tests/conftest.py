import pytest


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("MAILCHIMP_API_KEY", "mock_api_key")
    monkeypatch.setenv("MAILCHIMP_SERVER_PREFIX", "mock_server")