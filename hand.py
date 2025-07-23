import cv2
import mediapipe as mp
import time

# === MediaPipe Hands Initialization ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

# === Button Definitions ===
buttons = {
    '+': (20, 110, 80, 50),
    '-': (120, 110, 80, 50),
    '*': (220, 110, 80, 50),
    '/': (320, 110, 80, 50),
    '=': (420, 110, 80, 50),
    'C': (520, 110, 80, 50),
}




tip_ids = [4, 8, 12, 16, 20]

# === Calculator State ===
expression = ""
last_input_time = 0
hover_start_time = 0
hovering_button = None
waiting_for = "number"
idle_timeout_start = 0

# === Utility Functions ===
def draw_buttons(frame, hover=None, hover_time=0):
    for label, (x, y, w, h) in buttons.items():
        if label == hover:
            brightness = min(int((hover_time / 1.2) * 155), 155)
            color = (50, 200 + brightness // 3, 50)
        else:
            color = (80, 80, 200)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, cv2.FILLED)
        cv2.putText(frame, label, (x + 20, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

def detect_fingers(hand_landmarks):
    lm = hand_landmarks.landmark
    fingers = [1 if lm[tip_ids[0]].x < lm[tip_ids[0] - 1].x else 0]
    for i in range(1, 5):
        fingers.append(1 if lm[tip_ids[i]].y < lm[tip_ids[i] - 2].y else 0)
    return fingers

def classify_number(fingers):
    mapping = {
        (0, 0, 0, 0, 0): 0,
        (0, 1, 0, 0, 0): 1,
        (0, 1, 1, 0, 0): 2,
        (0, 1, 1, 1, 0): 3,
        (0, 1, 1, 1, 1): 4,
        (1, 1, 1, 1, 1): 5
    }
    return mapping.get(tuple(fingers), None)

def get_finger_position(hand_landmarks, frame):
    h, w, _ = frame.shape
    cx = int(hand_landmarks.landmark[8].x * w)
    cy = int(hand_landmarks.landmark[8].y * h)
    return cx, cy

def check_button_hover(cx, cy):
    for label, (x, y, w, h) in buttons.items():
        if x <= cx <= x + w and y <= cy <= y + h:
            return label
    return None

# === Main Loop ===
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers = detect_fingers(hand_landmarks)
            number = classify_number(fingers)
            cx, cy = get_finger_position(hand_landmarks, frame)

            cv2.circle(frame, (cx, cy), 12, (0, 255, 255), 2)

            hovered = check_button_hover(cx, cy)
            hover_duration = current_time - hover_start_time if hovered == hovering_button else 0
            draw_buttons(frame, hover=hovered, hover_time=hover_duration)

            # === Hover Button Interaction ===
            if hovered:
                if hovered == hovering_button:
                    if hover_duration > 1.2:
                        if hovered in '+-*/' and waiting_for == "operator":
                            expression += hovered
                            waiting_for = "number"
                        elif hovered == '=':
                            try:
                                result = str(eval(expression))
                                expression = result
                            except:
                                expression = "Err"
                            waiting_for = "number"
                        elif hovered in ('C', 'Clear'):
                            expression = ""
                            waiting_for = "number"
                        last_input_time = current_time
                        idle_timeout_start = 0
                        hovering_button = None
                        hover_start_time = 0
                else:
                    hovering_button = hovered
                    hover_start_time = current_time
            else:
                hovering_button = None
                hover_start_time = 0

            # === Number Input ===
            if hovered is None and number is not None and (current_time - last_input_time > 0.8):
                if waiting_for == "number":
                    expression += str(number)
                    waiting_for = "operator"
                    last_input_time = current_time
                    idle_timeout_start = current_time

            # === Timeout Handling ===
            if waiting_for == "operator" and idle_timeout_start > 0:
                if current_time - idle_timeout_start > 3:
                    waiting_for = "number"
                    idle_timeout_start = 0
    else:
        draw_buttons(frame)

    # === Display Output ===
    cv2.rectangle(frame, (30, 20), (750, 80), (30, 30, 30), -1)
    cv2.putText(frame, f"Expression: {expression}", (40, 65), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)
    cv2.imshow("Gesture Calculator", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
