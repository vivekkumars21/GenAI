from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()


model = ChatMistralAI(model = "mistral-large-latest", temperature= 0) #temp low for reasonable responses and high for creative responses

response = model.invoke("poem on ai")

print(response.content)