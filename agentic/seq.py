import os
from typing import TypedDict


class pipelineState(TypedDict):
    raw_input: str
    edited_text: str
    scripted_text: str
    final_output: str


from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.7)
