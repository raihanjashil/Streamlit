import os
import streamlit as st
from mistralai import Mistral

MODEL_ID = "mistral-small-latest"
CHAT_INPUT_PLACEHOLDER = "How can I help you today?"
PAGE_TITLE = "Mistral Customer Support"

def get_client():
    return Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def render_history():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def get_response(client, messages):
    response = client.chat.complete(
        model=MODEL_ID,
        messages=[{"role": m["role"], "content": m["content"]} for m in messages]
    )
    return response.choices[0].message.content

def handle_input(client, user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        reply = get_response(client, st.session_state.messages)
        placeholder.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

def main():
    st.title(PAGE_TITLE)
    client = get_client()
    init_session()
    render_history()

    user_input = st.chat_input(CHAT_INPUT_PLACEHOLDER)
    if user_input:
        handle_input(client, user_input)

if __name__ == "__main__":
    main()