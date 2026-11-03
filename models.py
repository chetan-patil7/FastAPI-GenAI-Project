# models.py - Gemini API version
import os
import time
from google import genai
from google.genai import types

MODEL = "gemini-3.8-flash"
MAX_RETRIES = 3  # retry on 503 overload errors

SYSTEM_PROMPT = (
    "You are a friendly tutor for school students. "
    "Explain simply, in short answers, and use markdown."
)


def load_text_model():
    """Initialize and return the Gemini client (replaces local pipeline)."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set. "
            "Create a .env file with: GEMINI_API_KEY=your_key_here"
        )
    client = genai.Client(api_key=api_key)
    return client


def generate_text(
    pipe,                        # Gemini client (was: HuggingFace Pipeline)
    prompt: str,
    temperature: float = 0.7,
    max_new_tokens: int = 512,
) -> str:
    """Generate text using the Gemini API with retry on 503 overload."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[gemini] Attempt {attempt}/{MAX_RETRIES} with model: {MODEL}")
            response = pipe.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=temperature,
                    max_output_tokens=max_new_tokens,
                ),
            )
            print(f"[gemini] Success on attempt {attempt}")
            return response.text.strip()

        except Exception as e:
            error_str = str(e)
            is_overloaded = "503" in error_str or "UNAVAILABLE" in error_str
            is_rate_limited = "429" in error_str

            if (is_overloaded or is_rate_limited) and attempt < MAX_RETRIES:
                wait = 2 ** (attempt - 1)  # 1s, 2s, 4s
                print(f"[gemini] Overloaded (attempt {attempt}), retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"[ERROR] {type(e).__name__}: {e}")
                raise