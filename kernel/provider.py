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
from kernel.analysis.index import LargeLanguageModel, GeneratePromptConfig


class AuroraEchoConfig(BaseModel):
    mosaic: bool


class VisualReaction(BaseModel):
    thumbs: dict[str, int]
    emotions: list[str]


class AuroraEchoProvider:
    def __init__(self, camera: CameraManager, config: AuroraEchoConfig):
        self.camera = camera
        self.apply_mosaic = config.mosaic
        self.recognizing = False
        self.text = ''
        self.sentiment = 0
        self.named_entities = []
        self.recognize_thread: threading.Thread | None = None
        load_sentiment_model()
        self.model = LargeLanguageModel()
        self.product_desc = ''
        self.object_analysis = ''
        self.subject_analysis = ''
        self.llm_thread: threading.Thread | None = None
        self.generating = False

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
        self.camera.thumbs['up'] = 0
        self.camera.thumbs['down'] = 0
        self.camera.facial_expressions = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'neutral': 0, 'sad': 0,
                                          'surprise': 0}
        self.recognize_thread.start()
        self.recognizing = True

    def interrupt_recognize(self):
        self.recognize_thread.join()
        self.recognizing = False

    def integrate_llm(self, target):
        self.generating = True
        desc = open('static/openai/product_desc.txt', 'r').read()
        reaction = VisualReaction(thumbs=self.camera.thumbs, emotions=self.camera.get_facial_list())
        visual = f"Thumbs: up {reaction.thumbs['up']} times, down {reaction.thumbs['down']} times\n" \
                 f"Emotions: {'>'.join(reaction.emotions)}"
        config = GeneratePromptConfig(named_entity=self.named_entities, expression=visual, sentiment=self.sentiment,
                                      feedback=self.text, product_desc=desc)
        result = self.model(target, config)
        self.generating = False
        return result

    def call_llm_object(self):
        object_comment = self.integrate_llm('object')
        self.object_analysis = object_comment
        return object_comment

    def call_llm_subject(self):
        subject_comment = self.integrate_llm('subject')
        self.subject_analysis = subject_comment
        return subject_comment

    def start_llm(self, target, model):
        self.model.switch(model)
        self.llm_thread = threading.Thread(target=self.call_llm_object if target == 'object' else self.call_llm_subject)
        self.llm_thread.start()

    def interrupt_llm(self):
        self.llm_thread.join()

    def get_llm_result(self, target):
        if target == 'object':
            return self.object_analysis
        elif target == 'subject':
            return self.subject_analysis
        else:
            return 'Invalid target'

    def set_mosaic(self, mosaic: bool):
        self.apply_mosaic = mosaic

    def get_mosaic(self):
        return self.apply_mosaic

    def get_subject_analysis(self):
        return self.subject_analysis

    def get_object_analysis(self):
        return self.object_analysis
