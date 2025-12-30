# 📈 LangChain Financial Agent

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-v0.3-green)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![GitHub Actions](https://img.shields.io/badge/Deployment-GitHub%20Actions-black)

An automated AI agent that acts as a financial research assistant. It autonomously retrieves real-time spot prices for Gold and Silver (International USD & Shanghai SGE CNY), analyzes market news, and delivers a professional HTML report via email every day.

## 🚀 Key Features

* **Multi-Market Data Retrieval**: Fetches real-time data for both International (XAU/USD) and Chinese (Au99.99/CNY) markets using Tavily Search API.
* **AI-Powered Analysis**: Uses **Google Gemini** to synthesize data and generate "Wall Street style" market trend reports in Chinese.
* **Automated Workflow**: Fully serverless deployment using **GitHub Actions** (Cron Schedule).
* **Professional Reporting**: Renders Markdown analysis into styled HTML emails and distributes them via SMTP.

## 🛠️ Tech Stack

* **Core Framework**: LangChain (Python)
* **LLM**: Google Gemini (via `langchain-google-genai`)
* **Search Tool**: Tavily AI
* **Automation**: GitHub Actions (Daily Cron)
* **Notification**: SMTP (Gmail App Password)
<img width="1415" height="870" alt="image" src="https://github.com/user-attachments/assets/ec1e6b7b-0c6a-4558-80f4-7ed94628ccc3" />

## 📦 How to Run

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Setup `.env` file with your API Keys
4. Run: `python agent.py`
