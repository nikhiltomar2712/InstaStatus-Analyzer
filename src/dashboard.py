import pandas as pd
import plotly.express as px
import streamlit as st

from src.analyzer import AccountAnalyzer
from src.auth import AuthManager
from src.exporter import export_csv, export_json, export_pdf
from src.fetcher import InstagramFetcher
from src.sample_data import build_demo_account


st.set_page_config(page_title="InstaStatus Analyzer", layout="wide")
st.title("InstaStatus Analyzer")

with st.sidebar:
    username = st.text_input("Instagram username", value="instagram")
    followers_amount = st.slider("Followers to sample", min_value=0, max_value=500, value=50, step=10)
    posts_amount = st.slider("Posts to analyze", min_value=0, max_value=50, value=12, step=1)
    demo_mode = st.toggle("Demo mode", value=True)
    analyze_clicked = st.button("Analyze", type="primary")


def load_data():
    if demo_mode:
        return build_demo_account(username, followers_amount, posts_amount)

    auth = AuthManager()
    client = auth.login()
    fetcher = InstagramFetcher(client)
    return fetcher.fetch_account_data(username, followers_amount=followers_amount, posts_amount=posts_amount)


if analyze_clicked:
    if not username.strip():
        st.warning("Enter a username to analyze.")
        st.stop()

    try:
        with st.spinner("Analyzing account..."):
            data = load_data()
            st.session_state.analysis_result = AccountAnalyzer().analyze(data)
    except Exception as exc:
        st.error(f"Unable to analyze account: {exc}")

result = st.session_state.get("analysis_result")
if not result:
    result = AccountAnalyzer().analyze(build_demo_account(username, followers_amount, posts_amount))

user = result["user_info"]
engagement = result["engagement"]
quality = result["follower_quality"]
content = result["content_summary"]

metric_columns = st.columns(5)
metric_columns[0].metric("Followers", f"{user.get('follower_count', 0):,}")
metric_columns[1].metric("Engagement", f"{engagement['engagement_rate_percent']}%")
metric_columns[2].metric("Real", quality["real_count"])
metric_columns[3].metric("Suspicious", quality["suspicious_count"])
metric_columns[4].metric("Bots", quality["bot_count"])

left, right = st.columns([1, 1])

with left:
    st.subheader("Follower Quality")
    distribution = pd.DataFrame(
        [
            {"Label": "Real", "Count": quality["real_count"]},
            {"Label": "Suspicious", "Count": quality["suspicious_count"]},
            {"Label": "Bot", "Count": quality["bot_count"]},
        ]
    )
    st.plotly_chart(px.pie(distribution, names="Label", values="Count"), use_container_width=True)

with right:
    st.subheader("Content Mix")
    mix = pd.DataFrame(
        [
            {"Type": "Photos", "Count": content["photos"]},
            {"Type": "Videos", "Count": content["videos"]},
            {"Type": "Carousels", "Count": content["carousels"]},
            {"Type": "Other", "Count": content["other"]},
        ]
    )
    st.plotly_chart(px.bar(mix, x="Type", y="Count"), use_container_width=True)

st.subheader("Top Posts")
st.dataframe(pd.DataFrame(result["top_posts"]), use_container_width=True)

st.subheader("Follower Sample")
st.dataframe(pd.DataFrame(result["follower_details"]), use_container_width=True)

export_columns = st.columns(3)
if export_columns[0].button("Export CSV"):
    st.success(f"Saved {export_csv(result['follower_details'])}")
if export_columns[1].button("Export JSON"):
    st.success(f"Saved {export_json(result)}")
if export_columns[2].button("Export PDF"):
    try:
        st.success(f"Saved {export_pdf(result)}")
    except RuntimeError as exc:
        st.error(str(exc))
