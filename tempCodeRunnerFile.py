from email import message

from dotenv import load_dotenv

load_dotenv()

from httpx2 import query
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage

from rich import print


@tool
def get_textToLength(text: str) -> int:
    """Return the charcter len of given text"""
    return len(text)


tools = {"get_textToLength": get_textToLength}

# tool Binding


llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

llm_bind = llm.bind_tools([get_textToLength])

query = HumanMessage(
    "Return the number of characters given in the text : hello how are you !!"
)
messages = []
messages.append(query)


result = llm_bind.invoke(messages)

messages.append(result)


if result.tool_calls:
    tool_name = result.tool_calls[0]["name"]
    tool_message = tools[tool_name].invoke(result.tool_calls[0])

    messages.append(tool_message)

results = llm_bind.invoke(messages)
print(results.content)
