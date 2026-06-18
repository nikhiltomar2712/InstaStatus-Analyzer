from src.analyzer import AccountAnalyzer
from src.sample_data import build_demo_account


class FakeBotDetector:
    def __init__(self):
        self.labels = iter(["real", "suspicious", "bot"])

    def analyze_follower(self, follower, user_info):
        label = next(self.labels)
        probability = {"real": 12, "suspicious": 52, "bot": 88}[label]
        return probability, label

    def sentiment_score(self, text):
        return 0.5


def test_analyze_counts_followers_and_engagement():
    analyzer = AccountAnalyzer(bot_detector=FakeBotDetector())
    data = {
        "user_info": {"username": "test", "follower_count": 1000, "following_count": 50},
        "followers": [{"username": "a"}, {"username": "b"}, {"username": "c"}],
        "posts": [
            {"like_count": 100, "comment_count": 10, "code": "A", "media_type": 1},
            {"like_count": 200, "comment_count": 20, "code": "B", "media_type": 2, "view_count": 1000},
        ],
    }

    result = analyzer.analyze(data)

    assert result["engagement"]["avg_likes"] == 150
    assert result["engagement"]["avg_comments"] == 15
    assert result["engagement"]["engagement_rate_percent"] == 16.5
    assert result["follower_quality"]["real_count"] == 1
    assert result["follower_quality"]["suspicious_count"] == 1
    assert result["follower_quality"]["bot_count"] == 1
    assert result["follower_quality"]["risk_level"] == "high"
    assert result["content_summary"]["posts_analyzed"] == 2


def test_demo_account_can_be_analyzed_without_credentials():
    result = AccountAnalyzer().analyze(build_demo_account("demo", followers_amount=10, posts_amount=3))

    assert result["user_info"]["username"] == "demo"
    assert result["follower_quality"]["total_followers_analyzed"] == 10
    assert result["content_summary"]["posts_analyzed"] == 3
