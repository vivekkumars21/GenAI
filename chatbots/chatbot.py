from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()


model = ChatMistralAI(model_name="mistral-small-2506", temperature=0.7)

message: list = [
    SystemMessage(content="You are a funny assistant."),
]

print(
    "----------------------------- !! Welcome to Mistral AI Chatbot !!-----------------------------------"
)

while True:
    prompt = input("You : ")
    message.append(HumanMessage(content=prompt))
    if prompt.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break
    response = model.invoke(message)
    message.append(AIMessage(content=response.content))
    print("Bot : ", response.content)
