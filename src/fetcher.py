import time
from typing import Dict, List

try:
    from instagrapi.exceptions import RateLimitError
except ImportError:
    class RateLimitError(Exception):
        pass

from src.rate_limiter import rate_limit
from src.utils import logger


class InstagramFetcher:
    def __init__(self, client):
        self.client = client

    @rate_limit
    def get_user_info(self, username: str) -> Dict:
        self._require_client()
        try:
            user_id = self.client.user_id_from_username(username)
            info = self.client.user_info(user_id)
            return {
                "pk": self._value(info, "pk", user_id),
                "username": self._value(info, "username", username),
                "full_name": self._value(info, "full_name", ""),
                "biography": self._value(info, "biography", ""),
                "follower_count": self._value(info, "follower_count", 0),
                "following_count": self._value(info, "following_count", 0),
                "media_count": self._value(info, "media_count", 0),
                "is_private": self._value(info, "is_private", False),
                "is_verified": self._value(info, "is_verified", False),
                "external_url": self._value(info, "external_url", ""),
                "profile_pic_url": str(self._value(info, "profile_pic_url", "") or ""),
            }
        except Exception as exc:
            logger.error("Failed to fetch user info for %s: %s", username, exc)
            raise

    @rate_limit
    def get_followers(self, user_id: str, amount: int = 50) -> List[Dict]:
        self._require_client()
        try:
            followers = self.client.user_followers(user_id, amount=amount)
            return [self._serialize_follower(pk, data) for pk, data in followers.items()]
        except RateLimitError:
            logger.warning("Instagram rate limit hit while fetching followers; sleeping for 5 minutes.")
            time.sleep(300)
            return self.get_followers(user_id, amount)
        except Exception as exc:
            logger.error("Failed to fetch followers for %s: %s", user_id, exc)
            return []

    @rate_limit
    def get_recent_posts(self, user_id: str, amount: int = 12) -> List[Dict]:
        self._require_client()
        try:
            medias = self.client.user_medias(user_id, amount)
            return [self._serialize_post(media) for media in medias]
        except Exception as exc:
            logger.error("Failed to fetch posts for %s: %s", user_id, exc)
            return []

    def fetch_account_data(self, username: str, followers_amount: int = 50, posts_amount: int = 12) -> Dict:
        user_info = self.get_user_info(username)
        user_id = user_info["pk"]
        return {
            "user_info": user_info,
            "followers": self.get_followers(user_id, amount=followers_amount),
            "posts": self.get_recent_posts(user_id, amount=posts_amount),
        }

    def _require_client(self) -> None:
        if self.client is None:
            raise RuntimeError("InstagramFetcher requires an authenticated Instagrapi client.")

    @staticmethod
    def _serialize_follower(pk, data) -> Dict:
        return {
            "pk": pk,
            "username": InstagramFetcher._value(data, "username", ""),
            "full_name": InstagramFetcher._value(data, "full_name", ""),
            "is_private": InstagramFetcher._value(data, "is_private", False),
            "profile_pic_url": str(InstagramFetcher._value(data, "profile_pic_url", "") or ""),
            "follower_count": InstagramFetcher._value(data, "follower_count", 0),
            "following_count": InstagramFetcher._value(data, "following_count", 0),
            "media_count": InstagramFetcher._value(data, "media_count", 0),
            "biography": InstagramFetcher._value(data, "biography", ""),
        }

    @staticmethod
    def _serialize_post(media) -> Dict:
        return {
            "id": InstagramFetcher._value(media, "id", ""),
            "code": InstagramFetcher._value(media, "code", ""),
            "like_count": InstagramFetcher._value(media, "like_count", 0),
            "comment_count": InstagramFetcher._value(media, "comment_count", 0),
            "caption_text": InstagramFetcher._value(media, "caption_text", ""),
            "taken_at": InstagramFetcher._value(media, "taken_at", ""),
            "media_type": InstagramFetcher._value(media, "media_type", 0),
            "view_count": InstagramFetcher._value(media, "view_count", 0),
        }

    @staticmethod
    def _value(source, name: str, default=None):
        if isinstance(source, dict):
            return source.get(name, default)
        return getattr(source, name, default)
