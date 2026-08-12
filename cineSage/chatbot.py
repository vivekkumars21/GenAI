from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate

model = ChatMistralAI(model_name="mistral-small-2506")

prompt = PromptTemplate.from_template("""
Extract movie details from the following paragraph.

Return:
Movie Name:
Release Year:
Director:
Actors:
Genre:
Plot:
Rating: 

if other details are not available, you can go with wikipeida details

Paragraph:
{paragraph}
""")

paragraph = input("Enter movie paragraph: ")

response = model.invoke(prompt.format(paragraph=paragraph))

print(response.content)
