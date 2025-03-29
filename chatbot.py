import streamlit as st
import requests


def get_agent_output(messages: list):
    response = requests.post(
        url="http://127.0.0.1:5000/chat",
        headers={"Content-Type": "application/json"},
        json={"messages": messages, "model": st.session_state["openai_model"]},
    )
    response.raise_for_status()
    return response.json()["response"]


st.title("我大哥")
st.info("目前能夠簡單聊天，未來會加入更多功能。", icon="ℹ️")

# Set OpenAI API key from Streamlit secrets

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

with st.sidebar:
    choice = st.selectbox(
        "Select OpenAI Model",
        options=["gpt-4o-mini", "gpt-4o"],
    )
    st.session_state.openai_model = choice


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = get_agent_output(st.session_state.messages)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
