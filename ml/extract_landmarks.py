import os
import cv2
import mediapipe as mp
import pandas as pd
import numpy as np

# -----------------------------
# Paths
# -----------------------------
DATASET_PATH = r"dataset\selected"
OUTPUT_FILE = r"dataset\landmarks\zombix_dataset.csv"
MODEL_PATH = r"ml\hand_landmarker.task"

# -----------------------------
# Classes
# -----------------------------
CLASSES = [
    "fist",
    "palm",
    "peace",
    "like",
    "no_gesture"
]

# -----------------------------
# MediaPipe Hand Landmarker
# -----------------------------
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

# -----------------------------
# Store dataset
# -----------------------------
data = []

total_images = 0
detected_images = 0
failed_images = 0

# -----------------------------
# Process images
# -----------------------------
with HandLandmarker.create_from_options(options) as landmarker:

    for label in CLASSES:

        folder = os.path.join(DATASET_PATH, label)

        if not os.path.exists(folder):
            print(f"Folder not found: {folder}")
            continue

        images = os.listdir(folder)

        print(f"\nProcessing class: {label}")
        print(f"Images found: {len(images)}")

        for image_name in images:

            image_path = os.path.join(folder, image_name)

            # Read image
            image = cv2.imread(image_path)

            if image is None:
                failed_images += 1
                continue

            total_images += 1

            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convert to MediaPipe image
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=image_rgb
            )

            # Detect hand
            result = landmarker.detect(mp_image)

            # Check if hand detected
            if not result.hand_landmarks:
                failed_images += 1
                continue

            landmarks = result.hand_landmarks[0]

            # -----------------------------
            # Convert landmarks to NumPy
            # -----------------------------
            points = []

            for landmark in landmarks:
                points.append([
                    landmark.x,
                    landmark.y,
                    landmark.z
                ])

            points = np.array(points)

            # -----------------------------
            # Normalize
            # -----------------------------

            # Wrist = landmark 0
            wrist = points[0]

            # Move wrist to origin
            points = points - wrist

            # Find maximum distance from wrist
            distances = np.linalg.norm(points, axis=1)

            max_distance = np.max(distances)

            if max_distance > 0:
                points = points / max_distance

            # Flatten 21 landmarks × 3 values
            features = points.flatten()

            # Add label
            row = list(features) + [label]

            data.append(row)

            detected_images += 1

        print(f"Completed: {label}")

# -----------------------------
# Create DataFrame
# -----------------------------

columns = []

for i in range(21):
    columns.append(f"x{i}")
    columns.append(f"y{i}")
    columns.append(f"z{i}")

columns.append("label")

df = pd.DataFrame(data, columns=columns)

# -----------------------------
# Create output directory
# -----------------------------

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

# -----------------------------
# Save CSV
# -----------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# -----------------------------
# Final result
# -----------------------------

print("\n====================================")
print("LANDMARK EXTRACTION COMPLETED")
print("====================================")

print(f"Total images processed : {total_images}")
print(f"Hands detected         : {detected_images}")
print(f"Images skipped         : {failed_images}")
print(f"Dataset rows           : {len(df)}")
print(f"Features per image     : 63")
print(f"Output file            : {OUTPUT_FILE}")