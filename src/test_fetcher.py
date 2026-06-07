import pytest
from src.fetcher import InstagramFetcher
from unittest.mock import MagicMock

def test_get_user_info(mocker):
    mock_client = MagicMock()
    mock_client.user_id_from_username.return_value = "123"
    mock_client.user_info.return_value = MagicMock(
        pk="123",
        username="test",
        full_name="Test",
        biography="",
        follower_count=100,
        following_count=50,
        media_count=10,
        is_private=False,
        is_verified=False,
        external_url="",
        profile_pic_url=""
    )
    fetcher = InstagramFetcher(mock_client)
    info = fetcher.get_user_info("test")
    assert info["username"] == "test"
