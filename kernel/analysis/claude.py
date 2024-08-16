from anthropic import Anthropic
from config import data

candidate = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-2.1",
    "claude-2.0",
    "claude-instant-1.2",
]


class Claude:
    def __init__(self):
        if data['anthropic']['key'] == '':
            raise ValueError('Anthropic API key not found. Please add your Anthropic API key in config.json')
        self.api_key = data['anthropic']['key']
        self.model = data['anthropic']['model']
        if self.model not in candidate:
            self.model = 'claude-3-5-sonnet-20240620'
        self.anthropic = Anthropic(api_key=self.api_key)

    def message(self, messages):
        contents = self.anthropic.messages.create(
            model=self.model,
            messages=messages,
            max_tokens=1024
        ).content

        result = ''

        for content in contents:
            if content.type == 'text':
                result += content.text + '\n'

        return result
