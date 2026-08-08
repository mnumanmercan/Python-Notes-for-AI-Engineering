import os
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
from typing import Literal

load_dotenv()
api_key = os.environ["ANTHROPIC_API_KEY"]

class ProductComment(BaseModel):
    product: str
    emotion: Literal["positive", "negative", "neutral"]
    advantages: list[str]
    disadvantages: list[str]
    will_buy_again: Literal["Yes", "No", "Unsure"]

client = Anthropic()

response = client.messages.parse(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system= "Sana verilen metinden yapılandırılmış verileri çıkart (structured output), veriyi JSON formatında sun. Yorum yapma sadece çıktıyı ver.",
    messages= [
        {"role": "user", 
         "content": "Apple Airpods 3 kulaklığı 2 hafta önce aldım. Ses kalitesi harika ama pil ömrü berbat, bir günde bitiyor. Bir de sağ kulaklık ara ara ses kesiyor. Tekrar alır mıydım, emin değilim."}
    ],
    output_format=ProductComment
)

print(response.parsed_output)