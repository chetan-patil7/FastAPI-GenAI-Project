# main.py - Gemini API version: client initialized ONCE at startup
import time
from dotenv import load_dotenv
load_dotenv()  # load GEMINI_API_KEY from .env file

from fastapi import FastAPI, HTTPException
from models import load_text_model, generate_text

app = FastAPI()

# ✅ Initialize Gemini client ONCE when the server starts (not on every request)
gemini_client = load_text_model()
print("[startup] Gemini client ready.")


@app.get("/generate/text")
def serve_language_model_controller(prompt: str, temperature: float = 0.7):
    t0 = time.perf_counter()
    try:
        output = generate_text(gemini_client, prompt, temperature)
        print(f"[gemini] response time: {time.perf_counter() - t0:.1f}s")
        return output
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
