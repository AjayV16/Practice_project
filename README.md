# 🎓 Video Learning Assistant

A ChatGPT-style educational assistant that lets you **upload any video and ask questions about its content** — powered by OpenAI and VideoDB.

## 🚀 Features

- Upload video files or use video URLs (YouTube, etc.)
- Auto-indexes transcripts and scenes using VideoDB
- Ask natural language questions and get smart summaries from the transcript
- Built with **Streamlit** for easy deployment

## 📁 Folder Structure

├── app.py # Streamlit UI
├── config.py # Settings and keys
├── run.py # Setup + launch script
├── requirements.txt
└── utils/
├── videodb_client.py
└── openai_service.py

## 🧪 How to Run
> Make sure you have Python 3.8+

1. Clone this repo:
```bash
git clone https://github.com/AjayV16/Practice_project.git
cd Practice_project
Create virtual environment:
python -m venv .venv
.\.venv\Scripts\activate   # For Windows

Install dependencies:
pip install -r requirements.txt

Create a .env file in root directory:
VIDEODB_API_KEY=your_videodb_key_here
OPENAI_API_KEY=your_openai_key_here

Run the app:
python run.py
