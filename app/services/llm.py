import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Use your Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "Your Key")
GEMINI_MODEL = "gemini-2.0-flash-lite"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

HEADERS = {"Content-Type": "application/json"}

def _post(payload):
    url = f"{API_URL}?key={GEMINI_API_KEY}"
    return requests.post(url, headers=HEADERS, json=payload, timeout=60)

def ask_llm(prompt: str, max_output_tokens: int = 256, temperature: float = 0.2) -> str:
    """
    Query Gemini API with simple retry logic.
    """
    if not GEMINI_API_KEY:
        return "LLM not configured: missing GEMINI_API_KEY."

    wrapped = (
        "You are a helpful personal finance assistant. "
        "Answer using only the provided data summary when possible. "
        "Be concise.\n\n"
        f"Instruction:\n{prompt}\n\nResponse:"
    )

    payload = {
        "contents": [{"parts": [{"text": wrapped}]}],
        "generationConfig": {
            "maxOutputTokens": max_output_tokens,
            "temperature": temperature,
        }
    }

    for attempt in range(4):
        resp = _post(payload)
        if resp.status_code == 200:
            try:
                data = resp.json()
                # Gemini returns candidates[0].content.parts[0].text
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            except Exception:
                return resp.text

        if resp.status_code in (503, 529):
            time.sleep(2 + attempt * 2)
            continue

        if resp.status_code in (401, 403):
            return f"Auth error from Gemini API ({resp.status_code}). Check your API key."

        return f"LLM error {resp.status_code}: {resp.text}"

    return "LLM is busy/loading. Please try again."

