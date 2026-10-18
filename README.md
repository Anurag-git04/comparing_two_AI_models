# ⚡ LLM Model Benchmark & Latency Comparison

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/Groq-API-f55036.svg?logo=fastapi&logoColor=white)](https://groq.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini_API-4285F4.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lightweight, streaming-based benchmarking tool to evaluate and compare large language models (LLMs) across different inference providers (**Groq** and **Google Gemini**) side-by-side using identical prompts.

The script logs real-time streaming metrics including **Time to First Token (TTFT)**, **End-to-End Latency**, **Token Counts**, and **Generation Throughput (Tokens/sec)**, printing a formatted CLI comparison table and auto-generating an updated `results.md` report.

---

## 📊 Key Metrics Tracked

| Metric | Description |
| :--- | :--- |
| **TTFT (s)** | Time to First Token — duration from request initiation until the first token stream chunk arrives. |
| **Latency (s)** | Total turnaround time until the entire completion response has finished streaming. |
| **In / Out / Total Tok** | Prompt tokens, generated tokens (including reasoning/thinking tokens), and combined count. |
| **Out tok/s** | Effective generation speed: `out_tokens / (latency - ttft)`. |
| **Retry & Resilience** | Built-in exponential backoff retry mechanism handling transient `503 Service Unavailable` errors. |

---

## 📈 Sample Benchmark Output

Running against prompt: *"Explain how a hash map works in about 150 words."*

| Provider | Model | TTFT (s) | Latency (s) | In tok | Out tok | Total tok | Out tok/s |
|---|---|---|---|---|---|---|---|
| **Groq** | `openai/gpt-oss-120b` | 0.999 | 1.532 | 83 | 290 | 373 | 544.2 |
| **Groq** | `openai/gpt-oss-20b` | 0.197 | 0.464 | 83 | 308 | 391 | 1150.7 |
| **Gemini** | `gemini-3.8-flash` | 14.760 | 14.768 | 15 | 568 | 583 | 73,399.2* |

> *Note: Output tokens and speed for Gemini models reflect stream chunk processing and thinking token accounting based on the `google-genai` SDK response metadata.*

---

## 📁 Repository Structure

```text
AI-Practice/
├── .env.example        # Template for required API keys (safe for Git)
├── .gitignore          # Ignores .env secrets, virtualenvs, caches & IDE files
├── compare_models.py   # Benchmark runner with streaming & retry logic
├── requirements.txt    # Project dependencies
├── results.md          # Generated table & complete model responses
└── README.md           # Documentation & setup guide
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- [Groq API Key](https://console.groq.com/keys)
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 2. Clone the Repository
```bash
git clone https://github.com/<your-username>/AI-Practice.git
cd AI-Practice
```

### 3. Set Up a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure API Keys
Copy the example environment file:
```bash
cp .env.example .env
```
*(On Windows PowerShell, use: `Copy-Item .env.example .env`)*

Edit `.env` and fill in your keys:
```env
GROQ_API_KEY="your_groq_api_key_here"
GEMINI_API_KEY="your_gemini_api_key_here"
```

> ⚠️ **Security Warning**: The `.env` file contains your private API keys and is excluded by `.gitignore`. Never commit `.env` to GitHub.

---

## 💻 Usage

### Run with the Default Prompt
```bash
python compare_models.py
```
*Default prompt: "Explain how a hash map works in about 150 words."*

### Run with a Custom Prompt
Pass any prompt enclosed in quotes as a CLI argument:
```bash
python compare_models.py "Explain quantum computing in simple terms for a 10 year old."
```

### View Results
After execution:
1. The comparison summary table is displayed in the terminal.
2. The full output table and model text responses are automatically saved to [results.md](results.md).

---

## ⚙️ Customizing Models

You can change which models are benchmarked directly in [`compare_models.py`](compare_models.py):

```python
# Select Groq models
GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    # "llama-3.3-70b-versatile",
]

# Select Gemini model
GEMINI_MODEL = "gemini-3.8-flash"
```

---

## 📤 Pushing to GitHub

Follow these steps to initialize and push this repository to GitHub:

```bash
# 1. Initialize git repository (if not already done)
git init

# 2. Stage files
git add .

# 3. Verify staged files (CRITICAL: ensure .env and .venv are NOT listed!)
git status

# 4. Commit files
git commit -m "feat: setup LLM streaming benchmark and model comparison"

# 5. Rename branch to main
git branch -M main

# 6. Add your GitHub remote repository
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# 7. Push to GitHub
git push -u origin main
```

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).
