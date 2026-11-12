import pygame
import cv2
import pickle
import numpy as np
import mediapipe as mp
import os
import sys


# =========================================================
# INITIALIZE PYGAME
# =========================================================

pygame.init()

WIDTH = 1100
HEIGHT = 700

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "ZOMBiX - Real-Time Gesture Detection"
)

clock = pygame.time.Clock()


# =========================================================
# COLORS
# =========================================================

BACKGROUND = (5, 20, 32)
PANEL = (8, 40, 58)
PANEL_LIGHT = (12, 55, 75)

WHITE = (245, 245, 245)
GRAY = (170, 185, 195)

GREEN = (40, 220, 130)
RED = (235, 70, 70)
BLUE = (70, 140, 255)
YELLOW = (240, 200, 60)


# =========================================================
# FONTS
# =========================================================

title_font = pygame.font.Font(
    None,
    65
)

heading_font = pygame.font.Font(
    None,
    38
)

normal_font = pygame.font.Font(
    None,
    30
)

small_font = pygame.font.Font(
    None,
    24
)

gesture_font = pygame.font.Font(
    None,
    48
)


# =========================================================
# PROJECT PATH
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


HAND_MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "hand_landmarker.task"
)


# =========================================================
# LOAD RANDOM FOREST MODEL
# =========================================================

try:

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        model = pickle.load(file)

    model_loaded = True

    print("Gesture model loaded.")
    print(
        "Classes:",
        model.classes_
    )

except Exception as e:

    print("Could not load gesture model.")
    print(e)

    model_loaded = False


# =========================================================
# MEDIAPIPE
# =========================================================

BaseOptions = mp.tasks.BaseOptions

RunningMode = mp.tasks.vision.RunningMode


options = mp.tasks.vision.HandLandmarkerOptions(

    base_options=BaseOptions(
        model_asset_path=HAND_MODEL_PATH
    ),

    running_mode=RunningMode.IMAGE,

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

    pygame.quit()

    sys.exit()


# =========================================================
# NORMALIZE LANDMARKS
# =========================================================

def normalize_landmarks(hand_landmarks):

    points = np.array(
        [
            [
                landmark.x,
                landmark.y,
                landmark.z
            ]

            for landmark in hand_landmarks
        ],

        dtype=np.float32
    )

    # Wrist
    wrist = points[0].copy()

    # Move wrist to origin
    points = points - wrist

    # Scale
    distances = np.linalg.norm(
        points,
        axis=1
    )

    max_distance = np.max(
        distances
    )

    if max_distance > 0:

        points = points / max_distance

    return points.flatten()


# =========================================================
# GESTURE ACTION
# =========================================================

def get_action(gesture):

    actions = {

        "fist": "SHOOT",

        "palm": "SHIELD",

        "peace": "SPECIAL ATTACK",

        "like": "RELOAD",

        "no_gesture": "NEUTRAL"
    }

    return actions.get(
        gesture,
        "NEUTRAL"
    )


# =========================================================
# DRAW TEXT
# =========================================================

def draw_text(
    text,
    font,
    color,
    x,
    y
):

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
# MAIN LOOP
# =========================================================

running = True

gesture = "NO HAND"

confidence = 0.0

action = "NONE"

camera_surface = None


while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False


    # =====================================================
    # CAMERA
    # =====================================================

    ret, frame = cap.read()

    if ret:

        # Mirror camera
        frame = cv2.flip(
            frame,
            1
        )

        # RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hand
        result = landmarker.detect(
            mp_image
        )

        # Default
        gesture = "NO HAND"

        confidence = 0.0

        action = "NONE"


        # =================================================
        # HAND DETECTED
        # =================================================

        if result.hand_landmarks:

            hand_landmarks = result.hand_landmarks[0]

            height, width, _ = frame.shape


            # =============================================
            # DRAW LANDMARKS
            # =============================================

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


            # =============================================
            # PREDICTION
            # =============================================

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
                        np.max(
                            probabilities
                        )
                    )

                    gesture = str(
                        prediction
                    ).upper()

                    action = get_action(
                        prediction
                    )

                except Exception as e:

                    print(
                        "Prediction error:",
                        e
                    )

                    gesture = "ERROR"

                    confidence = 0.0

                    action = "NONE"


            # =============================================
            # BOUNDING BOX
            # =============================================

            xs = [
                int(
                    landmark.x * width
                )

                for landmark in hand_landmarks
            ]

            ys = [
                int(
                    landmark.y * height
                )

                for landmark in hand_landmarks
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


        # =================================================
        # CAMERA TO PYGAME
        # =================================================

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

        camera_surface = pygame.transform.scale(
            camera_surface,
            (650, 490)
        )


    # =====================================================
    # DRAW BACKGROUND
    # =====================================================

    screen.fill(
        BACKGROUND
    )


    # =====================================================
    # TITLE
    # =====================================================

    draw_text(
        "REAL-TIME GESTURE DETECTION",
        title_font,
        WHITE,
        35,
        30
    )

    draw_text(
        "Show your hand to the webcam",
        normal_font,
        GRAY,
        38,
        100
    )


    # =====================================================
    # CAMERA PANEL
    # =====================================================

    camera_rect = pygame.Rect(
        35,
        150,
        670,
        510
    )

    pygame.draw.rect(
        screen,
        PANEL,
        camera_rect,
        border_radius=15
    )


    if camera_surface is not None:

        screen.blit(
            camera_surface,
            (45, 160)
        )


    # =====================================================
    # INFORMATION PANEL
    # =====================================================

    info_rect = pygame.Rect(
        735,
        150,
        330,
        510
    )

    pygame.draw.rect(
        screen,
        PANEL,
        info_rect,
        border_radius=15
    )


    # =====================================================
    # WEBCAM STATUS
    # =====================================================

    draw_text(
        "Webcam Feed",
        heading_font,
        WHITE,
        765,
        180
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (1020, 195),
        7
    )


    # =====================================================
    # LANDMARK COUNT
    # =====================================================

    draw_text(
        "Hand Landmarks",
        normal_font,
        GRAY,
        765,
        245
    )

    draw_text(
        "21",
        heading_font,
        GREEN,
        765,
        280
    )


    # =====================================================
    # PREDICTION
    # =====================================================

    draw_text(
        "Prediction",
        normal_font,
        GRAY,
        765,
        350
    )

    draw_text(
        gesture,
        gesture_font,
        GREEN,
        765,
        385
    )


    # =====================================================
    # CONFIDENCE
    # =====================================================

    draw_text(
        "Confidence",
        normal_font,
        GRAY,
        765,
        455
    )

    draw_text(
        "{:.1f}%".format(
            confidence * 100
        ),
        heading_font,
        WHITE,
        765,
        490
    )


    # =====================================================
    # ACTION
    # =====================================================

    draw_text(
        "Action",
        normal_font,
        GRAY,
        765,
        550
    )

    draw_text(
        action,
        normal_font,
        GREEN,
        765,
        590
    )


    # =====================================================
    # FOOTER
    # =====================================================

    draw_text(
        "ESC  Back",
        small_font,
        GRAY,
        930,
        665
    )


    pygame.display.flip()

    clock.tick(30)


# =========================================================
# CLEANUP
# =========================================================

cap.release()

landmarker.close()

pygame.quit()

sys.exit()