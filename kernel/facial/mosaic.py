import cv2
from cv2.typing import MatLike
import mediapipe as mp


def apply_mosaic(image: MatLike, x: int, y: int, w: int, h: int, size=5):
    sub_face = image[y:y + h, x:x + w]
    sub_face = cv2.resize(sub_face, (size, size), interpolation=cv2.INTER_LINEAR)
    sub_face = cv2.resize(sub_face, (w, h), interpolation=cv2.INTER_NEAREST)
    image[y:y + h, x:x + w] = sub_face
    return image


class PerformMosaic:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=1,
                                                                   min_detection_confidence=0.5)

    def __call__(self, image: MatLike):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        try:
            faces = self.face_detection.process(image)
            if faces.detections:
                for detection in faces.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = image.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    image = apply_mosaic(image, x, y, w, h)

            return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        except:
            cv2.putText(image, 'Error in performing mosaic', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
