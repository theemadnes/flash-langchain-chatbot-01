import gradio as gr
#from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import ChatVertexAI
import os
from dotenv import load_dotenv
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage


# load environment variables from .env file
load_dotenv()

PROJECT_ID = os.environ.get('PROJECT_ID')   # @param {type:"string"}

# check to see if $PORT is set, and if so, set Gradio env var to use it. otherwise, use 8080 as default.
if "PORT" in os.environ:
  os.environ["GRADIO_SERVER_PORT"] = os.getenv(
    "PORT"
  )
else:
    os.environ["GRADIO_SERVER_PORT"] = "8080"
    
print(f"Setting Gradio server port to {os.getenv('GRADIO_SERVER_PORT')}")

model = ChatVertexAI(model="gemini-1.5-flash", project=PROJECT_ID)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)

config = {"configurable": {"session_id": "abc2"}} # dummy value; todo later

def generate_response(message, history):
  # not using the history variable, since we're using langchain stuff to store history
  #print(gr.State())
  #print(history)
  ans = with_message_history.invoke(
    [HumanMessage(content=message)],
    config=config,
    )
  return ans.content

interface = gr.ChatInterface(fn=generate_response, examples=["Tell me about Chicago", "What was flying in the Concorde like?", "Where is the Bermuda Triangle?"], title="Chat Bot")

if __name__ == "__main__":
  interface.launch(server_name="0.0.0.0")
