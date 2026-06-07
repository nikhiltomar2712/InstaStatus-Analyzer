import typer
from rich.console import Console
from rich.table import Table
from src.auth import AuthManager
from src.fetcher import InstagramFetcher
from src.analyzer import AccountAnalyzer
from src.exporter import export_csv, export_json

app = typer.Typer()
console = Console()

@app.command()
def analyze(
    username: str = typer.Argument(..., help="Instagram username to analyze"),
    export: str = typer.Option(None, help="Export format: csv or json")
):
    """Analyze an Instagram account and display stats."""
    auth = AuthManager()
    try:
        client = auth.login()
    except Exception:
        console.print("[yellow]No login credentials, using limited public data.[/yellow]")
        client = None

    fetcher = InstagramFetcher(client) if client else None
    analyzer = AccountAnalyzer()

    with console.status(f"Analyzing {username}..."):
        if client:
            data = fetcher.fetch_account_data(username, followers_amount=30)
        else:
            # demo data
            data = {
                "user_info": {"username": username, "follower_count": 1000, "following_count": 500, "biography": "Demo"},
                "followers": [{"username": f"user{i}", "biography": "", "follower_count": 100, "following_count": 1000, "is_private": False, "profile_pic_url": ""} for i in range(30)],
                "posts": [{"like_count": i*10, "comment_count": i, "code": "xyz", "media_type":1, "view_count":0} for i in range(1,13)]
            }
        result = analyzer.analyze(data)

    # Display using Rich
    table = Table(title="Account Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Username", result["user_info"]["username"])
    table.add_row("Engagement Rate", f"{result['engagement']['engagement_rate_percent']}%")
    table.add_row("Real Followers", str(result["follower_quality"]["real_count"]))
    table.add_row("Suspicious", str(result["follower_quality"]["suspicious_count"]))
    table.add_row("Bots", str(result["follower_quality"]["bot_count"]))
    console.print(table)

    if export == "csv":
        export_csv(result["follower_details"])
    elif export == "json":
        export_json(result)

if __name__ == "__main__":
    app()
