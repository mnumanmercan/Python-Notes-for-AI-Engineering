def count_up(limit):
    for i in range(limit):
        yield i+1

for n in count_up(5):
    print(n)

def stream_upper(words: list[str]):
    for word in words:
            yield word.upper()
for n in stream_upper(["hello world", "mnm"]):
    print(n)
