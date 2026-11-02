
# client.py - Streamlit chat UI that calls the FastAPI endpoint
import requests
import streamlit as st

st.title("GenAI Lab Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask the tutor something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        r = requests.get(
            "http://localhost:8000/generate/text",
            params={"prompt": prompt},
            timeout=600,
        )
    r.raise_for_status()
    answer = r.json()

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)