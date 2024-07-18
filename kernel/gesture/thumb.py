import mediapipe as mp
from cv2.typing import MatLike

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)


def classify_hand_gesture(landmarks):
    thumb_tip = landmarks[4]
    thumb_mcp = landmarks[2]
    index_finger_mcp = landmarks[5]

    if thumb_tip.y < thumb_mcp.y and thumb_tip.y < index_finger_mcp.y:
        return "thumb up"
    elif thumb_tip.y > thumb_mcp.y and thumb_tip.y > index_finger_mcp.y:
        return "thumb down"
    else:
        return "none"


def get_thumb(frame: MatLike):
    results = hands.process(frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = classify_hand_gesture(hand_landmarks.landmark)
            return gesture
    return "none"
