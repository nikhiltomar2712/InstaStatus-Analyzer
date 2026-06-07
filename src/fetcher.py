from instagrapi import Client
from instagrapi.exceptions import LoginRequired, RateLimitError
from src.rate_limiter import rate_limit
from src.utils import logger
import time
from typing import List, Dict, Optional
import pandas as pd

class InstagramFetcher:
    def __init__(self, client: Client):
        self.client = client

    @rate_limit
    def get_user_info(self, username: str) -> Dict:
        try:
            user_id = self.client.user_id_from_username(username)
            info = self.client.user_info(user_id)
            return {
                "pk": info.pk,
                "username": info.username,
                "full_name": info.full_name,
                "biography": info.biography,
                "follower_count": info.follower_count,
                "following_count": info.following_count,
                "media_count": info.media_count,
                "is_private": info.is_private,
                "is_verified": info.is_verified,
                "external_url": info.external_url,
                "profile_pic_url": info.profile_pic_url,
            }
        except Exception as e:
            logger.error(f"Failed to fetch user info: {e}")
            raise

    @rate_limit
    def get_followers(self, user_id: str, amount: int = 0) -> List[Dict]:
        """Fetch followers with metadata. amount=0 means all."""
        try:
            followers = self.client.user_followers(user_id, amount=amount)
            result = []
            for pk, data in followers.items():
                result.append({
                    "pk": pk,
                    "username": data.username,
                    "full_name": data.full_name,
                    "is_private": data.is_private,
                    "profile_pic_url": data.profile_pic_url,
                    "follower_count": getattr(data, "follower_count", None),
                    "following_count": getattr(data, "following_count", None),
                    "biography": getattr(data, "biography", ""),
                })
            return result
        except RateLimitError:
            logger.warning("Rate limit hit, sleeping...")
            time.sleep(300)
            return self.get_followers(user_id, amount)
        except Exception as e:
            logger.error(f"Failed to fetch followers: {e}")
            return []

    @rate_limit
    def get_recent_posts(self, user_id: str, amount: int = 12) -> List[Dict]:
        try:
            medias = self.client.user_medias(user_id, amount)
            posts = []
            for media in medias:
                posts.append({
                    "id": media.id,
                    "code": media.code,
                    "like_count": media.like_count,
                    "comment_count": media.comment_count,
                    "caption_text": media.caption_text,
                    "taken_at": media.taken_at,
                    "media_type": media.media_type,  # 1=photo, 2=video, 8=carousel
                    "view_count": getattr(media, "view_count", 0),  # for videos/reels
                })
            return posts
        except Exception as e:
            logger.error(f"Failed to get posts: {e}")
            return []

    def fetch_account_data(self, username: str, followers_amount: int = 0, posts_amount: int = 12) -> Dict:
        user_info = self.get_user_info(username)
        user_id = user_info["pk"]
        followers = self.get_followers(user_id, amount=followers_amount)
        posts = self.get_recent_posts(user_id, amount=posts_amount)
        return {
            "user_info": user_info,
            "followers": followers,
            "posts": posts
        }
