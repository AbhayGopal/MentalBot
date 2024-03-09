import os
import openai
import json
import streamlit as st


st.title("MentalBot")

openai.api_base = st.secrets["OPENAI_API_KEY"] #points to .streamlit/secrets.toml
# change openai.api_base to openai.api_key if using the openai api

# Check for existing chat history file
chat_history_file = "chat_history.json"
if os.path.exists(chat_history_file):
    with open(chat_history_file, "r") as f:
        st.session_state.messages = json.load(f)
else:
    st.session_state.messages = []

# Session state for model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "caffeinatedwoof/llama-2-7b-chat-hf-amod-mental-health-counseling-conversations-GGML"

print(st.session_state["openai_model"])  # Debugging

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input and prompt update
if prompt := st.chat_input("How are you feeling?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response and message update
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="local-model",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save chat history to JSON file
with open(chat_history_file, "w") as f:
    json.dump(st.session_state.messages, f)


