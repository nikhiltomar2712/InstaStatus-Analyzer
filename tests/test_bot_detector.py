from src.bot_detector import BotDetector


def test_bot_detector_labels_clear_bot_profile():
    detector = BotDetector()
    probability, label = detector.analyze_follower(
        {
            "username": "promo999888",
            "biography": "Follow back crypto giveaway",
            "follower_count": 4,
            "following_count": 1600,
            "media_count": 0,
            "profile_pic_url": "",
        }
    )

    assert probability >= 70
    assert label == "bot"


def test_bot_detector_labels_realistic_profile():
    detector = BotDetector()
    probability, label = detector.analyze_follower(
        {
            "username": "creator_jane",
            "biography": "Artist and community builder",
            "follower_count": 900,
            "following_count": 280,
            "media_count": 24,
            "profile_pic_url": "https://example.com/avatar.jpg",
        }
    )

    assert probability < 35
    assert label == "real"
