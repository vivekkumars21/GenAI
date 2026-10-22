from httpx import get
from langchain.tools import tool


@tool
def greet_user(name: str) -> str:
    """Generate a greeting message to the user"""
    return f"Hello {name}, Welcome to AI World"


result = greet_user.invoke({"name": "vivek"})
print(result)

print(greet_user.name)
print(greet_user.description)
print(greet_user.args)
