from dotenv import load_dotenv

load_dotenv()

import os
import requests

from langchain_google_genai import GoogleGenerativeAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient

#tool creating

def get