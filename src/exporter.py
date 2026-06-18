import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List
from xml.sax.saxutils import escape


DEFAULT_EXPORT_DIR = Path("exports")
PREFERRED_CSV_FIELDS = (
    "username",
    "full_name",
    "bot_label",
    "bot_probability",
    "sentiment_score",
    "follower_count",
    "following_count",
    "media_count",
    "is_private",
    "profile_pic_url",
    "biography",
    "pk",
)


def export_csv(
    follower_details: List[Dict],
    filename: str = "followers_report.csv",
    output_dir: Path | str = DEFAULT_EXPORT_DIR,
) -> str:
    path = _resolve_path(filename, output_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = _fieldnames(follower_details)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(follower_details)

    return str(path)


def export_json(
    analysis_result: Dict,
    filename: str = "analysis_report.json",
    output_dir: Path | str = DEFAULT_EXPORT_DIR,
) -> str:
    path = _resolve_path(filename, output_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(analysis_result, handle, indent=2, ensure_ascii=False, default=str)
    return str(path)


def export_pdf(
    analysis_result: Dict,
    filename: str = "report.pdf",
    output_dir: Path | str = DEFAULT_EXPORT_DIR,
) -> str:
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError as exc:
        raise RuntimeError("Install the pdf extra to export PDF reports.") from exc

    path = _resolve_path(filename, output_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    info = analysis_result.get("user_info", {})
    engagement = analysis_result.get("engagement", {})
    quality = analysis_result.get("follower_quality", {})

    story.append(Paragraph("Instagram Account Analysis Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Account Info", styles["Heading1"]))
    story.append(
        Paragraph(
            "<br/>".join(
                [
                    f"Username: {escape(str(info.get('username', 'N/A')))}",
                    f"Bio: {escape(str(info.get('biography', '')))}",
                    f"Followers: {info.get('follower_count', 0)}",
                    f"Following: {info.get('following_count', 0)}",
                ]
            ),
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 12))
    story.append(Paragraph("Engagement", styles["Heading1"]))
    story.append(
        Paragraph(
            "<br/>".join(
                [
                    f"Engagement Rate: {engagement.get('engagement_rate_percent', 0)}%",
                    f"Avg Likes: {engagement.get('avg_likes', 0)}",
                    f"Avg Comments: {engagement.get('avg_comments', 0)}",
                    f"Total Likes: {engagement.get('total_likes_last_posts', 0)}",
                ]
            ),
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 12))
    story.append(Paragraph("Follower Quality", styles["Heading1"]))
    story.append(
        Paragraph(
            "<br/>".join(
                [
                    f"Risk Level: {escape(str(quality.get('risk_level', 'unknown')))}",
                    f"Real: {quality.get('real_count', 0)} ({quality.get('percent_real', 0)}%)",
                    f"Suspicious: {quality.get('suspicious_count', 0)}",
                    f"Bots: {quality.get('bot_count', 0)} ({quality.get('percent_bot', 0)}%)",
                ]
            ),
            styles["Normal"],
        )
    )

    top_posts = analysis_result.get("top_posts", [])
    if top_posts:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Top Posts", styles["Heading1"]))
        rows = [["Code", "Likes", "Comments", "Type", "Score"]]
        for post in top_posts[:5]:
            rows.append(
                [
                    escape(str(post.get("code", ""))),
                    post.get("like_count", 0),
                    post.get("comment_count", 0),
                    post.get("media_type", ""),
                    post.get("engagement_score", 0),
                ]
            )
        table = Table(rows)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
            )
        )
        story.append(table)

    document.build(story)
    return str(path)


def _resolve_path(filename: str, output_dir: Path | str) -> Path:
    path = Path(filename)
    if path.is_absolute() or path.parent != Path("."):
        return path
    return Path(output_dir) / path


def _fieldnames(rows: Iterable[Dict]) -> List[str]:
    discovered = []
    for row in rows:
        for key in row.keys():
            if key not in discovered:
                discovered.append(key)

    preferred = [field for field in PREFERRED_CSV_FIELDS if field in discovered]
    remaining = sorted(field for field in discovered if field not in preferred)
    return preferred + remaining
