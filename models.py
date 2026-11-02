# models.py - Act 1: load a Hugging Face model and generate text
import torch
from transformers import Pipeline, pipeline

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

SYSTEM_PROMPT = (
    "You are a friendly tutor for school students. "
    "Explain simply, in short answers, and use markdown."
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# bfloat16 only makes sense on GPU; use float32 on CPU
dtype = torch.bfloat16 if device.type == "cuda" else torch.float32


def load_text_model() -> Pipeline:
    return pipeline(
        "text-generation",
        model=MODEL_ID,
        torch_dtype=dtype,
        device=device,
    )


def generate_text(
    pipe: Pipeline,
    prompt: str,
    temperature: float = 0.7,
    max_new_tokens: int = 128,
) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    chat_prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    out = pipe(
        chat_prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_k=50,
        top_p=0.95,
        return_full_text=False,  # return only the new text, not the whole chat
    )
    return out[0]["generated_text"].strip()