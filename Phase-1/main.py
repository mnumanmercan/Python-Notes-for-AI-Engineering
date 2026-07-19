from helpers import format_message

msgs = [
    {"role": "user", "content": "Merhaba"},
    {"role": "assistant", "content": "Selam!"},
]

print(format_message(msgs))