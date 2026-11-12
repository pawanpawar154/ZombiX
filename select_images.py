import os
import shutil
import random

# =====================================================
# PATHS
# =====================================================

SOURCE = r"C:\Users\003\Downloads\hagrid-sample-120k-384p\hagrid_120k"

DESTINATION = r"dataset\selected"


# =====================================================
# DATASET SETTINGS
# =====================================================

SAMPLES_PER_CLASS = 500

# Main ZombiX gestures
MAIN_CLASSES = {
    "train_val_fist": "fist",
    "train_val_palm": "palm",
    "train_val_peace": "peace",
    "train_val_like": "like"
}


# Gestures that will be used as no_gesture
NO_GESTURE_CLASSES = {
    "train_val_rock": 100,
    "train_val_ok": 100,
    "train_val_one": 100,
    "train_val_three": 100,
    "train_val_four": 100
}


# Make selection reproducible
random.seed(42)


# =====================================================
# CREATE DESTINATION FOLDERS
# =====================================================

os.makedirs(DESTINATION, exist_ok=True)

for class_name in ["fist", "palm", "peace", "like", "no_gesture"]:
    os.makedirs(
        os.path.join(DESTINATION, class_name),
        exist_ok=True
    )


# =====================================================
# FUNCTION TO GET IMAGES
# =====================================================

def get_images(folder):

    if not os.path.exists(folder):
        print("ERROR: Folder not found:")
        print(folder)
        return []

    images = []

    for file in os.listdir(folder):

        if file.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            images.append(file)

    return images


# =====================================================
# FUNCTION TO COPY IMAGES
# =====================================================

def copy_images(source_folder, destination_folder, amount):

    images = get_images(source_folder)

    print("\nFolder:", source_folder)
    print("Images available:", len(images))

    if len(images) < amount:

        print(
            f"ERROR: Only {len(images)} images available. "
            f"Need {amount}."
        )

        return False

    selected = random.sample(images, amount)

    for number, image in enumerate(selected, start=1):

        source_file = os.path.join(
            source_folder,
            image
        )

        extension = os.path.splitext(image)[1]

        destination_file = os.path.join(
            destination_folder,
            f"{number:04d}{extension}"
        )

        shutil.copy2(
            source_file,
            destination_file
        )

    return True


# =====================================================
# SELECT MAIN GESTURES
# =====================================================

print("\n======================================")
print("Selecting ZombiX main gestures")
print("======================================")

for source_class, output_class in MAIN_CLASSES.items():

    source_folder = os.path.join(
        SOURCE,
        source_class
    )

    destination_folder = os.path.join(
        DESTINATION,
        output_class
    )

    success = copy_images(
        source_folder,
        destination_folder,
        SAMPLES_PER_CLASS
    )

    if success:
        print(
            f"✓ {output_class}: "
            f"{SAMPLES_PER_CLASS} images copied"
        )


# =====================================================
# SELECT NO-GESTURE DATA
# =====================================================

print("\n======================================")
print("Creating no_gesture class")
print("======================================")

no_gesture_number = 1

for source_class, amount in NO_GESTURE_CLASSES.items():

    source_folder = os.path.join(
        SOURCE,
        source_class
    )

    images = get_images(source_folder)

    print(
        f"\n{source_class}: "
        f"{len(images)} images available"
    )

    if len(images) < amount:

        print(
            f"ERROR: Not enough images in "
            f"{source_class}"
        )

        continue

    selected = random.sample(
        images,
        amount
    )

    destination_folder = os.path.join(
        DESTINATION,
        "no_gesture"
    )

    for image in selected:

        source_file = os.path.join(
            source_folder,
            image
        )

        extension = os.path.splitext(image)[1]

        destination_file = os.path.join(
            destination_folder,
            f"{no_gesture_number:04d}{extension}"
        )

        shutil.copy2(
            source_file,
            destination_file
        )

        no_gesture_number += 1

    print(
        f"✓ Added {amount} images "
        f"to no_gesture"
    )


# =====================================================
# FINAL RESULT
# =====================================================

print("\n======================================")
print("ZombiX DATASET CREATED")
print("======================================")

total = 0

for class_name in [
    "fist",
    "palm",
    "peace",
    "like",
    "no_gesture"
]:

    folder = os.path.join(
        DESTINATION,
        class_name
    )

    count = len([
        file for file in os.listdir(folder)
        if file.lower().endswith(
            (".jpg", ".jpeg", ".png")
        )
    ])

    print(
        f"{class_name:12} : {count}"
    )

    total += count


print("--------------------------------------")
print(f"TOTAL        : {total}")
print("--------------------------------------")