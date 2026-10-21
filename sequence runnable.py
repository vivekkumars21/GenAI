from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

prompt = ChatPromptTemplate.from_template("explain me topic of {topic} in short")

model = ChatOllama(model="gemma4:e4b")
parser = StrOutputParser()

sort_prompt = ChatPromptTemplate.from_template("explain {topic} in short")
detailed_prompt = ChatPromptTemplate.from_template("explain {topic} in detail")


chain = RunnableParallel(
    {
        "sort": sort_prompt | model | parser,
        "detailed": detailed_prompt | model | parser,
    }
)

result = chain.invoke({"topic": "quantum computing"})

print(result)
