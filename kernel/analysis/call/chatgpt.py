from openai import OpenAI
from config import OPENAI_KEY
from typing import TypedDict
import json
from kernel.availability import check_availability

client = OpenAI(api_key=OPENAI_KEY)


class GeneratePromptConfig(TypedDict):
    named_entity: list[tuple[str, str]]
    expression: str
    sentiment: float
    feedback: str
    product_desc: str


def generate_prompt(target, config: GeneratePromptConfig):
    if target != 'object' and target != 'subject':
        raise ValueError('target must be either "object.txt" or "subject"')

    overall_prompt = open('static/openai/overall.txt', 'r')\
        .read()\
        .replace('{{ named_entity }}', json.dumps(config['named_entity']))\
        .replace('{{ expression }}', config['expression'])\
        .replace('{{ sentiment }}', str(config['sentiment'])\
        .replace('{{ product_desc }}', str(config['product_desc'])))
    user_prompt = open(f'static/openai/{target}.txt', 'r').read() \
        .replace('{{ feedback }}', config['feedback'])

    prompt = [
        { "role": "system", "content": overall_prompt },
        { "role": "user", "content": user_prompt }
    ]

    return prompt


def send_to_chatgpt(prompt, model="gpt-4o-mini"):
    if not check_availability():
        raise Exception('ChatGPT is not available in your country, it may be due to the censorship of the Internet, '
                        'or the unavailability of OpenAI API Service.')
    return client.chat.completions.create(
        model=model,
        messages=prompt,
    ).choices[0].message.content
