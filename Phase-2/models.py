from dataclasses import asdict, dataclass

@dataclass
class Completion:
    text: str
    model: str
    tokens_used: int=0
    finish_reason: str | None = None

completion1 = Completion(text="Generated text 1", model="gpt-4o")
completion2 = Completion(text="Generated text 2", model="gpt-4o", tokens_used=2, finish_reason="Done")

print(completion1)
print(asdict(completion1))
print(completion2)