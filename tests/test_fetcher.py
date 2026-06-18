from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from src.fetcher import InstagramFetcher


def test_get_user_info_serializes_instagram_object():
    mock_client = MagicMock()
    mock_client.user_id_from_username.return_value = "123"
    mock_client.user_info.return_value = SimpleNamespace(
        pk="123",
        username="test",
        full_name="Test User",
        biography="Bio",
        follower_count=100,
        following_count=50,
        media_count=10,
        is_private=False,
        is_verified=False,
        external_url="",
        profile_pic_url="https://example.com/profile.jpg",
    )

    info = InstagramFetcher(mock_client).get_user_info("test")

    assert info["username"] == "test"
    assert info["follower_count"] == 100
    mock_client.user_info.assert_called_once_with("123")


def test_fetcher_requires_client():
    fetcher = InstagramFetcher(None)

    with pytest.raises(RuntimeError):
        fetcher.get_user_info("test")
