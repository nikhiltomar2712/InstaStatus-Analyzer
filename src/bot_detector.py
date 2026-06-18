import os
import re
from dataclasses import dataclass
from typing import Dict, Optional, Tuple


GENERIC_BIO_TERMS = (
    "follow for follow",
    "follow back",
    "brand ambassador",
    "dm for promo",
    "crypto",
    "investment",
    "giveaway",
    "public figure",
    "model",
)

POSITIVE_WORDS = {
    "artist",
    "builder",
    "community",
    "creator",
    "design",
    "family",
    "founder",
    "learning",
    "official",
    "photography",
    "student",
}

NEGATIVE_WORDS = {
    "betting",
    "cash",
    "casino",
    "crypto",
    "deal",
    "discount",
    "earn",
    "forex",
    "giveaway",
    "promo",
    "winner",
}


@dataclass(frozen=True)
class FollowerFeatures:
    follower_count: int
    following_count: int
    media_count: int
    following_to_follower_ratio: float
    bio_length: int
    generic_bio_terms: int
    has_profile_picture: bool
    is_private: bool
    username_digit_ratio: float


class BotDetector:
    """Score follower quality without requiring heavyweight ML dependencies.

    A saved sklearn-style model can still be used by setting BOT_MODEL_PATH and,
    optionally, BOT_SCALER_PATH. If no model is configured, the detector falls
    back to deterministic heuristics that are cheap enough for tests and demos.
    """

    def __init__(self, model_path: Optional[str] = None, scaler_path: Optional[str] = None):
        self.model = None
        self.scaler = None
        self.model_path = model_path or os.getenv("BOT_MODEL_PATH")
        self.scaler_path = scaler_path or os.getenv("BOT_SCALER_PATH")
        if self.model_path:
            self._load_model()

    def _load_model(self) -> None:
        try:
            import joblib
        except ImportError:
            return

        if not self.model_path or not os.path.exists(self.model_path):
            return

        self.model = joblib.load(self.model_path)
        if self.scaler_path and os.path.exists(self.scaler_path):
            self.scaler = joblib.load(self.scaler_path)

    def extract_features(self, follower: Dict, user_info: Optional[Dict] = None) -> FollowerFeatures:
        username = str(follower.get("username", "") or "")
        bio = str(follower.get("biography", "") or "")
        follower_count = self._as_int(follower.get("follower_count"))
        following_count = self._as_int(follower.get("following_count"))
        media_count = self._as_int(follower.get("media_count"))
        denominator = max(follower_count, 1)
        ratio = following_count / denominator
        digits = sum(1 for char in username if char.isdigit())
        username_digit_ratio = digits / len(username) if username else 0.0
        generic_terms = sum(1 for term in GENERIC_BIO_TERMS if term in bio.lower())

        return FollowerFeatures(
            follower_count=follower_count,
            following_count=following_count,
            media_count=media_count,
            following_to_follower_ratio=ratio,
            bio_length=len(bio.strip()),
            generic_bio_terms=generic_terms,
            has_profile_picture=bool(follower.get("profile_pic_url")),
            is_private=bool(follower.get("is_private")),
            username_digit_ratio=username_digit_ratio,
        )

    def analyze_follower(self, follower: Dict, user_info: Optional[Dict] = None) -> Tuple[float, str]:
        features = self.extract_features(follower, user_info)

        if self.model is not None:
            probability = self._model_probability(features)
        else:
            probability = self._heuristic_probability(features)

        if probability >= 70:
            label = "bot"
        elif probability >= 35:
            label = "suspicious"
        else:
            label = "real"
        return round(probability, 2), label

    def sentiment_score(self, text: str) -> float:
        """Return a lightweight 0..1 bio quality score.

        This is intentionally not a full sentiment model. It gives the analyzer
        a stable signal without downloading external model weights at import
        time.
        """

        words = set(re.findall(r"[a-zA-Z]+", (text or "").lower()))
        if not words:
            return 0.5

        positive_hits = len(words & POSITIVE_WORDS)
        negative_hits = len(words & NEGATIVE_WORDS)
        score = 0.5 + (positive_hits * 0.08) - (negative_hits * 0.12)
        return round(min(max(score, 0.0), 1.0), 3)

    def _model_probability(self, features: FollowerFeatures) -> float:
        vector = [[
            features.follower_count,
            features.following_count,
            features.media_count,
            features.following_to_follower_ratio,
            features.bio_length,
            features.generic_bio_terms,
            int(features.has_profile_picture),
            int(features.is_private),
            features.username_digit_ratio,
        ]]
        if self.scaler is not None:
            vector = self.scaler.transform(vector)

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(vector)[0]
            return float(probabilities[-1] * 100)

        prediction = self.model.predict(vector)[0]
        return 100.0 if int(prediction) == 1 else 0.0

    @staticmethod
    def _heuristic_probability(features: FollowerFeatures) -> float:
        score = 8.0

        if features.following_to_follower_ratio >= 10:
            score += 30
        elif features.following_to_follower_ratio >= 5:
            score += 22
        elif features.following_to_follower_ratio >= 2.5:
            score += 12

        if features.follower_count < 25 and features.following_count > 250:
            score += 18
        elif features.follower_count < 100 and features.following_count > 800:
            score += 14

        if features.media_count == 0 and features.follower_count < 150:
            score += 12

        if not features.has_profile_picture:
            score += 14

        if features.bio_length == 0:
            score += 7
        elif features.bio_length > 35:
            score -= 4

        score += min(features.generic_bio_terms * 9, 24)

        if features.username_digit_ratio >= 0.45:
            score += 12
        elif features.username_digit_ratio >= 0.3:
            score += 6

        if features.is_private:
            score -= 3

        if features.follower_count > 500 and features.has_profile_picture and features.bio_length > 20:
            score -= 10

        return min(max(score, 0.0), 100.0)

    @staticmethod
    def _as_int(value) -> int:
        try:
            if value is None:
                return 0
            return max(int(value), 0)
        except (TypeError, ValueError):
            return 0
