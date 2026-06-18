import os
from typing import Callable, Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    from instagrapi import Client
except ImportError:
    Client = None

from src.utils import logger


if load_dotenv:
    load_dotenv()


class AuthManager:
    def __init__(self, client_factory: Optional[Callable] = None):
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.session_dir = os.getenv("SESSION_DIR", "./sessions")
        os.makedirs(self.session_dir, exist_ok=True)

        if client_factory:
            self.client = client_factory()
        elif Client is not None:
            self.client = Client()
        else:
            self.client = None

    def login(self):
        if self.client is None:
            raise RuntimeError("Instagrapi is not installed. Install the instagram extra to use live data.")
        if not self.username or not self.password:
            raise ValueError("Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env to use live data.")

        session_file = os.path.join(self.session_dir, f"{self.username}.session")
        if os.path.exists(session_file):
            try:
                self.client.load_settings(session_file)
                self.client.login(self.username, self.password)
                logger.info("Logged in using saved Instagram session.")
                return self.client
            except Exception as exc:
                logger.warning("Saved Instagram session is invalid: %s", exc)

        self.client.login(self.username, self.password)
        self.client.dump_settings(session_file)
        logger.info("New Instagram login successful; session saved.")
        return self.client

    def logout(self) -> None:
        if self.client is not None:
            self.client.logout()
            logger.info("Logged out.")
