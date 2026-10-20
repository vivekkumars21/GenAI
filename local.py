from ollama import chat

response = chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": "Write a poem about the ocean. in short ",
            "temperature": 0.7,
        }
    ],
)

print(response.message.content)
