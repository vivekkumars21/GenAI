from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

vector = embeddings.embed_query("What is machine learning?")

print(vector)
