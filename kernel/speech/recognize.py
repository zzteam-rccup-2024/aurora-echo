import gc
import numpy as np
import torch
from transformers import AutoProcessor, AutoModelForCTC
from kernel.config import device


class Wav2Vec:
    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("data/models/facebook/wav2vec2-large-960h")
        self.model = AutoModelForCTC.from_pretrained("data/models/facebook/wav2vec2-large-960h")

        self.model = self.model.to(device)
        print('Recognizer initialized')

    def __call__(self, audio: np.ndarray) -> str:
        inputs = self.processor(audio, return_tensors="pt", sampling_rate=16000).input_values.float().to(device)
        with torch.no_grad():
            logits = self.model(inputs).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]

            return transcription.lower()
