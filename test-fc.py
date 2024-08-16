from pydantic import BaseModel
from kernel.analysis.chatgpt import ChatGPT


class Foo(BaseModel):
    a: int
    b: str


message = [
    {'role': 'user', 'content': 'Testing the JSON output for ChatGPT.'}
]

gpt = ChatGPT()
result = gpt.json(messages=message, schema=Foo)
print(result)