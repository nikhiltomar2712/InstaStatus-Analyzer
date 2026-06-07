import pytest
from src.analyzer import AccountAnalyzer

def test_analyze_basic():
    analyzer = AccountAnalyzer()
    data = {
        "user_info": {"username": "test", "follower_count": 100, "following_count": 50, "biography": ""},
        "followers": [],
        "posts": []
    }
    result = analyzer.analyze(data)
    assert result["follower_quality"]["total_followers_analyzed"] == 0
