from mistralai import Mistral
from config import data


class MistralAI:
    def __init__(self):
        self.model = data['mistral']['model']
        self.api_key = data['mistral']['key']
        self.mistral = Mistral(api_key=self.api_key)

    def message(self, messages):
        return self.mistral.chat.complete(
            model=self.model,
            messages=messages
        ).choices[0].message.content
