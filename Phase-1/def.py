def format_message(messages, separator=" | ", **kwargs):
    
    message = [f"{m['role']}: {m['content']}" for m in messages]
    print(kwargs)
    return separator.join(message)

msgs = [
    {"role": "user", "content": "Merhaba"},
    {"role": "assistant", "content": "Selam!"},
]
# Beklenen: "user: Merhaba | assistant: Selam!"

format_message(msgs, model="test", temparature=0.4)