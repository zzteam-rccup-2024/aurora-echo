from kernel.facial.model import fetch_model
from cv2.typing import MatLike
import cv2
from kernel.facial.dataset import transform
from kernel.config import device


class FacialEmotionRecognizer:
    def __init__(self):
        self.model, _, _ = fetch_model('data/models/facial.pth')
        self.model.eval()

    def __call__(self, image: MatLike):
        image = transform(image).float().to(device)
        result = self.model(image.unsqueeze(0))
        mappings = {'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'neutral': 4, 'others': 5, 'sad': 6, 'surprise': 7}
        return list(mappings.keys())[result.argmax().item()]


def with_camera(recognizer: FacialEmotionRecognizer, camera: cv2.VideoCapture):
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        recognized = recognizer(frame)
        print(recognized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break