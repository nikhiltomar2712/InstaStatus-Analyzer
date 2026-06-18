from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from src import __version__
from src.analyzer import AccountAnalyzer
from src.auth import AuthManager
from src.exporter import export_csv, export_json, export_pdf
from src.fetcher import InstagramFetcher
from src.sample_data import build_demo_account


app = typer.Typer(help="Analyze Instagram account engagement and follower quality.")
console = Console()


@app.command()
def analyze(
    username: str = typer.Argument(..., help="Instagram username to analyze."),
    export: Optional[str] = typer.Option(
        None,
        "--export",
        "-e",
        help="Export format: csv, json, or pdf.",
    ),
    followers: int = typer.Option(50, "--followers", "-f", min=0, help="Followers to sample."),
    posts: int = typer.Option(12, "--posts", "-p", min=0, help="Recent posts to analyze."),
    demo: bool = typer.Option(False, "--demo", help="Use deterministic demo data."),
    output_dir: Path = typer.Option(Path("exports"), "--output-dir", help="Directory for exports."),
) -> None:
    """Analyze an Instagram account and print a compact report."""

    data = _load_account_data(username, followers, posts, demo)
    analyzer = AccountAnalyzer()

    with console.status(f"Analyzing {username}..."):
        result = analyzer.analyze(data)

    _print_summary(result)

    if export:
        path = _export_result(result, export.lower(), output_dir)
        console.print(f"[green]Exported {export.lower()} report to {path}[/green]")


@app.command()
def version() -> None:
    """Print the installed package version."""

    console.print(__version__)


def _load_account_data(username: str, followers: int, posts: int, demo: bool) -> dict:
    if demo:
        return build_demo_account(username, followers, posts)

    auth = AuthManager()
    try:
        client = auth.login()
    except Exception as exc:
        console.print(f"[yellow]Live Instagram login unavailable: {exc}[/yellow]")
        console.print("[yellow]Using demo data. Add credentials to .env for live analysis.[/yellow]")
        return build_demo_account(username, followers, posts)

    fetcher = InstagramFetcher(client)
    return fetcher.fetch_account_data(username, followers_amount=followers, posts_amount=posts)


def _print_summary(result: dict) -> None:
    user = result["user_info"]
    engagement = result["engagement"]
    quality = result["follower_quality"]
    content = result["content_summary"]

    table = Table(title=f"Account Analysis: @{user.get('username', 'unknown')}")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_row("Followers", str(user.get("follower_count", 0)))
    table.add_row("Following", str(user.get("following_count", 0)))
    table.add_row("Posts Analyzed", str(content["posts_analyzed"]))
    table.add_row("Engagement Rate", f"{engagement['engagement_rate_percent']}%")
    table.add_row("Real Followers", str(quality["real_count"]))
    table.add_row("Suspicious Followers", str(quality["suspicious_count"]))
    table.add_row("Bot Followers", str(quality["bot_count"]))
    table.add_row("Risk Level", quality["risk_level"].title())
    console.print(table)


def _export_result(result: dict, export_format: str, output_dir: Path) -> str:
    if export_format == "csv":
        return export_csv(result["follower_details"], output_dir=output_dir)
    if export_format == "json":
        return export_json(result, output_dir=output_dir)
    if export_format == "pdf":
        return export_pdf(result, output_dir=output_dir)
    raise typer.BadParameter("Export format must be one of: csv, json, pdf.")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
