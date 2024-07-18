import cv2
from cv2.typing import MatLike
from kernel.facial.predict import FacialEmotionRecognizer


class CameraManager:
    def __init__(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id)
        self.face_recognizer = FacialEmotionRecognizer()
        self.facial_expressions = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'neutral': 0, 'sad': 0,
                                   'surprise': 0}
        self.hand_action = 'none'
        self.emotion = 'neutral'

    def get_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            return None
        return frame

    def recognize_face(self, frame: MatLike):
        result = self.face_recognizer(frame)
        if result == 'others':
            return
        self.emotion = result
        self.facial_expressions[result] += 1

    def get_facial_list(self):
        sorted(self.facial_expressions.items(), key=lambda x: x[1], reverse=True)
