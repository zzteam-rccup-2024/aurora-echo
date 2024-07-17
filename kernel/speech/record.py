import numpy as np
import pyaudio
from kernel.speech.config import FORMAT, CHANNELS, RATE, CHUNK, SILENCE_THRESHOLD, SILENCE_DURATION
from kernel.speech.utils import db_level
import wave
from datetime import datetime


def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print('Recording...')

    audio_buffer = np.empty((0, ), dtype=np.int16)
    silent_chunks = 0
    recording = True

    while recording:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        audio_buffer = np.concatenate((audio_buffer, data))

        if db_level(data) > SILENCE_THRESHOLD:
            silent_chunks += 1

            if silent_chunks > (SILENCE_DURATION * RATE / CHUNK):
                recording = False
        else:
            silent_chunks = 0

    print(f"Recording: {len(audio_buffer) / RATE:.2f}s", end='\r')
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return audio_buffer


def save_to_wav(audio):
    filename = f"data/audio/{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio.tobytes())