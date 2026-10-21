from dotenv import load_dotenv

load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

search_tool = TavilySearchResults(max_results=5)

llm = ChatOllama(model="gemma4:e4b")

prompt = ChatPromptTemplate.from_template(
    "summarize following search results in short bullet points: {news}"
)

news_result = search_tool.run("latest jio ipo news")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"news": news_result})
print(result)
