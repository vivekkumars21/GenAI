from dotenv import load_dotenv

load_dotenv()

from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

search_tool = TavilySearch(max_results=5)

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

prompt = ChatPromptTemplate.from_template(
    "summarize following search results in short bullet points: {news}"
)

news_result = search_tool.run("latest jio ipo news")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"news": news_result})
print(result)
