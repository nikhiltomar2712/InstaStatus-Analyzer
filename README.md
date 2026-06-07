# 📊 InstaStatus-Analyzer

**Comprehensive Instagram account analysis: real vs bot followers, engagement metrics, content performance, and more.**

[![Stars](https://img.shields.io/github/stars/nikhiltomar2712/InstaStatus-Analyzer?style=social)](https://github.com/nikhiltomar2712/InstaStatus-Analyzer)
[![Forks](https://img.shields.io/github/forks/nikhiltomar2712/InstaStatus-Analyzer?style=social)](https://github.com/nikhiltomar2712/InstaStatus-Analyzer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Features

- 🔍 **Real vs Fake Follower Detection** – hybrid model (heuristic + ML) flags bots, mass followers, and suspicious accounts.
- 📈 **Engagement Breakdown** – like count, comments quality, reel/story views (if public).
- 📋 **Follower Export** – full list with usernames, bios, verification status, follower counts (CSV/JSON/PDF).
- 🧠 **Bot Detection** – low engagement, generic bios, high following/follower ratio, comment sentiment (Hugging Face), posting patterns.
- 🖥️ **Multiple Interfaces**:
  - **CLI** (Rich + Typer) for power users
  - **Web Dashboard** (Streamlit) for interactive exploration
  - **REST API** (FastAPI – optional) for integration
- 🐳 **Docker support** – ready to deploy anywhere.
- 🔐 **Multi‑account & proxy support** – rotate IPs and manage sessions.
- ⏱️ **Rate limiting** – respects Instagram’s limits automatically.
- 📦 **Portable** – Python 3.10+, `pip` or `poetry`.

---

## ⚠️ Disclaimer

This tool uses **unofficial** APIs (Instagrapi) and public data scraping.  
**It may violate Instagram’s Terms of Service**. Use at your own risk.  
Always respect rate limits, obtain consent when analyzing non‑public data, and do not use for spam or harassment.

---

## 📥 Installation

### Prerequisites
- Python 3.10+
- Git
- (Optional) Docker

### Using pip

```bash
git clone https://github.com/nikhiltomar2712/InstaStatus-Analyzer.git
cd InstaStatus-Analyzer
python -m venv venv

source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
```
bash

poetry install
```

Environment Variables
Copy .env.example to .env and fill in your credentials (optional for public data only).
```
🧪 Quick Start
CLI
bash
# Analyze any public account
python -m src.cli analyze --username "instagram" --export csv
```
# Batch analysis
python scripts/batch_analysis.py --input accounts.txt
Streamlit Dashboard
bash
streamlit run src/dashboard.py
Open http://localhost:8501

FastAPI (optional)
bash
uvicorn src.api:app --reload
Docs at http://localhost:8000/docs

🧠 Bot Detection Logic
We combine rule‑based heuristics and a scikit‑learn RandomForest classifier (trained on manually labeled datasets). Features include:

Engagement rate (likes / followers)

Follower / following ratio

Bio length & presence of keywords (generic)

Comment sentiment (Hugging Face distilbert-base-uncased-finetuned-sst-2-english)

Account age & post frequency

Profile picture presence

Output: Confidence score (0–100%) and a “bot / suspicious / real” label.

📁 Export Formats
csv – full follower list with metadata

json – structured for API consumption

pdf – professional report (via ReportLab)

🐳 Docker
bash
docker-compose up --build
Streamlit dashboard will be available at http://localhost:8501.

🧩 Architecture
text
src/
├── auth.py          # Instagrapi session handling, multi‑account
├── fetcher.py       # Data collection (followers, posts, stories)
├── analyzer.py      # Metrics calculation, growth trends
├── bot_detector.py  # ML / rule‑based bot detection
├── exporter.py      # CSV, JSON, PDF generation
├── dashboard.py     # Streamlit web app
├── cli.py           # Typer CLI
├── api.py           # FastAPI (optional)
├── rate_limiter.py  # Decorator for API calls
└── utils.py         # Helpers, proxy, logging
🤝 Contributing
Pull requests are welcome! Please read CONTRIBUTING.md first.

📄 License
MIT © [Nikhil Tomar]

text

---

## 2. `requirements.txt`
instagrapi>=2.0.0
selenium>=4.15.0
rich>=13.0.0
typer>=0.9.0
streamlit>=1.28.0
gradio>=4.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
scikit-learn>=1.3.0
transformers>=4.35.0
torch>=2.1.0
pandas>=2.1.0
reportlab>=4.0.0
python-dotenv>=1.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
webdriver-manager>=4.0.0
pytest>=7.4.0
pytest-mock>=3.12.0

text

---

## 3. `pyproject.toml`

```toml
[tool.poetry]
name = "instastatus-analyzer"
version = "0.1.0"
description = "Instagram Account Intelligence – real vs bot followers, engagement, exports."
authors = ["Nikhil Tomar <nikhiltomarsan@gmail.com.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"
instagrapi = "^2.0.0"
selenium = "^4.15.0"
rich = "^13.0.0"
typer = "^0.9.0"
streamlit = "^1.28.0"
gradio = "^4.0.0"
fastapi = "^0.104.0"
uvicorn = "^0.24.0"
scikit-learn = "^1.3.0"
transformers = "^4.35.0"
torch = "^2.1.0"
pandas = "^2.1.0"
reportlab = "^4.0.0"
python-dotenv = "^1.0.0"
requests = "^2.31.0"
beautifulsoup4 = "^4.12.0"
webdriver-manager = "^4.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-mock = "^3.12.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
