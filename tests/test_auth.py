from unittest.mock import MagicMock, patch

import pytest

from src.auth import AuthManager


@patch("src.auth.Client")
def test_login_success(mock_client, monkeypatch, tmp_path):
    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    monkeypatch.setenv("INSTAGRAM_USERNAME", "test")
    monkeypatch.setenv("INSTAGRAM_PASSWORD", "pass")
    monkeypatch.setenv("SESSION_DIR", str(tmp_path))

    auth = AuthManager()
    result = auth.login()

    assert result == mock_instance
    mock_instance.login.assert_called_once_with("test", "pass")
    mock_instance.dump_settings.assert_called_once_with(str(tmp_path / "test.session"))


def test_login_requires_credentials(monkeypatch, tmp_path):
    monkeypatch.delenv("INSTAGRAM_USERNAME", raising=False)
    monkeypatch.delenv("INSTAGRAM_PASSWORD", raising=False)
    monkeypatch.setenv("SESSION_DIR", str(tmp_path))

    auth = AuthManager(client_factory=MagicMock)

    with pytest.raises(ValueError):
        auth.login()
