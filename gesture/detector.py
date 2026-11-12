import cv2
import mediapipe as mp
import numpy as np
import joblib


# ---------------------------------------
# Load trained ML model
# ---------------------------------------

MODEL_PATH = r"ml\gesture_model.pkl"
model = joblib.load(MODEL_PATH)

print("Gesture model loaded!")


# ---------------------------------------
# MediaPipe Hand Landmarker
# ---------------------------------------

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

MODEL_PATH_HAND = r"ml\hand_landmarker.task"

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH_HAND
    ),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

landmarker = HandLandmarker.create_from_options(options)


# ---------------------------------------
# Open webcam
# ---------------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    exit()


print("Webcam started!")
print("Show your hand to the camera.")
print("Press Q to quit.")


frame_timestamp = 0


# ---------------------------------------
# Main loop
# ---------------------------------------

while True:

    success, frame = cap.read()

    if not success:
        print("Could not read webcam frame.")
        break

    # Flip camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
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
    result = landmarker.detect_for_video(
        mp_image,
        frame_timestamp
    )

    frame_timestamp += 1


    # -----------------------------------
    # If hand detected
    # -----------------------------------

    if result.hand_landmarks:

        landmarks = result.hand_landmarks[0]

        points = []

        for landmark in landmarks:

            points.append([
                landmark.x,
                landmark.y,
                landmark.z
            ])

        points = np.array(points)


        # --------------------------------
        # Normalize landmarks
        # --------------------------------

        wrist = points[0]

        points = points - wrist

        distances = np.linalg.norm(
            points,
            axis=1
        )

        max_distance = np.max(distances)

        if max_distance > 0:

            points = points / max_distance


        # --------------------------------
        # Convert to ML features
        # --------------------------------

        features = points.flatten()

        features = features.reshape(1, -1)


        # --------------------------------
        # Predict gesture
        # --------------------------------

        prediction = model.predict(features)[0]

        probability = model.predict_proba(
            features
        )[0]

        confidence = np.max(probability)


        # --------------------------------
        # Display result
        # --------------------------------

        text = f"{prediction.upper()}  {confidence * 100:.1f}%"

        cv2.putText(
            frame,
            text,
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )


        # --------------------------------
        # Draw landmarks
        # --------------------------------

        height, width, _ = frame.shape

        for landmark in landmarks:

            x = int(landmark.x * width)
            y = int(landmark.y * height)

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

    else:

        cv2.putText(
            frame,
            "NO HAND",
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 255),
            3
        )


    # -----------------------------------
    # Show webcam
    # -----------------------------------

    cv2.imshow(
        "ZombiX - Gesture Detector",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ---------------------------------------
# Cleanup
# ---------------------------------------

cap.release()

cv2.destroyAllWindows()

landmarker.close()

print("Gesture detector stopped.")