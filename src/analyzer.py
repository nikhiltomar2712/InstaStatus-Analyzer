import pandas as pd
import numpy as np
from typing import Dict, List
from src.bot_detector import BotDetector
from src.utils import logger

class AccountAnalyzer:
    def __init__(self):
        self.bot_detector = BotDetector()

    def analyze(self, account_data: Dict) -> Dict:
        user_info = account_data["user_info"]
        followers = account_data["followers"]
        posts = account_data["posts"]

        # 1. Basic engagement metrics
        avg_likes = np.mean([p["like_count"] for p in posts]) if posts else 0
        avg_comments = np.mean([p["comment_count"] for p in posts]) if posts else 0
        engagement_rate = (avg_likes / user_info["follower_count"]) * 100 if user_info["follower_count"] > 0 else 0

        # 2. Bot detection on followers
        follower_analysis = []
        for f in followers:
            prob, label = self.bot_detector.analyze_follower(f, user_info)
            # Simple comment sentiment on bio
            sent = self.bot_detector.sentiment_score(f.get("biography", ""))
            f["bot_probability"] = prob
            f["bot_label"] = label
            f["sentiment_score"] = sent
            follower_analysis.append(f)

        # 3. Overall stats
        df_followers = pd.DataFrame(follower_analysis)
        total = len(df_followers)
        bots = len(df_followers[df_followers["bot_label"] == "bot"])
        suspicious = len(df_followers[df_followers["bot_label"] == "suspicious"])
        real = len(df_followers[df_followers["bot_label"] == "real"])

        # 4. Growth trend (simple: compare follower count to posts frequency – placeholder)
        # Real implementation would need historical data. We'll estimate account age from posts?
        # For now, set to "N/A"
        growth_trend = "stable"

        # 5. Top posts (by likes)
        top_posts = sorted(posts, key=lambda x: x["like_count"], reverse=True)[:5]

        result = {
            "user_info": user_info,
            "engagement": {
                "avg_likes": avg_likes,
                "avg_comments": avg_comments,
                "engagement_rate_percent": round(engagement_rate, 2),
                "total_likes_last_posts": sum(p["like_count"] for p in posts),
                "total_views_last_reels": sum(p.get("view_count", 0) for p in posts if p["media_type"] == 2),
            },
            "follower_quality": {
                "total_followers_analyzed": total,
                "real_count": real,
                "suspicious_count": suspicious,
                "bot_count": bots,
                "percent_real": round((real/total)*100, 2) if total else 0,
                "percent_bot": round((bots/total)*100, 2) if total else 0,
            },
            "top_posts": top_posts,
            "growth_trend": growth_trend,
            "follower_details": follower_analysis  # raw list
        }
        return result
