import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
api_key = os.environ["ANTHROPIC_API_KEY"]
print(type(os.getenv("MAX_TOKENS")))
client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=10,
    system="Sen alanında uzman bir Fullstack Developer ve Architectsin.",
    messages=[
        {"role": "user", "content": "Merhaba, kısaca kendini tanıt."}
    ],
)

print(response.content[0].text)