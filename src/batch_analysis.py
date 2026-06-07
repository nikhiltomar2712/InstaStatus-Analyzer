import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.auth import AuthManager
from src.fetcher import InstagramFetcher
from src.analyzer import AccountAnalyzer
from src.exporter import export_json
import time

def main(input_file: str):
    with open(input_file, 'r') as f:
        usernames = [line.strip() for line in f if line.strip()]

    auth = AuthManager()
    client = auth.login()
    fetcher = InstagramFetcher(client)
    analyzer = AccountAnalyzer()

    for username in usernames:
        print(f"Analyzing {username}...")
        try:
            data = fetcher.fetch_account_data(username, followers_amount=30)
            result = analyzer.analyze(data)
            export_json(result, f"{username}_report.json")
            time.sleep(10)
        except Exception as e:
            print(f"Failed for {username}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_analysis.py accounts.txt")
        sys.exit(1)
    main(sys.argv[1])
