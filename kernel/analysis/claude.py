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
        if data['anthropic']['api_key'] == '':
            raise ValueError('Anthropic API key not found. Please add your Anthropic API key in config.json')
        self.api_key = data['anthropic']['api_key']
        self.model = data['anthropic']['model']
        if self.model not in candidate:
            self.model = 'claude-3-5-sonnet-20240620'
        self.base_url = data['anthropic']['base_url']
        self.anthropic = Anthropic(api_key=self.api_key, base_url=self.base_url)

    def message(self, messages):
        return self.anthropic.completions.create(
            model=self.model,
            messages=messages
        ).choices[0]
