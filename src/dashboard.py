import streamlit as st
import pandas as pd
from src.auth import AuthManager
from src.fetcher import InstagramFetcher
from src.analyzer import AccountAnalyzer
from src.exporter import export_csv, export_json, export_pdf
import plotly.express as px

st.set_page_config(page_title="InstaStatus Analyzer", layout="wide")

st.title("📊 InstaStatus Analyzer")
username = st.text_input("Enter Instagram username (public):")

if st.button("Analyze"):
    with st.spinner("Fetching data..."):
        auth = AuthManager()
        client = auth.login() if auth.username else None
        fetcher = InstagramFetcher(client) if client else InstagramFetcher(None)
        analyzer = AccountAnalyzer()

        # For public demo we use dummy data if no login
        if client:
            data = fetcher.fetch_account_data(username, followers_amount=50, posts_amount=12)
        else:
            st.warning("No login credentials. Using demo data.")
            data = {
                "user_info": {"username": username, "follower_count": 1000, "following_count": 500, "biography": "Demo"},
                "followers": [{"username": f"user{i}", "biography": "", "follower_count": 100, "following_count": 1000, "is_private": False, "profile_pic_url": ""} for i in range(50)],
                "posts": [{"like_count": i*10, "comment_count": i, "code": "xyz", "media_type":1, "view_count":0} for i in range(1,13)]
            }
        result = analyzer.analyze(data)

    # Display
    col1, col2, col3 = st.columns(3)
    col1.metric("Real Followers", result["follower_quality"]["real_count"])
    col2.metric("Suspicious", result["follower_quality"]["suspicious_count"])
    col3.metric("Bots", result["follower_quality"]["bot_count"])

    st.subheader("Engagement")
    st.write(f"Engagement Rate: {result['engagement']['engagement_rate_percent']}%")

    # Pie chart
    labels = ['Real','Suspicious','Bot']
    values = [result["follower_quality"]["real_count"],
              result["follower_quality"]["suspicious_count"],
              result["follower_quality"]["bot_count"]]
    fig = px.pie(names=labels, values=values, title="Follower Distribution")
    st.plotly_chart(fig)

    # Top posts
    st.subheader("Top Posts")
    st.table(pd.DataFrame(result["top_posts"]))

    # Export
    if st.button("Export CSV"):
        export_csv(result["follower_details"])
        st.success("CSV exported to exports/ folder")
    if st.button("Export JSON"):
        export_json(result)
        st.success("JSON exported")
    if st.button("Export PDF"):
        export_pdf(result)
        st.success("PDF exported")
