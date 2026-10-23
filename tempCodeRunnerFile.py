from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

from rich import print


@tool
def get_textToLength(text: str) -> int:
    """Return the charcter len of given text"""
    return len(text)


# tool Binding

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

llm_bind = llm.bind_tools([get_textToLength])

result = llm.invoke("Return the charcter len of given text : hello how are you")
result2 = llm_bind.invoke("Return the charcter len of given text : hello how are you")
print(result)
print(result2.content)
