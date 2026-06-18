from datetime import datetime, timedelta, timezone
from typing import Dict, List


def build_demo_account(username: str = "instagram", followers_amount: int = 50, posts_amount: int = 12) -> Dict:
    followers_amount = max(followers_amount, 0)
    posts_amount = max(posts_amount, 0)
    return {
        "user_info": _demo_user(username),
        "followers": _demo_followers(followers_amount),
        "posts": _demo_posts(posts_amount),
    }


def _demo_user(username: str) -> Dict:
    return {
        "pk": "demo-user",
        "username": username,
        "full_name": f"{username.title()} Demo Account",
        "biography": "Creator account used for local InstaStatus Analyzer demos.",
        "follower_count": 12840,
        "following_count": 612,
        "media_count": 184,
        "is_private": False,
        "is_verified": False,
        "external_url": "",
        "profile_pic_url": "https://example.com/profile.jpg",
    }


def _demo_followers(amount: int) -> List[Dict]:
    followers = []
    for index in range(amount):
        if index % 9 == 0:
            followers.append(
                {
                    "pk": f"bot-{index}",
                    "username": f"dealpromo{index}999",
                    "full_name": "Promo Deals",
                    "is_private": False,
                    "profile_pic_url": "",
                    "follower_count": 8 + index,
                    "following_count": 1800 + (index * 13),
                    "media_count": 0,
                    "biography": "Follow back and DM for promo giveaway",
                }
            )
        elif index % 5 == 0:
            followers.append(
                {
                    "pk": f"suspicious-{index}",
                    "username": f"user_{index}481",
                    "full_name": "",
                    "is_private": False,
                    "profile_pic_url": "https://example.com/avatar.jpg" if index % 10 else "",
                    "follower_count": 70 + index,
                    "following_count": 850 + (index * 7),
                    "media_count": 1,
                    "biography": "Crypto investment tips",
                }
            )
        else:
            followers.append(
                {
                    "pk": f"real-{index}",
                    "username": f"creator_{index}",
                    "full_name": f"Creator {index}",
                    "is_private": index % 7 == 0,
                    "profile_pic_url": "https://example.com/avatar.jpg",
                    "follower_count": 220 + (index * 17),
                    "following_count": 160 + (index * 3),
                    "media_count": 12 + (index % 9),
                    "biography": "Artist and community builder learning in public",
                }
            )
    return followers


def _demo_posts(amount: int) -> List[Dict]:
    now = datetime.now(timezone.utc)
    posts = []
    for index in range(amount):
        media_type = [1, 2, 8][index % 3]
        posts.append(
            {
                "id": f"demo-post-{index}",
                "code": f"DEMO{index:03}",
                "like_count": 420 + (index * 37),
                "comment_count": 18 + (index % 6) * 4,
                "caption_text": f"Demo post {index}",
                "taken_at": (now - timedelta(days=index * 3)).isoformat(),
                "media_type": media_type,
                "view_count": 2800 + (index * 120) if media_type == 2 else 0,
            }
        )
    return posts
