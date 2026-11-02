# 🤖 FastAPI GenAI Chatbot

A lightweight **Generative AI chatbot** built with **FastAPI** (backend) and **Streamlit** (frontend), powered by the **TinyLlama-1.1B** language model via Hugging Face Transformers.

---

## 📁 Project Structure

```
FastAPI_GenAI_Project/
│
├── main.py           # FastAPI server — exposes the /generate/text endpoint
├── models.py         # AI model logic — loads TinyLlama and generates text
├── client.py         # Streamlit chat UI — sends requests to FastAPI
├── requirements.txt  # Python dependencies
├── .gitignore        # Git ignore rules
└── README.md         # Project documentation
```

---

## 🔄 Request Flow

```
User (Browser)
    │
    ▼
client.py  ──── HTTP GET ────►  main.py  ────►  models.py
(Streamlit UI)               (FastAPI server)  (TinyLlama model)
    ▲                                                  │
    └──────────── Response (generated text) ◄──────────┘
```

1. User types a message in the **Streamlit UI** (`client.py`)
2. Streamlit sends an **HTTP GET** request to `http://localhost:8000/generate/text`
3. **FastAPI** (`main.py`) receives the request and calls the model functions
4. **`models.py`** loads TinyLlama and generates a response
5. The response is returned and displayed in the chat UI

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FastAPI_GenAI_Project.git
cd FastAPI_GenAI_Project
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv genaiservice

# Activate (Windows)
genaiservice\Scripts\activate

# Activate (Mac/Linux)
source genaiservice/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI backend

```bash
uvicorn main:app --reload
```

> API will be available at: `http://localhost:8000`
> Swagger docs at: `http://localhost:8000/docs`

### 5. Run the Streamlit frontend (new terminal)

```bash
streamlit run client.py
```

> Chat UI will open at: `http://localhost:8501`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI + Uvicorn |
| **Frontend** | Streamlit |
| **AI Model** | TinyLlama-1.1B-Chat-v1.0 |
| **ML Framework** | Hugging Face Transformers + PyTorch |
| **HTTP Client** | Python `requests` |

---

## 📡 API Reference

### `GET /generate/text`

Generates a text response from the language model.

**Query Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `prompt` | `string` | required | The user's input message |
| `temperature` | `float` | `0.7` | Controls randomness (0.0 = deterministic, 1.0 = creative) |

**Example Request:**
```
GET http://localhost:8000/generate/text?prompt=What is FastAPI?&temperature=0.7
```

**Example Response:**
```json
"FastAPI is a modern, fast web framework for building APIs with Python..."
```

---

## 🌿 Branch Strategy

| Branch | Description |
|---|---|
| `main` | Stable version using **TinyLlama** (local model) |
| `gemini-api` | Experimental version using **Google Gemini API** |

---

## ⚙️ Configuration

The model and system prompt can be configured in `models.py`:

```python
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Change model here

SYSTEM_PROMPT = (
    "You are a friendly tutor for school students. "
    "Explain simply, in short answers, and use markdown."
)
```

To increase response length, update `max_new_tokens` in `models.py`:
```python
def generate_text(..., max_new_tokens: int = 512):  # default is 128
```

---

## 📋 Requirements

```
fastapi
uvicorn
transformers
torch
streamlit
requests
```

---

## 📝 Notes

- The model runs **locally on CPU** by default. If a CUDA GPU is available, it will automatically use it for faster inference.
- The first request may be slow as the model weights are downloaded from Hugging Face (~2GB).
- This project is structured as **Act 1 (naive)** — the model is reloaded on every request. Future acts will optimize this with model caching.
