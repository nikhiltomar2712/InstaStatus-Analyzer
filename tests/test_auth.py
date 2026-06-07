import pytest
from src.auth import AuthManager
from unittest.mock import patch, MagicMock

@patch("src.auth.Client")
def test_login_success(mock_client):
    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    auth = AuthManager()
    auth.username = "test"
    auth.password = "pass"
    result = auth.login()
    assert result == mock_instance
    mock_instance.login.assert_called_once_with("test", "pass")
