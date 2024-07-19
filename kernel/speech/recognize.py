import gc
import numpy as np
import torch
from transformers import AutoProcessor, AutoModelForCTC
from kernel.config import device


def recognize_audio(audio: np.ndarray) -> str:
    print('Initializing the recognizer...')

    processor = AutoProcessor.from_pretrained("data/models/facebook/wav2vec2-large-960h")
    model = AutoModelForCTC.from_pretrained("data/models/facebook/wav2vec2-large-960h")

    model = model.to(device)
    print('Recognizer initialized')

    inputs = processor(audio, return_tensors="pt", sampling_rate=16000).input_values.float().to(device)
    with torch.no_grad():
        logits = model(inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]

        del model
        del processor
        gc.collect()

        return transcription.lower()
