# AI Yarn Defect Assistant

A Streamlit app that takes yarn testing counts (yarn count, thick places, thin
places, neps) and uses Gemini to explain likely causes, who to notify, and
what to check next.

## Setup

1. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Get a Gemini API key from https://aistudio.google.com/apikey
3. Copy `.env.example` to `.env` and paste your key in:
   ```
   cp .env.example .env
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```
5. Open the URL Streamlit prints (usually http://localhost:8501).

## Notes

- Never commit your `.env` file or share your API key - it's already in
  `.gitignore`.
- The `.streamlit/config.toml` file sets the app's color theme; it's part of
  the app, not a personal setting.
