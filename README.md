# 🧟 ZOMBiX – ML-Based Hand Gesture Zombie Survival Game

**ZOMBiX** is a machine learning-based zombie survival game that allows players to control game actions using real-time hand gestures through a webcam.

Instead of using a traditional keyboard or mouse for combat actions, players can use hand gestures to shoot zombies, activate shields, perform special attacks, and reload weapons.

The project combines Machine Learning, Computer Vision, and Game Development to create an interactive gaming experience.

## 🎮 Features

- Real-time hand gesture detection using a webcam.
- Hand landmark detection using MediaPipe.
- Machine learning-based gesture classification.
- Random Forest Classifier for gesture prediction.
- Interactive zombie survival gameplay.
- Gesture-controlled shooting, shielding, special attacks, and reloading.
- Real-time gesture prediction and confidence display.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Webcam access and image processing |
| MediaPipe | Hand landmark detection |
| Scikit-learn | Machine learning model |
| Random Forest | Gesture classification |
| Pygame | Game development |
| NumPy | Numerical operations |
| Pickle | Saving and loading trained model |

## 🧠 Machine Learning Model

ZOMBiX uses a **Random Forest Classifier** to recognize different hand gestures.

### How it works

1. Webcam captures the player's hand.
2. MediaPipe detects 21 hand landmarks.
3. Landmark coordinates (X, Y, Z) are extracted.
4. Coordinates are normalized and converted into 63 numerical features.
5. The trained Random Forest model predicts the gesture.
6. The predicted gesture triggers the corresponding game action.

### Supported Gestures

| Hand Gesture | Game Action |
|---|---|
| ✊ Fist | Shoot |
| ✋ Open Palm | Shield |
| ✌️ Peace | Special Attack |
| 👍 Thumbs Up | Reload |
| No Gesture | No Action |

## 📂 Project Structure

```text
ZOMBiX/
│
├── game/
│   └── gesture_game.py
│
├── ml/
│   ├── extract_landmarks.py
│   ├── gesture_model.pkl
│   └── hand_landmarker.task
│
├── .gitignore
├── README.md
└── requirements.txt
```

*Note: Update this structure if your actual project contains additional files or folders.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/pawanpawar154/ZOMBiX.git
```

### 2. Navigate to the project folder

```bash
cd ZOMBiX
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install opencv-python mediapipe pygame numpy scikit-learn
```

### 6. Run the game

```bash
python game/gesture_game.py
```

Make sure your webcam is connected and the required model files are present.

## 🎯 Project Objectives

- To develop a gesture-controlled gaming system.
- To implement machine learning for real-time hand gesture recognition.
- To integrate computer vision with interactive game development.
- To explore practical applications of machine learning and human-computer interaction.

## 🚀 Future Scope

- Add multiple zombie types and difficulty levels.
- Improve gesture recognition accuracy.
- Introduce multiple game stages and environments.
- Add player scoring and leaderboard functionality.
- Support more hand gestures and game controls.

## 👨‍💻 Developer

**Developed as an AI & ML project.**

**Project Name:** ZOMBiX – ML-Based Hand Gesture Zombie Survival Game

---

⭐ If you find this project interesting, consider giving the repository a star!