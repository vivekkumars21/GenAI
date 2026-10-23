from dotenv import load_dotenv
from fastapi import params

load_dotenv()

import os
import requests

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient

from rich import print

# tool creating


@tool
def get_weather(city: str) -> str:
    """Get the current weather of any city"""

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": os.getenv("d9d1ab1a709bbf4687919f79d7845b27"),
        "units": " metric",
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


print(get_weather.invoke("ahmedabad"))

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


print(get_latestNews.invoke("Ahmedabad"))

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

tools = {"get_weather": get_weather, "get_latestNews": get_latestNews}

llm_with_tools = llm.bind_tools([get_weather, get_latestNews])


# agentLoop

messages = []

print("City intelligence System")
print("enter EXIT for quit")


while True:
    user_input = input("User : ")
    if user_input.lower() == "exit":
        break

    messages.append(HumanMessage(user_input))

    while True:
        result = llm_with_tools.invoke(messages)
        messages.append(result)

        if result.tool_calls:
            for tool_call in result.tool_calls:
                tool_name = tool_call["name"]
                #  Human in loop
                confirm = input(
                    "agent want to call this {tool_name} if you want to continue type YES nither No"
                )

                if confirm.lower() != "yes":
                    print("Call denied")
                    break

                # execute Tools
                tool_result = tools[tool_name].invoke(tool_call)
                messages.append(
                    ToolMessage(content=tool_result, tool_call_id=tool_call["id"])
                )

                continue

            else:
                print(result.content)
