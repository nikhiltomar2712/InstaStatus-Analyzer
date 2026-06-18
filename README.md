# InstaStatus-Analyzer

Instagram account intelligence for engagement metrics, follower-quality scoring,
demo analysis, exports, a Streamlit dashboard, and a FastAPI service.

> This project uses unofficial Instagram tooling when live mode is enabled. Use
> it responsibly, respect rate limits, and only analyze accounts you are allowed
> to inspect.

## What It Does

- Scores sampled followers as `real`, `suspicious`, or `bot`.
- Calculates average likes, comments, engagement rate, reel/video views, and top posts.
- Runs without credentials in deterministic demo mode.
- Exports reports as CSV, JSON, and optional PDF.
- Provides a Typer CLI, Streamlit dashboard, FastAPI API, Docker setup, and CI.
- Supports optional saved sklearn-style bot models through `BOT_MODEL_PATH`.

## Project Layout

```text
src/
  analyzer.py       Core metrics and report generation
  bot_detector.py   Lightweight bot scoring with optional ML model loading
  sample_data.py    Deterministic demo account data
  auth.py           Optional Instagrapi login/session handling
  fetcher.py        Live Instagram data fetching
  exporter.py       CSV, JSON, and PDF exports
  cli.py            Command-line interface
  dashboard.py      Streamlit app
  api.py            FastAPI app
scripts/
  batch_analysis.py Batch JSON report generation
tests/
  test_*.py         Unit tests for the lightweight core
```

## Setup

```bash
git clone https://github.com/nikhiltomar2712/InstaStatus-Analyzer.git
cd InstaStatus-Analyzer
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

For the full local app stack:

```bash
python -m pip install -r requirements.txt
```

Optional live Instagram access:

```bash
cp .env.example .env
# Fill INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env
```

## CLI

Demo mode works without Instagram credentials:

```bash
python -m src.cli analyze instagram --demo --followers 50 --posts 12 --export json
```

Live mode uses `.env` credentials and falls back to demo data if login is not available:

```bash
python -m src.cli analyze instagram --followers 100 --posts 12 --export csv
```

## Dashboard

```bash
streamlit run src/dashboard.py
```

Open `http://localhost:8501`.

## API

```bash
uvicorn src.api:app --reload
```

Useful endpoints:

- `GET /health`
- `GET /demo/{username}`
- `POST /analyze`

Example:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"username":"instagram","followers_amount":50,"posts_amount":12,"demo":true}'
```

## Batch Analysis

Create a file with one username per line, then run:

```bash
python scripts/batch_analysis.py accounts.txt --demo --output-dir exports
```

## Docker

```bash
docker compose up --build
```

- Dashboard: `http://localhost:8501`
- API docs: `http://localhost:8000/docs`

## Exports

Reports are written to `exports/` by default:

- CSV follower sample report
- JSON full analysis report
- PDF summary report when `reportlab` is installed

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

The test suite intentionally avoids live Instagram calls and external ML model
downloads.

## Environment Variables

See `.env.example` for all options.

- `INSTAGRAM_USERNAME` and `INSTAGRAM_PASSWORD`: optional live-mode credentials
- `SESSION_DIR`: where Instagrapi sessions are stored
- `RATE_LIMIT_DELAY`: seconds to sleep before live fetch calls
- `BOT_MODEL_PATH` and `BOT_SCALER_PATH`: optional saved ML model files

## License

MIT
