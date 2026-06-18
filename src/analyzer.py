from collections import Counter
from typing import Dict, Iterable, List, Optional

from src.bot_detector import BotDetector


class AccountAnalyzer:
    def __init__(self, bot_detector: Optional[BotDetector] = None):
        self.bot_detector = bot_detector or BotDetector()

    def analyze(self, account_data: Dict) -> Dict:
        user_info = account_data.get("user_info", {})
        followers = account_data.get("followers", [])
        posts = account_data.get("posts", [])

        follower_count = self._as_number(user_info.get("follower_count"))
        avg_likes = self._average(post.get("like_count", 0) for post in posts)
        avg_comments = self._average(post.get("comment_count", 0) for post in posts)
        engagement_rate = (
            ((avg_likes + avg_comments) / follower_count) * 100 if follower_count else 0
        )

        follower_analysis = []
        for follower in followers:
            analyzed_follower = dict(follower)
            probability, label = self.bot_detector.analyze_follower(analyzed_follower, user_info)
            analyzed_follower["bot_probability"] = probability
            analyzed_follower["bot_label"] = label
            analyzed_follower["sentiment_score"] = self.bot_detector.sentiment_score(
                analyzed_follower.get("biography", "")
            )
            follower_analysis.append(analyzed_follower)

        label_counts = Counter(follower.get("bot_label", "unknown") for follower in follower_analysis)
        total_analyzed = len(follower_analysis)
        total_likes = sum(self._as_number(post.get("like_count")) for post in posts)
        total_comments = sum(self._as_number(post.get("comment_count")) for post in posts)
        total_views = sum(
            self._as_number(post.get("view_count")) for post in posts if post.get("media_type") == 2
        )

        top_posts = sorted(
            (self._with_post_score(post) for post in posts),
            key=lambda post: post["engagement_score"],
            reverse=True,
        )[:5]

        suspicious_percent = self._percent(
            label_counts.get("bot", 0) + label_counts.get("suspicious", 0),
            total_analyzed,
        )

        return {
            "user_info": user_info,
            "engagement": {
                "avg_likes": round(avg_likes, 2),
                "avg_comments": round(avg_comments, 2),
                "engagement_rate_percent": round(engagement_rate, 2),
                "total_likes_last_posts": total_likes,
                "total_comments_last_posts": total_comments,
                "total_views_last_reels": total_views,
            },
            "follower_quality": {
                "total_followers_analyzed": total_analyzed,
                "real_count": label_counts.get("real", 0),
                "suspicious_count": label_counts.get("suspicious", 0),
                "bot_count": label_counts.get("bot", 0),
                "percent_real": self._percent(label_counts.get("real", 0), total_analyzed),
                "percent_suspicious": self._percent(label_counts.get("suspicious", 0), total_analyzed),
                "percent_bot": self._percent(label_counts.get("bot", 0), total_analyzed),
                "risk_level": self._risk_level(suspicious_percent),
            },
            "content_summary": self._content_summary(posts),
            "top_posts": top_posts,
            "growth_trend": "not_enough_historical_data",
            "follower_details": follower_analysis,
        }

    @staticmethod
    def _average(values: Iterable) -> float:
        numbers = [AccountAnalyzer._as_number(value) for value in values]
        return sum(numbers) / len(numbers) if numbers else 0.0

    @staticmethod
    def _as_number(value) -> float:
        try:
            if value is None:
                return 0
            return float(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _percent(part: int, whole: int) -> float:
        return round((part / whole) * 100, 2) if whole else 0

    @staticmethod
    def _risk_level(suspicious_percent: float) -> str:
        if suspicious_percent >= 40:
            return "high"
        if suspicious_percent >= 15:
            return "medium"
        return "low"

    @staticmethod
    def _with_post_score(post: Dict) -> Dict:
        scored_post = dict(post)
        likes = AccountAnalyzer._as_number(scored_post.get("like_count"))
        comments = AccountAnalyzer._as_number(scored_post.get("comment_count"))
        views = AccountAnalyzer._as_number(scored_post.get("view_count"))
        scored_post["engagement_score"] = round(likes + (comments * 2) + (views * 0.05), 2)
        return scored_post

    @staticmethod
    def _content_summary(posts: List[Dict]) -> Dict:
        media_names = {1: "photo", 2: "video", 8: "carousel"}
        counts = Counter(media_names.get(post.get("media_type"), "other") for post in posts)
        return {
            "posts_analyzed": len(posts),
            "photos": counts.get("photo", 0),
            "videos": counts.get("video", 0),
            "carousels": counts.get("carousel", 0),
            "other": counts.get("other", 0),
        }
