import pygame
import cv2
import pickle
import numpy as np
import mediapipe as mp
import sys
import os
import subprocess

# =========================================================
# INITIALIZE PYGAME
# =========================================================

pygame.init()

# =========================================================
# FULLSCREEN
# =========================================================

display_info = pygame.display.Info()

WIDTH = display_info.current_w
HEIGHT = display_info.current_h

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.FULLSCREEN
)

pygame.display.set_caption(
    "ZOMBiX - Learn Gestures"
)

clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================

BACKGROUND = (7, 24, 38)
PANEL = (10, 40, 60)
PANEL_LIGHT = (15, 55, 75)

WHITE = (245, 245, 245)
GRAY = (170, 185, 195)

GREEN = (40, 220, 130)
BLUE = (70, 130, 255)
RED = (230, 70, 70)
YELLOW = (240, 200, 60)

# =========================================================
# FONTS
# =========================================================

# Scale fonts according to screen size
scale = min(WIDTH / 1100, HEIGHT / 700)

title_font = pygame.font.Font(
    None,
    max(45, int(65 * scale))
)

normal_font = pygame.font.Font(
    None,
    max(22, int(30 * scale))
)

small_font = pygame.font.Font(
    None,
    max(18, int(25 * scale))
)

gesture_font = pygame.font.Font(
    None,
    max(32, int(45 * scale))
)

# =========================================================
# GESTURE INFORMATION
# =========================================================

gestures = [
    {
        "name": "FIST",
        "gesture": "fist",
        "action": "SHOOT",
        "description": "Close your hand into a fist."
    },
    {
        "name": "OPEN PALM",
        "gesture": "palm",
        "action": "SHIELD",
        "description": "Open your hand with all fingers extended."
    },
    {
        "name": "PEACE",
        "gesture": "peace",
        "action": "SPECIAL ATTACK",
        "description": "Raise two fingers to make a V shape."
    },
    {
        "name": "THUMBS UP",
        "gesture": "like",
        "action": "RELOAD",
        "description": "Raise your thumb upward."
    }
]

current_index = 0

# =========================================================
# LOAD MACHINE LEARNING MODEL
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "gesture_model.pkl"
)

try:

    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

    model_loaded = True

    print("========================================")
    print("Gesture model loaded successfully.")
    print("Model classes:", model.classes_)
    print("========================================")

except Exception as e:

    print("========================================")
    print("Could not load gesture model.")
    print("Error:", e)
    print("========================================")

    model_loaded = False

# =========================================================
# MEDIAPIPE
# =========================================================

HAND_MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "hand_landmarker.task"
)

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = mp.tasks.vision.HandLandmarkerOptions(

    base_options=BaseOptions(
        model_asset_path=HAND_MODEL_PATH
    ),

    running_mode=VisionRunningMode.IMAGE,

    num_hands=1,

    min_hand_detection_confidence=0.3,

    min_hand_presence_confidence=0.3,

    min_tracking_confidence=0.3
)

landmarker = mp.tasks.vision.HandLandmarker.create_from_options(
    options
)

# =========================================================
# WEBCAM
# =========================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("Could not open webcam.")

else:

    print("Webcam opened successfully.")

# =========================================================
# LANDMARK NORMALIZATION
# =========================================================

def normalize_landmarks(hand_landmarks):

    points = np.array(
        [
            [landmark.x, landmark.y, landmark.z]
            for landmark in hand_landmarks
        ],
        dtype=np.float32
    )

    wrist = points[0].copy()

    points = points - wrist

    distances = np.linalg.norm(
        points,
        axis=1
    )

    max_distance = np.max(distances)

    if max_distance > 0:

        points = points / max_distance

    return points.flatten()


# =========================================================
# DRAW TEXT
# =========================================================

def draw_text(text, font, color, x, y):

    surface = font.render(
        text,
        True,
        color
    )

    screen.blit(
        surface,
        (x, y)
    )


# =========================================================
# DRAW BUTTON
# =========================================================

def draw_button(text, rect, color):

    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):

        hover_color = (
            min(color[0] + 30, 255),
            min(color[1] + 30, 255),
            min(color[2] + 30, 255)
        )

        button_color = hover_color

    else:

        button_color = color

    pygame.draw.rect(
        screen,
        button_color,
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        2,
        border_radius=10
    )

    text_surface = normal_font.render(
        text,
        True,
        WHITE
    )

    text_rect = text_surface.get_rect(
        center=rect.center
    )

    screen.blit(
        text_surface,
        text_rect
    )


# =========================================================
# BACK BUTTON
# =========================================================

back_button = pygame.Rect(
    int(WIDTH * 0.035),
    HEIGHT - int(65 * scale),
    int(180 * scale),
    int(48 * scale)
)

# =========================================================
# DRAW GESTURE CARDS
# =========================================================

def draw_gesture_card(index):

    card_x = int(WIDTH * 0.035)

    card_y = int(HEIGHT * 0.22)

    card_width = int(WIDTH * 0.29)

    card_height = int(62 * scale)

    gap = int(13 * scale)

    for i, gesture in enumerate(gestures):

        rect = pygame.Rect(
            card_x,
            card_y + i * (card_height + gap),
            card_width,
            card_height
        )

        if i == index:

            color = (20, 90, 75)

        else:

            color = PANEL

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (40, 90, 110),
            rect,
            2,
            border_radius=10
        )

        number = normal_font.render(
            str(i + 1),
            True,
            GRAY
        )

        screen.blit(
            number,
            (
                rect.x + int(15 * scale),
                rect.y + int(17 * scale)
            )
        )

        name = normal_font.render(
            gesture["name"],
            True,
            WHITE
        )

        screen.blit(
            name,
            (
                rect.x + int(50 * scale),
                rect.y + int(17 * scale)
            )
        )

        action = pygame.font.Font(
            None,
            max(18, int(25 * scale))
        ).render(
            "→ " + gesture["action"],
            True,
            GREEN
        )

        action_rect = action.get_rect(
            midright=(
                rect.right - int(12 * scale),
                rect.centery
            )
        )

        screen.blit(
            action,
            action_rect
        )


# =========================================================
# RETURN TO MAIN MENU
# =========================================================

def return_to_main_menu():

    global cap
    global landmarker

    # -----------------------------------------------------
    # RELEASE WEBCAM
    # -----------------------------------------------------

    if cap is not None:

        cap.release()

        cap = None

    # -----------------------------------------------------
    # CLOSE MEDIAPIPE
    # -----------------------------------------------------

    if landmarker is not None:

        try:

            landmarker.close()

        except Exception:
            pass

        landmarker = None

    # -----------------------------------------------------
    # CLOSE PYGAME
    # -----------------------------------------------------

    pygame.quit()

    # -----------------------------------------------------
    # FIND MAIN.PY
    # -----------------------------------------------------

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    main_path = os.path.join(
        base_dir,
        "main.py"
    )

    # -----------------------------------------------------
    # START MAIN MENU WITHOUT TERMINAL
    # -----------------------------------------------------

    if os.name == "nt":

        startupinfo = subprocess.STARTUPINFO()

        startupinfo.dwFlags |= (
            subprocess.STARTF_USESHOWWINDOW
        )

        startupinfo.wShowWindow = (
            subprocess.SW_HIDE
        )

        subprocess.Popen(
            [
                sys.executable,
                main_path
            ],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    else:

        subprocess.Popen(
            [
                sys.executable,
                main_path
            ]
        )

    # -----------------------------------------------------
    # CLOSE LEARNING PROGRAM
    # -----------------------------------------------------

    sys.exit()


# =========================================================
# MAIN LOOP
# =========================================================

running = True

detected_gesture = "NO HAND"

confidence = 0.0

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # =================================================
        # MOUSE BUTTON
        # =================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if back_button.collidepoint(
                    event.pos
                ):

                    return_to_main_menu()

        # =================================================
        # KEYBOARD
        # =================================================

        if event.type == pygame.KEYDOWN:

            # ESC → return to main menu
            if event.key == pygame.K_ESCAPE:

                return_to_main_menu()

            # RIGHT → Next gesture
            if event.key == pygame.K_RIGHT:

                current_index += 1

                if current_index >= len(gestures):

                    current_index = 0

            # LEFT → Previous gesture
            if event.key == pygame.K_LEFT:

                current_index -= 1

                if current_index < 0:

                    current_index = len(gestures) - 1

    # =====================================================
    # READ WEBCAM
    # =====================================================

    ret, frame = cap.read()

    if ret:

        frame = cv2.flip(
            frame,
            1
        )

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = landmarker.detect(
            mp_image
        )

        detected_gesture = "NO HAND"

        confidence = 0.0

        # =================================================
        # HAND DETECTED
        # =================================================

        if result.hand_landmarks:

            hand_landmarks = result.hand_landmarks[0]

            detected_gesture = "HAND DETECTED"

            height, width, _ = frame.shape

            # =================================================
            # DRAW 21 LANDMARKS
            # =================================================

            for landmark in hand_landmarks:

                x = int(
                    landmark.x * width
                )

                y = int(
                    landmark.y * height
                )

                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    (0, 255, 150),
                    -1
                )

            # =================================================
            # ML PREDICTION
            # =================================================

            if model_loaded:

                try:

                    features = normalize_landmarks(
                        hand_landmarks
                    )

                    prediction = model.predict(
                        [features]
                    )[0]

                    probabilities = model.predict_proba(
                        [features]
                    )[0]

                    confidence = float(
                        np.max(probabilities)
                    )

                    detected_gesture = str(
                        prediction
                    ).upper()

                except Exception as e:

                    print("Prediction error:")
                    print(e)

                    detected_gesture = "PREDICTION ERROR"

                    confidence = 0.0

            else:

                detected_gesture = "MODEL NOT LOADED"

            # =================================================
            # HAND BOUNDING BOX
            # =================================================

            xs = [
                int(lm.x * width)
                for lm in hand_landmarks
            ]

            ys = [
                int(lm.y * height)
                for lm in hand_landmarks
            ]

            min_x = max(
                0,
                min(xs) - 20
            )

            max_x = min(
                width,
                max(xs) + 20
            )

            min_y = max(
                0,
                min(ys) - 20
            )

            max_y = min(
                height,
                max(ys) + 20
            )

            cv2.rectangle(
                frame,
                (min_x, min_y),
                (max_x, max_y),
                (0, 255, 120),
                2
            )

        # =====================================================
        # CONVERT CAMERA TO PYGAME
        # =====================================================

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame = np.rot90(
            frame
        )

        camera_surface = pygame.surfarray.make_surface(
            frame
        )

        # =====================================================
        # CAMERA SIZE
        # =====================================================

        camera_width = int(
            WIDTH * 0.36
        )

        camera_height = int(
            HEIGHT * 0.46
        )

        camera_surface = pygame.transform.scale(
            camera_surface,
            (
                camera_width,
                camera_height
            )
        )

    else:

        detected_gesture = "CAMERA ERROR"

        confidence = 0.0

        camera_surface = None

    # =====================================================
    # DRAW SCREEN
    # =====================================================

    screen.fill(
        BACKGROUND
    )

    # =====================================================
    # TITLE
    # =====================================================

    draw_text(
        "LEARN GESTURES",
        title_font,
        WHITE,
        int(WIDTH * 0.035),
        int(HEIGHT * 0.045)
    )

    draw_text(
        "Show the gesture to the camera and check the detection.",
        normal_font,
        GRAY,
        int(WIDTH * 0.037),
        int(HEIGHT * 0.135)
    )

    # =====================================================
    # GESTURE LIST
    # =====================================================

    draw_gesture_card(
        current_index
    )

    # =====================================================
    # CAMERA PANEL
    # =====================================================

    camera_x = int(WIDTH * 0.40)

    camera_y = int(HEIGHT * 0.205)

    camera_width = int(WIDTH * 0.56)

    camera_height = int(HEIGHT * 0.49)

    camera_rect = pygame.Rect(
        camera_x,
        camera_y,
        camera_width,
        camera_height
    )

    pygame.draw.rect(
        screen,
        PANEL,
        camera_rect,
        border_radius=12
    )

    if camera_surface is not None:

        camera_display_rect = camera_surface.get_rect(
            center=camera_rect.center
        )

        screen.blit(
            camera_surface,
            camera_display_rect
        )

    # =====================================================
    # DETECTION RESULT PANEL
    # =====================================================

    result_y = int(HEIGHT * 0.72)

    result_height = int(HEIGHT * 0.085)

    result_rect = pygame.Rect(
        camera_x,
        result_y,
        camera_width,
        result_height
    )

    pygame.draw.rect(
        screen,
        PANEL_LIGHT,
        result_rect,
        border_radius=10
    )

    draw_text(
        "Detected:",
        normal_font,
        WHITE,
        result_rect.x + int(20 * scale),
        result_rect.y + int(15 * scale)
    )

    draw_text(
        detected_gesture,
        normal_font,
        GREEN,
        result_rect.x + int(125 * scale),
        result_rect.y + int(15 * scale)
    )

    confidence_text = "Confidence: {:.0f}%".format(
        confidence * 100
    )

    confidence_surface = small_font.render(
        confidence_text,
        True,
        GRAY
    )

    confidence_rect = confidence_surface.get_rect(
        midright=(
            result_rect.right - int(20 * scale),
            result_rect.centery
        )
    )

    screen.blit(
        confidence_surface,
        confidence_rect
    )

    # =====================================================
    # CURRENT GESTURE INFORMATION
    # =====================================================

    info_x = int(WIDTH * 0.035)

    info_y = int(HEIGHT * 0.735)

    draw_text(
        "Gesture:",
        small_font,
        GRAY,
        info_x,
        info_y
    )

    current = gestures[current_index]

    draw_text(
        current["name"],
        gesture_font,
        GREEN,
        info_x,
        info_y + int(25 * scale)
    )

    draw_text(
        "Action: " + current["action"],
        normal_font,
        WHITE,
        info_x + int(190 * scale),
        info_y + int(35 * scale)
    )

    draw_text(
        current["description"],
        small_font,
        GRAY,
        info_x,
        info_y + int(85 * scale)
    )

    # =====================================================
    # BACK BUTTON
    # =====================================================

    draw_button(
        "BACK",
        back_button,
        RED
    )

    # =====================================================
    # GESTURE NAVIGATION
    # =====================================================

    navigation_text = "← →  Change gesture"

    navigation_surface = small_font.render(
        navigation_text,
        True,
        GRAY
    )

    navigation_rect = navigation_surface.get_rect(
        midleft=(
            back_button.right + int(30 * scale),
            back_button.centery
        )
    )

    screen.blit(
        navigation_surface,
        navigation_rect
    )

    # =====================================================
    # UPDATE DISPLAY
    # =====================================================

    pygame.display.flip()

    clock.tick(30)


# =========================================================
# CLEANUP
# =========================================================

if cap is not None:

    cap.release()

if landmarker is not None:

    try:

        landmarker.close()

    except Exception:
        pass

pygame.quit()

sys.exit()