import csv
import json
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from typing import Dict, List

def export_csv(follower_details: List[Dict], filename: str = "followers_report.csv"):
    if not follower_details:
        print("No data to export.")
        return
    os.makedirs("exports", exist_ok=True)
    path = os.path.join("exports", filename)
    keys = follower_details[0].keys()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(follower_details)
    print(f"CSV exported to {path}")

def export_json(analysis_result: Dict, filename: str = "analysis_report.json"):
    os.makedirs("exports", exist_ok=True)
    path = os.path.join("exports", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis_result, f, indent=2, default=str)
    print(f"JSON exported to {path}")

def export_pdf(analysis_result: Dict, filename: str = "report.pdf"):
    os.makedirs("exports", exist_ok=True)
    path = os.path.join("exports", filename)
    doc = SimpleDocTemplate(path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    info = analysis_result["user_info"]
    eng = analysis_result["engagement"]
    fq = analysis_result["follower_quality"]

    story.append(Paragraph("Instagram Account Analysis Report", styles['Title']))
    story.append(Spacer(1, 12))

    # User Info
    story.append(Paragraph("Account Info", styles['Heading1']))
    user_text = f"Username: {info['username']}<br/>Bio: {info['biography']}<br/>Followers: {info['follower_count']}<br/>Following: {info['following_count']}"
    story.append(Paragraph(user_text, styles['Normal']))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Engagement", styles['Heading1']))
    eng_text = f"Engagement Rate: {eng['engagement_rate_percent']}%<br/>Avg Likes: {eng['avg_likes']:.1f}<br/>Total Likes (recent): {eng['total_likes_last_posts']}"
    story.append(Paragraph(eng_text, styles['Normal']))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Follower Quality", styles['Heading1']))
    fq_text = f"Real: {fq['real_count']} ({fq['percent_real']}%)<br/>Suspicious: {fq['suspicious_count']}<br/>Bots: {fq['bot_count']} ({fq['percent_bot']}%)"
    story.append(Paragraph(fq_text, styles['Normal']))

    # Table for top posts
    story.append(Spacer(1, 12))
    story.append(Paragraph("Top Posts", styles['Heading1']))
    top_posts = analysis_result.get("top_posts", [])
    if top_posts:
        data = [["Code", "Likes", "Comments", "Type"]]
        for p in top_posts[:5]:
            data.append([p['code'], p['like_count'], p['comment_count'], p['media_type']])
        t = Table(data)
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                               ('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
        story.append(t)

    doc.build(story)
    print(f"PDF exported to {path}")
