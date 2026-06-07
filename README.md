# 📊 InstaStatus-Analyzer

**Comprehensive Instagram account analysis: real vs bot followers, engagement metrics, content performance, and more.**

[![Stars](https://img.shields.io/github/stars/yourusername/InstaStatus-Analyzer?style=social)](https://github.com/yourusername/InstaStatus-Analyzer)
[![Forks](https://img.shields.io/github/forks/yourusername/InstaStatus-Analyzer?style=social)](https://github.com/yourusername/InstaStatus-Analyzer)
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
git clone https://github.com/yourusername/InstaStatus-Analyzer.git
cd InstaStatus-Analyzer
python -m venv venv

source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

bash

poetry install

Environment Variables
Copy .env.example to .env and fill in your credentials (optional for public data only).

🧪 Quick Start
CLI
bash
# Analyze any public account
python -m src.cli analyze --username "instagram" --export csv

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

📸 Screenshots (describe)
CLI in action
https://docs/cli_screenshot.png

Streamlit Dashboard
https://docs/dashboard_screenshot.png

PDF Report example
https://docs/pdf_report.png

🐳 Docker
bash
docker-compose up --build
Streamlit dashboard will be available at http://localhost:8501.

