import gradio as gr
from langchain_google_vertexai import VertexAI
import os
from dotenv import load_dotenv

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

llm = VertexAI(model_name="gemini-1.5-flash", project=PROJECT_ID)

def generate_response(message, history):
  #ans = rag_chain({"question": message, "chat_history": chat_history})["answer"]
  ans = llm(message)
  return ans

interface = gr.ChatInterface(fn=generate_response, examples=["Tell me about Chicago", "What was flying in the Concorde like?", "Where is the Bermuda Triangle?"], title="Chat Bot")
interface.launch(server_name="0.0.0.0")