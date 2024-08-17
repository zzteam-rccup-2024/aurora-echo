from openai import OpenAI
from config import data


class Whisper:
    def __init__(self, field: str = 'openai-whisper'):
        if data[field]['key'] == '':
            raise ValueError('OpenAI API key not found. Please add your OpenAI API key in config.json')
        self.api_key = data[field]['key']
        self.model = data[field]['model']
        if 'base_url' in data[field]:
            self.base_url = data[field]['base_url']
        else:
            self.base_url = None
        self.openai = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def __call__(self, audio_path: str):
        file = open(audio_path, 'rb')
        return self.openai.audio.transcriptions.create(
            model=self.model,
            file=file
        ).text
