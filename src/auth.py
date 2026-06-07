import os
from instagrapi import Client
from dotenv import load_dotenv
from src.utils import logger

load_dotenv()

class AuthManager:
    def __init__(self):
        self.client = Client()
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.session_dir = os.getenv("SESSION_DIR", "./sessions")
        os.makedirs(self.session_dir, exist_ok=True)

    def login(self) -> Client:
        session_file = os.path.join(self.session_dir, f"{self.username}.session")
        if os.path.exists(session_file):
            try:
                self.client.load_settings(session_file)
                self.client.login(self.username, self.password)
                logger.info("Logged in using saved session.")
                return self.client
            except Exception as e:
                logger.warning(f"Session invalid: {e}")
        if not self.username or not self.password:
            raise ValueError("Missing credentials. Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env")
        self.client.login(self.username, self.password)
        self.client.dump_settings(session_file)
        logger.info("New login successful, session saved.")
        return self.client

    def logout(self):
        self.client.logout()
        logger.info("Logged out.")
