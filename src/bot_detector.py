import re
import numpy as np
from transformers import pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
from typing import List, Dict, Tuple
import joblib
import os

class BotDetector:
    def __init__(self):
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            tokenizer="distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.model = None
        self.scaler = StandardScaler()
        self._load_or_train_model()

    def _load_or_train_model(self):
        """Placeholder: load pre-trained model if exists, else train a dummy model."""
        if os.path.exists("bot_model.pkl"):
            self.model = joblib.load("bot_model.pkl")
            self.scaler = joblib.load("scaler.pkl")
        else:
            # Train a tiny dummy model (will be replaced by real training)
            X = np.array([
                [0.1, 0.2, 1, 0.5, 0],
                [0.8, 10, 0.1, 0.1, 1],
                [0.3, 1.5, 2, 0.3, 0],
                [0.6, 5, 0.2, 0.05, 1],
            ])
            y = np.array([0, 1, 0, 1])  # 0=real, 1=bot
            self.scaler.fit(X)
            X_scaled = self.scaler.transform(X)
            self.model = RandomForestClassifier(n_estimators=10, random_state=42)
            self.model.fit(X_scaled, y)

    def extract_features(self, follower: Dict, user_info: Dict) -> np.ndarray:
        bio = follower.get("biography", "")
        follower_count = follower.get("follower_count", 0) or 0
        following_count = follower.get("following_count", 0) or 0

        # Follower/following ratio
        if following_count > 0:
            ratio = follower_count / following_count
        else:
            ratio = 10  # high value if following=0

        # Bio length and generic indicators
        bio_len = len(bio)
        generic_words = ["follow", "model", "brand ambassador", "public figure"]
        generic_count = sum(1 for w in generic_words if w.lower() in bio.lower())

        # Profile pic presence (simple check based on URL, assuming None means no pic)
        has_pic = 1 if follower.get("profile_pic_url") else 0

        # Account privacy (private = less likely bot? but we include)
        is_private = 1 if follower.get("is_private") else 0

        return np.array([ratio, bio_len, generic_count, has_pic, is_private])

    def analyze_follower(self, follower: Dict, user_info: Dict) -> Tuple[float, str]:
        features = self.extract_features(follower, user_info)
        features_scaled = self.scaler.transform([features])
        prob = self.model.predict_proba(features_scaled)[0]
        bot_prob = prob[1] * 100  # probability of class 1 (bot)
        if bot_prob > 70:
            label = "bot"
        elif bot_prob > 30:
            label = "suspicious"
        else:
            label = "real"
        return bot_prob, label

    def sentiment_score(self, text: str) -> float:
        if not text or len(text) < 3:
            return 0.5  # neutral if no text
        result = self.sentiment_pipeline(text[:512])[0]  # truncate
        score = result['score'] if result['label'] == 'POSITIVE' else 1 - result['score']
        return score
