from typing import Callable
Message = dict[str, str]
# Message alias'ı zaten var: Message = dict[str, str]

def transform_messages(messages: list[Message], transformer: Callable[[Message], Message]) -> list[Message]:
    return [transformer(m) for m in messages]


# Kullanım örneği:
def to_upper(msg):
    return {"role": msg["role"], "content": msg["content"].upper()}

result = transform_messages(msgs, to_upper)