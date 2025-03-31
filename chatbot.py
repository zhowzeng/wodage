import streamlit as st

from swarm import Agent, Swarm


def run_agent(messages: list):
    agent = Agent(
        name="General Assistant",
        instructions="回答使用者的問題，語言使用正體中文或英文。",
        model=st.session_state.model,
    )
    response = st.session_state.client.run(agent=agent, messages=messages)
    return response.messages


st.title("我大哥")
st.info("目前能夠簡單聊天，未來會加入更多功能。", icon="ℹ️")


if "client" not in st.session_state:
    st.session_state.client = Swarm()

if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"

with st.sidebar:
    choice = st.selectbox(
        "Select OpenAI Model",
        options=["gpt-4o-mini", "gpt-4o"],
    )
    st.session_state.model = choice


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    messages = run_agent(st.session_state.messages)
    st.session_state.messages.extend(messages)
    st.rerun()
