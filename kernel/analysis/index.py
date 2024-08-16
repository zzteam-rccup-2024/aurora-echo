from pydantic import BaseModel
import json
from chatgpt import ChatGPT
from claude import Claude
from llama import Llama
from qwen import Qwen
from mistral_ai import MistralAI


class GeneratePromptConfig(BaseModel):
    named_entity: list[tuple[str, str]]
    expression: str
    sentiment: float
    feedback: str
    product_desc: str


class LargeLanguageModel:
    def __init__(self):
        self.overall = open('static/openai/overall.txt', 'r').read()
        self.object = open('static/openai/object.txt', 'r').read()
        self.subject = open('static/openai/subject.txt', 'r').read()
        self.json = open('static/openai/json.txt', 'r').read()

    def generate_prompt(self, target, config: GeneratePromptConfig):
        if target != 'object' and target != 'subject' and target != 'json':
            raise ValueError('target must be either "object", "subject", or "json"')

        overall_prompt = (self.overall.replace(
            '{{ named_entity }}',
            json.dumps(config.named_entity)
        ).replace(
            '{{ expression }}', config.expression
        ).replace(
            '{{ sentiment }}', str(config.sentiment)
        ).replace(
            '{{ product_desc }}', str(config.product_desc)
        ))
        user_prompt = self.object if target == 'object' else self.subject if target == 'subject' else self.json
        user_prompt = user_prompt.replace('{{ feedback }}', config.feedback)

        prompt = [
            {"role": "system", "content": overall_prompt},
            {"role": "user", "content": user_prompt}
        ]

        return prompt

    def __call__(self, model, target, config: GeneratePromptConfig):
        prompt = self.generate_prompt(target, config)
        if model == 'chatgpt':
            return ChatGPT().message(prompt)
        elif model == 'claude':
            return Claude().message(prompt)
        elif model == 'llama':
            return Llama().message(prompt)
        elif model == 'qwen':
            return Qwen().message(prompt)
        elif model == 'mistral':
            return MistralAI().message(prompt)
        else:
            raise ValueError('model must be either "chatgpt", "claude", "llama", "qwen", or "mistral"')

