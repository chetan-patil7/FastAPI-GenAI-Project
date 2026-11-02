# main.py - Act 1 (naive): the model is loaded INSIDE the handler on every request
import time
from fastapi import FastAPI
from models import load_text_model, generate_text

app = FastAPI()


@app.get("/generate/text")
def serve_language_model_controller(prompt: str, temperature: float = 0.7):
    t0 = time.perf_counter()
    pipe = load_text_model()  # <-- slow: reloads weights every request
    load_s = time.perf_counter() - t0
    output = generate_text(pipe, prompt, temperature)
    print(f"[act1] model load: {load_s:.1f}s, total: {time.perf_counter() - t0:.1f}s")
    return output
