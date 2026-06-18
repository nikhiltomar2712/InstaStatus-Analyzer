import argparse
import time
from pathlib import Path

from src.analyzer import AccountAnalyzer
from src.auth import AuthManager
from src.exporter import export_json
from src.fetcher import InstagramFetcher
from src.sample_data import build_demo_account


def main() -> None:
    args = parse_args()
    input_file = args.input_option or args.input_file
    if not input_file:
        raise SystemExit("Usage: python scripts/batch_analysis.py accounts.txt")

    usernames = read_usernames(Path(input_file))
    analyzer = AccountAnalyzer()
    fetcher = None

    if not args.demo:
        try:
            fetcher = InstagramFetcher(AuthManager().login())
        except Exception as exc:
            print(f"Live Instagram login unavailable: {exc}")
            print("Using demo data for this batch.")

    for username in usernames:
        print(f"Analyzing {username}...")
        try:
            if fetcher:
                data = fetcher.fetch_account_data(
                    username,
                    followers_amount=args.followers,
                    posts_amount=args.posts,
                )
            else:
                data = build_demo_account(username, args.followers, args.posts)

            result = analyzer.analyze(data)
            path = export_json(result, f"{username}_report.json", output_dir=args.output_dir)
            print(f"Saved {path}")
            if args.delay:
                time.sleep(args.delay)
        except Exception as exc:
            print(f"Failed for {username}: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run InstaStatus analysis for many accounts.")
    parser.add_argument("input_file", nargs="?", help="Text file with one username per line.")
    parser.add_argument("--input", dest="input_option", help="Text file with one username per line.")
    parser.add_argument("--followers", type=int, default=50, help="Followers to sample per account.")
    parser.add_argument("--posts", type=int, default=12, help="Recent posts to analyze per account.")
    parser.add_argument("--output-dir", default="exports", help="Directory for JSON reports.")
    parser.add_argument("--delay", type=float, default=0, help="Seconds to wait between accounts.")
    parser.add_argument("--demo", action="store_true", help="Use deterministic demo data.")
    return parser.parse_args()


def read_usernames(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as handle:
        return [line.strip().lstrip("@") for line in handle if line.strip()]


if __name__ == "__main__":
    main()
