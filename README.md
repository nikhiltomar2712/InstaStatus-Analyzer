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
