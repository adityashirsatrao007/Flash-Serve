import streamlit as st
import requests
import time

st.set_page_config(page_title="Mini-vLLM Chat", page_icon="⚡", layout="wide")

st.title("⚡ Mini-vLLM: High-Performance Inference Engine")
st.markdown("This UI connects to your custom Python Production Engine.")

# Sidebar for controls
with st.sidebar:
    st.header("Engine Status")
    st.success("Engine is Running")
    st.info("Model: gpt2")
    
    max_tokens = st.slider("Max Tokens", 10, 100, 50)
    
# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is the future of AI?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Note: We are hitting our own API server
            api_url = "http://localhost:8000/v1/completions"
            payload = {"prompt": prompt, "max_tokens": max_tokens}
            
            resp = requests.post(api_url, json=payload)
            resp.raise_for_status()
            
            data = resp.json()
            full_response = data["choices"][0]["text"]
            
            # Simulate streaming effect for UI polish (since our simple API is non-streaming for now)
            displayed_response = ""
            for char in full_response:
                displayed_response += char
                message_placeholder.markdown(displayed_response + "▌")
                time.sleep(0.01)
            message_placeholder.markdown(displayed_response)
            
        except Exception as e:
            st.error(f"Error connecting to engine: {e}")
            full_response = "Error: Could not connect to API server. Make sure `python mini_vllm/serve/api_server.py` is running."
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
