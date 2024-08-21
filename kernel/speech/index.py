from kernel.speech.recognize import Wav2Vec
from kernel.speech.whisper import Whisper
from kernel.availability import check_availability


class SpeechToTextModel:
    def __init__(self):
        self.model = None

    def switch(self, model: str = 'whisper'):
        if model == 'whisper':
            self.model = Whisper('openai-whisper' if check_availability() else 'openai-proxied-whisper')
        elif model == 'wav2vec':
            self.model = Wav2Vec()
        else:
            raise ValueError('Invalid model')

    def __call__(self, audio):
        return self.model(audio)