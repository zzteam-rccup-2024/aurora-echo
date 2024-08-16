from openai import OpenAI
from config import data

candidate = [
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-4-turbo",
    "gpt-4-turbo-2024-04-09",
    "gpt-4-0125-preview",
    "gpt-4-turbo-preview",
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-16k-0613",
]


class ChatGPT:
    def __init__(self):
        if data['openai']['key'] == '':
            raise ValueError('OpenAI API key not found. Please add your OpenAI API key in config.json')
        self.api_key = data['openai']['key']
        self.model = data['openai']['model']
        if self.model not in candidate:
            self.model = 'gpt-4o-2024-08-06'
        self.openai = OpenAI(api_key=self.api_key)

    def message(self, messages):
        return self.openai.chat.completions.create(
            model=self.model,
            messages=messages
        ).choices[0]

    def json(self, messages, schema):
        return self.openai.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=schema,
        )
