from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.analyzer import AccountAnalyzer
from src.auth import AuthManager
from src.fetcher import InstagramFetcher
from src.sample_data import build_demo_account


app = FastAPI(
    title="InstaStatus Analyzer API",
    version="0.2.0",
    description="Instagram engagement and follower-quality analysis.",
)


class AnalyzeRequest(BaseModel):
    username: str = Field(..., min_length=1, examples=["instagram"])
    followers_amount: int = Field(50, ge=0, le=1000)
    posts_amount: int = Field(12, ge=0, le=100)
    demo: bool = True


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/demo/{username}")
def demo_analysis(username: str, followers_amount: int = 50, posts_amount: int = 12) -> dict:
    data = build_demo_account(username, followers_amount, posts_amount)
    return AccountAnalyzer().analyze(data)


@app.post("/analyze")
def analyze_account(request: AnalyzeRequest) -> dict:
    if request.demo:
        data = build_demo_account(request.username, request.followers_amount, request.posts_amount)
        return AccountAnalyzer().analyze(data)

    try:
        client = AuthManager().login()
        fetcher = InstagramFetcher(client)
        data = fetcher.fetch_account_data(
            request.username,
            followers_amount=request.followers_amount,
            posts_amount=request.posts_amount,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return AccountAnalyzer().analyze(data)
