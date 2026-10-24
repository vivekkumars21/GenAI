from dotenv import load_dotenv
from fastapi import params

load_dotenv()

import os
import requests

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from langchain.agents import create_agent

from rich import print

# tool creating


@tool
def get_weather(city: str) -> str:
    """Get the current weather of any city"""

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": os.getenv("d9d1ab1a709bbf4687919f79d7845b27"),
        "units": "metric",
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if response.status_code != 200:
        return (
            f"Could not get weather for {city}: {data.get('message', 'Unknown error')}"
        )

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f" Weather in {city}: {desc}, {temp} °C "


# tavily

tavilyClient = TavilyClient()


@tool
def get_latestNews(city: str) -> str:
    """Get the latest news about a specific city."""

    response = tavilyClient.search(
        query=f"Latest news in {city}", topic="news", time_range="day", max_results=5
    )

    news = response.get("results", [])

    if not news:
        return f"No recent news found for {city}."

    formatted_news = []

    for item in news:
        formatted_news.append(
            f"Title: {item.get('title', 'No title')}\n"
            f"Summary: {item.get('content', 'No summary')}\n"
            f"URL: {item.get('url', 'No URL')}"
        )

    return "\n\n".join(formatted_news)


llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")


# Agent loop

agent = create_agent(
    llm,
    tools=[get_weather, get_latestNews],
    system_prompt="You are a  helpful city assistant",
)

print("City Agent | Type exit for quit")

while True:
    user_input = input("You : ")
    if user_input.lower() == "exit":
        break

    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
    )

    print(result)
