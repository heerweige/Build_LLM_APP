import streamlit as st
import json
import requests

st.title('💬十分钟编写大模型应用')
st.caption("🚀 利用通义千问和 Streamlit 复刻一个聊天机器人")

# 确保模型选择与后端支持一致
with st.sidebar:
    option = st.selectbox(
        '选择大模型引擎',
        ('qwen2.5-72b-instruct', 'qwen-plus', 'qwen-turbo'))

st.session_state["openai_model"] = option

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What can I do for you?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reqest_intputs = {
        "model": st.session_state["openai_model"],  # 使用所选模型
        "messages": st.session_state.messages
    }
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            response = requests.post("http://127.0.0.1:8000/openai",
                                      data=json.dumps(reqest_intputs),
                                      headers={"Content-Type": "application/json"})

            if response.status_code == 200:
                response_data = response.json()
                st.markdown(response_data["content"])
                st.session_state.messages.append({"role": "assistant", "content": response_data["content"]})
            else:
                st.error(f"Error: {response.status_code}, {response.text}")
