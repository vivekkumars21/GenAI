from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()


model = ChatMistralAI(model = "mistral-large-latest")

response = model.invoke("what is paragraph on machine learning?")

print(response.content)