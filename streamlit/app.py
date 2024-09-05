import streamlit as st
from langchain_google_vertexai import ChatVertexAI
import os
from dotenv import load_dotenv
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
import random
import time


# load environment variables from .env file
load_dotenv()

PROJECT_ID = os.environ.get('PROJECT_ID')   # @param {type:"string"}

model = ChatVertexAI(model="gemini-1.5-flash", project=PROJECT_ID)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)

config = {"configurable": {"session_id": "abc2"}} # dummy value; todo later

st.title("Chat Bot")

def generate_response(input_text):
    st.info(with_message_history.invoke(
    [HumanMessage(content=input_text)],
    config=config,
    ).content)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)

