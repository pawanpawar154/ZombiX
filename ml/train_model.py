import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# =========================================================
# FILE PATHS
# =========================================================

DATASET_PATH = r"dataset\landmarks\zombix_dataset.csv"

MODEL_PATH = r"ml\gesture_model.pkl"


# =========================================================
# LOAD DATASET
# =========================================================

print("Loading landmark dataset...")

data = pd.read_csv(DATASET_PATH)

print("Dataset loaded.")
print("Total samples:", len(data))


# =========================================================
# SEPARATE FEATURES AND LABEL
# =========================================================

X = data.drop("label", axis=1)

y = data["label"]


print("Features:", X.shape)
print("Classes:", sorted(y.unique()))


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# =========================================================
# RANDOM FOREST MODEL
# =========================================================

print("\nTraining Random Forest...")

model = RandomForestClassifier(

    n_estimators=150,

    random_state=42,

    n_jobs=-1
)


model.fit(
    X_train,
    y_train
)


print("Training completed.")


# =========================================================
# TEST MODEL
# =========================================================

predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n========================================")
print("MODEL ACCURACY")
print("========================================")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


# =========================================================
# CLASSIFICATION REPORT
# =========================================================

print("\n========================================")
print("CLASSIFICATION REPORT")
print("========================================")

print(
    classification_report(
        y_test,
        predictions
    )
)


# =========================================================
# CONFUSION MATRIX
# =========================================================

print("\n========================================")
print("CONFUSION MATRIX")
print("========================================")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)


# =========================================================
# SAVE MODEL
# =========================================================

print("\nSaving model...")

with open(
    MODEL_PATH,
    "wb"
) as file:

    pickle.dump(
        model,
        file,
        protocol=pickle.HIGHEST_PROTOCOL
    )


print("\n========================================")
print("MODEL SAVED SUCCESSFULLY")
print("========================================")

print(
    "Location:",
    MODEL_PATH
)

print(
    "Classes:",
    model.classes_
)

print("========================================")