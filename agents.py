from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatMistralAI(model_name="mistral-small-2506")
parse = StrOutputParser()

short_temp = ChatPromptTemplate.from_template("Explain {topic} in short.")

formatted_prompt = short_temp.format_prompt(topic="data science")
response = model.invoke(formatted_prompt)
