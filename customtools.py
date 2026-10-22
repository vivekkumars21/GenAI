from langchain.tools import tool


@tool
def greet_user(name: str) -> str:
    """Generate a greeting message to the user"""
    return f"Hello {name}, Welcome to AI World"


result = greet_user.invoke({"name": "vivek"})
print(result)
