import cv2
from pydantic import BaseModel
from enum import Enum
from kernel.camera.manager import CameraManager
from kernel.speech.record import record_audio, save_to_wav
from kernel.speech.recognize import recognize_audio
import threading
from kernel.text.sentiment.predict import predict_sentiment
from kernel.text.sentiment.train import load_sentiment_model
from kernel.text.entity import recognize_entities
from kernel.analysis.call.chatgpt import send_to_chatgpt, generate_prompt
from kernel.analysis.call.llama import send_to_llama_online
from kernel.analysis.call.baidu import send_to_qianfan
from kernel.analysis.evaluate.llama import send_to_llama_offline
from kernel.analysis.evaluate.qwen import send_to_qwen_offline
import json


class LLMChoice(Enum):
    Llama_online = 'Llama-3-70B-Instruct', send_to_llama_online
    Llama_offline = 'Llama-3-8B-Instruct', send_to_llama_offline
    ChatGPT_online = 'chatgpt-3.5-turbo', send_to_chatgpt
    Qwen_offline = 'Qwen2-1.5B-Instruct', send_to_qwen_offline
    Ernie_online = 'ERNIE-4.0-8K-latest', send_to_qianfan


class AuroraEchoConfig(BaseModel):
    model: LLMChoice
    mosaic: bool


class VisualReaction(BaseModel):
    thumbs: dict[str, int]
    emotions: list[str]


class AuroraEchoProvider:
    def __init__(self, camera: CameraManager, config: AuroraEchoConfig):
        self.camera = camera
        self.model = config.model
        self.apply_mosaic = config.mosaic
        self.recognizing = False
        self.text = ''
        self.sentiment = 0
        self.named_entities = []
        self.recognize_thread: threading.Thread = None
        load_sentiment_model()
        self.call_llm = self.model.value[1]
        self.product_desc = ''

    def recognize_audio(self):
        try:
            self.recognizing = True
            audio = record_audio()
            recognised = recognize_audio(audio)
            save_to_wav(audio)
            self.text = recognised
        finally:
            self.recognizing = False
            self.named_entities = recognize_entities(self.text)
            self.sentiment = predict_sentiment(self.text)

    def start_recognize(self):
        if self.recognizing:
            return
        self.recognize_thread = threading.Thread(target=self.recognize_audio)
        self.recognize_thread.start()
        self.recognizing = True

    def interrupt_recognize(self):
        self.recognize_thread.join()
        self.recognizing = False

    def integrate_llm(self, target):
        desc = open('static/openai/product_desc.txt', 'r').read()
        reaction = VisualReaction(thumbs=self.camera.thumbs, emotions=self.camera.get_facial_list())
        visual = f"Thumbs: up {reaction.thumbs['up']} times, down {reaction.thumbs['down']} times\n" \
                 f"Emotions: {'>'.join(reaction.emotions)}"
        prompt = generate_prompt(target, {
            'named_entity': self.named_entities,
            'expression': visual,
            'sentiment': self.sentiment,
            'feedback': self.text,
            'product_desc': desc
        })
        result = self.call_llm(prompt)
        return result
