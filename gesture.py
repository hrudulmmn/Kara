import cv2
import mediapipe as mp
capture = cv2.VideoCapture(0)
hands = mp.solutions.hands
draw = mp.solutions.drawing_utils

hand = hands.Hands(
    static_image_mode = False,
    max_num_hands = 1,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)
while True:
    ret,frame = capture.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    result = hand.process(rgb)

    if result.multi_hand_landmarks:
        for landmarks in result.multi_hand_landmarks:
            draw.draw_landmarks(
                frame,
                landmarks,
                hands.HAND_CONNECTIONS
            )
    cv2.imshow("Camera",frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    
    for point in result.multi_hand_landmarks:
        point.x = point.x - result.multi_hand_landmarks[0].x
        point.y = point.y - result.multi_hand_landmarks[0].y
capture.release()
cv2.destroyAllWindows()
hand.close()

