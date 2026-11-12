import os
import cv2
import pygame
import sys
import subprocess
import random
import pickle
import math
import mediapipe as mp

from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    MOUSEBUTTONDOWN
)


# ============================================================
# PATHS
# ============================================================

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

ASSET_DIR = os.path.join(
    BASE_DIR,
    "assets"
)


# ============================================================
# ASSET PATHS
# ============================================================

GAME_BG_PATH = os.path.join(
    ASSET_DIR,
    "backgrounds",
    "game_bg.png"
)

GAME_OVER_BG_PATH = os.path.join(
    ASSET_DIR,
    "backgrounds",
    "game_over_bg.png"
)

PLAYER_PATH = os.path.join(
    ASSET_DIR,
    "player",
    "player.png"
)

ZOMBIE_PATH = os.path.join(
    ASSET_DIR,
    "zombie",
    "zombie.png"
)

# Zombie walking animation frames.
ZOMBIE_WALK_DIR = os.path.join(
    ASSET_DIR,
    "zombie"
)

ZOMBIE_WALK_PATHS = [
    os.path.join(
        ZOMBIE_WALK_DIR,
        f"walk_{i:02d}.png"
    )
    for i in range(1, 9)
]

BULLET_PATH = os.path.join(
    ASSET_DIR,
    "effects",
    "bullet.png"
)

MUZZLE_PATH = os.path.join(
    ASSET_DIR,
    "effects",
    "muzzle_flash.png"
)

RELOAD_PATH = os.path.join(
    ASSET_DIR,
    "effects",
    "reload_effect.png"
)

SHIELD_PATH = os.path.join(
    ASSET_DIR,
    "effects",
    "shield.png"
)

SPECIAL_PATH = os.path.join(
    ASSET_DIR,
    "effects",
    "special_attack.png"
)

DEATH_PATH = os.path.join(
    ASSET_DIR,
    "effects",
    "zombie_death.png"
)

HEART_PATH = os.path.join(
    ASSET_DIR,
    "ui",
    "heart.png"
)

EMPTY_HEART_PATH = os.path.join(
    ASSET_DIR,
    "ui",
    "heart_empty.png"
)

PAUSE_PATH = os.path.join(
    ASSET_DIR,
    "buttons",
    "pause.png"
)


# ============================================================
# PYGAME SETUP
# ============================================================

pygame.init()

display_info = pygame.display.Info()

WIDTH = display_info.current_w
HEIGHT = display_info.current_h

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.FULLSCREEN
)
pygame.display.set_caption(
    "ZOMBiX - Gesture Controlled Zombie Survival"
)

clock = pygame.time.Clock()


# ============================================================
# GAME AREA
# ============================================================

TOP_BAR_HEIGHT = 120
BOTTOM_BAR_HEIGHT = 85

GAME_TOP = TOP_BAR_HEIGHT
GAME_BOTTOM = HEIGHT - BOTTOM_BAR_HEIGHT

GAME_HEIGHT = GAME_BOTTOM - GAME_TOP


# ============================================================
# COLORS
# ============================================================

BLACK = (8, 10, 15)
DARK = (14, 19, 27)
PANEL = (20, 27, 36)

WHITE = (240, 240, 240)
GRAY = (160, 165, 175)

GREEN = (60, 220, 120)
DARK_GREEN = (25, 100, 60)

RED = (230, 60, 70)
DARK_RED = (120, 30, 35)

BLUE = (70, 150, 255)
CYAN = (60, 220, 255)

YELLOW = (250, 210, 70)
PURPLE = (180, 100, 255)

ORANGE = (255, 140, 50)


# ============================================================
# FONTS
# ============================================================

FONT_SMALL = pygame.font.SysFont(
    "arial",
    17
)

FONT_NORMAL = pygame.font.SysFont(
    "arial",
    23
)

FONT_MEDIUM = pygame.font.SysFont(
    "arial",
    30,
    bold=True
)

FONT_LARGE = pygame.font.SysFont(
    "arial",
    48,
    bold=True
)

FONT_TITLE = pygame.font.SysFont(
    "arial",
    64,
    bold=True
)


# ============================================================
# IMAGE LOADER
# ============================================================

def load_image(path, size=None):

    try:

        image = pygame.image.load(
            path
        ).convert_alpha()

        if size is not None:

            image = pygame.transform.smoothscale(
                image,
                size
            )

        print(
            "Loaded:",
            os.path.basename(path)
        )

        return image

    except Exception as e:

        print(
            "Could not load image:",
            path
        )

        print(e)

        return None


# ============================================================
# LOAD GAME ASSETS
# ============================================================

game_background = load_image(
    GAME_BG_PATH,
    (WIDTH, GAME_HEIGHT)
)

game_over_background = load_image(
    GAME_OVER_BG_PATH,
    (WIDTH, HEIGHT)
)

player_image = load_image(
    PLAYER_PATH,
    (110, 135)
)

zombie_image = load_image(
    ZOMBIE_PATH,
    (90, 110)
)

zombie_walk_frames = []

for walk_path in ZOMBIE_WALK_PATHS:
    image = load_image(
        walk_path,
        (100, 120)
    )

    if image is not None:
        zombie_walk_frames.append(image)

if zombie_walk_frames:
    print(
        f"Zombie animation loaded: "
        f"{len(zombie_walk_frames)} frames."
    )
else:
    print(
        "Zombie animation frames not found. "
        "Using zombie.png."
    )

bullet_image = load_image(
    BULLET_PATH,
    (30, 15)
)

muzzle_image = load_image(
    MUZZLE_PATH,
    (65, 55)
)

reload_image = load_image(
    RELOAD_PATH,
    (90, 90)
)

shield_image = load_image(
    SHIELD_PATH,
    (145, 145)
)

special_image = load_image(
    SPECIAL_PATH,
    (330, 330)
)

death_image = load_image(
    DEATH_PATH,
    (110, 110)
)

heart_image = load_image(
    HEART_PATH,
    (30, 30)
)

empty_heart_image = load_image(
    EMPTY_HEART_PATH,
    (30, 30)
)

pause_image = load_image(
    PAUSE_PATH,
    (45, 45)
)


# ============================================================
# GAME OVER BUTTONS
# ============================================================

BUTTON_WIDTH = 500
BUTTON_HEIGHT = 75
BUTTON_X = (WIDTH - BUTTON_WIDTH) // 2

GAME_OVER_PLAY_BUTTON = pygame.Rect(
    BUTTON_X,
    500,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

GAME_OVER_BACK_BUTTON = pygame.Rect(
    BUTTON_X,
    590,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

# ============================================================
# PAUSE SCREEN BUTTONS
# ============================================================

PAUSE_BUTTON_WIDTH = 500
PAUSE_BUTTON_HEIGHT = 75
PAUSE_BUTTON_X = (WIDTH - PAUSE_BUTTON_WIDTH) // 2

PAUSE_RESUME_BUTTON = pygame.Rect(
    PAUSE_BUTTON_X,
    370,
    PAUSE_BUTTON_WIDTH,
    PAUSE_BUTTON_HEIGHT
)

PAUSE_MENU_BUTTON = pygame.Rect(
    PAUSE_BUTTON_X,
    465,
    PAUSE_BUTTON_WIDTH,
    PAUSE_BUTTON_HEIGHT
)

# ============================================================
# LOAD ML MODEL
# ============================================================

model = None

try:

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        model = pickle.load(file)

    print(
        "Gesture model loaded successfully."
    )

    print(
        "Classes:",
        model.classes_
    )

except Exception as e:

    print(
        "ERROR loading gesture model:"
    )

    print(e)


# ============================================================
# MEDIAPIPE
# ============================================================

landmarker = None

try:

    BaseOptions = mp.tasks.BaseOptions

    VisionRunningMode = (
        mp.tasks.vision.RunningMode
    )

    HandLandmarker = (
        mp.tasks.vision.HandLandmarker
    )

    HandLandmarkerOptions = (
        mp.tasks.vision.HandLandmarkerOptions
    )

    options = HandLandmarkerOptions(

        base_options=BaseOptions(
            model_asset_path=HAND_MODEL_PATH
        ),

        running_mode=VisionRunningMode.IMAGE,

        num_hands=1,

        min_hand_detection_confidence=0.5,

        min_hand_presence_confidence=0.5,

        min_tracking_confidence=0.5
    )

    landmarker = (
        HandLandmarker.create_from_options(
            options
        )
    )

    print(
        "MediaPipe hand landmarker loaded."
    )

except Exception as e:

    print(
        "ERROR loading MediaPipe:"
    )

    print(e)


# ============================================================
# CAMERA
# ============================================================

camera = cv2.VideoCapture(0)

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
)


# ============================================================
# GAME VARIABLES
# ============================================================

player_x = WIDTH // 2

player_y = (
    GAME_TOP +
    GAME_HEIGHT // 2
)

PLAYER_SPEED = 6

health = 100

max_health = 100

ammo = 12

max_ammo = 12

score = 0

kills = 0

wave = 1

game_over = False

paused = False


# ============================================================
# GESTURE VARIABLES
# ============================================================

current_gesture = "no_gesture"

confidence = 0.0

last_action = "READY"

shield_active = False

gesture_cooldown = 0

special_cooldown = 0

reload_cooldown = 0


# ============================================================
# VISUAL EFFECT VARIABLES
# ============================================================
muzzle_timer = 0
reload_timer = 0
special_timer = 0

# Player damage effect
player_hit_timer = 0


# ============================================================
# EFFECT LISTS
# ============================================================

death_effects = []


# ============================================================
# ZOMBIES / BULLETS
# ============================================================

zombies = []

bullets = []

spawn_timer = 0

MAX_ZOMBIES = 4


# ============================================================
# ZOMBIE CLASS
# ============================================================

# ============================================================
# ZOMBIE CLASS
# ============================================================

class Zombie:

    def __init__(self):

        side = random.choice([
            "right",
            "left"
        ])

        if side == "right":

            self.x = WIDTH + 70

            self.y = random.randint(
                GAME_TOP + 70,
                GAME_BOTTOM - 70
            )

        else:

            self.x = -70

            self.y = random.randint(
                GAME_TOP + 70,
                GAME_BOTTOM - 70
            )

        self.speed = (
            35 +
            wave * 4
        )

        self.health = (
            2 +
            wave // 3
        )

        self.radius = 30

        # Animation state
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.095

        self.facing_left = False

        # Hit reaction
        self.hit_timer = 0.0

    def update(self, dt):

        if self.hit_timer > 0:

            self.hit_timer -= dt

        if self.hit_timer < 0:
            self.hit_timer = 0


        dx = player_x - self.x
        dy = player_y - self.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance > 0:

            self.facing_left = dx < 0

            move_distance = self.speed * dt

            self.x += (
                dx / distance
            ) * move_distance

            self.y += (
                dy / distance
            ) * move_distance

        # Walking animation
        if zombie_walk_frames and distance > 1:

            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:

                self.animation_timer -= self.animation_speed

                self.animation_frame = (
                    self.animation_frame + 1
                ) % len(zombie_walk_frames)

    def draw(self):

        image = None

        if zombie_walk_frames:

            image = zombie_walk_frames[
                self.animation_frame
            ]

        elif zombie_image is not None:

            image = zombie_image

        if image is not None:

            if self.facing_left:

                image = pygame.transform.flip(
                    image,
                    True,
                    False
                )

            rect = image.get_rect(
                center=(
                    int(self.x),
                    int(self.y)
                )
            )

            screen.blit(
                image,
                rect
            )

                        # White hit flash
            if self.hit_timer > 0:

                flash = pygame.Surface(
                    image.get_size(),
                    pygame.SRCALPHA
                )

                flash.fill(
                    (
                        255,
                        255,
                        255,
                        150
                    )
                )

                screen.blit(
                    flash,
                    rect
                )

        else:

            pygame.draw.circle(
                screen,
                DARK_GREEN,
                (
                    int(self.x),
                    int(self.y)
                ),
                self.radius
            )

        max_zombie_health = max(
            2,
            2 + wave // 3
        )

        bar_width = 55

        health_width = int(
            bar_width *
            max(
                0,
                self.health
            ) /
            max_zombie_health
        )

        pygame.draw.rect(
            screen,
            DARK_RED,
            (
                int(self.x - 27),
                int(self.y - 65),
                bar_width,
                5
            )
        )

        pygame.draw.rect(
            screen,
            RED,
            (
                int(self.x - 27),
                int(self.y - 65),
                health_width,
                5
            )
        )


# ============================================================
# BULLET CLASS
# ============================================================
# ============================================================
# BULLET CLASS
# ============================================================

class Bullet:

    def __init__(
        self,
        x,
        y,
        target
    ):

        self.x = x

        self.y = y

        dx = target.x - x

        dy = target.y - y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance == 0:

            distance = 1

        self.dx = dx / distance

        self.dy = dy / distance

        self.speed = 14

        self.radius = 6

    def update(self, dt):

        self.x += (
            self.dx *
            self.speed *
            dt *
            60
        )

        self.y += (
            self.dy *
            self.speed *
            dt *
            60
        )

    def draw(self):

        if bullet_image is not None:

            angle = math.degrees(
                math.atan2(
                    -self.dy,
                    self.dx
                )
            )

            image = pygame.transform.rotate(
                bullet_image,
                angle
            )

            rect = image.get_rect(
                center=(
                    int(self.x),
                    int(self.y)
                )
            )

            screen.blit(
                image,
                rect
            )

        else:

            pygame.draw.circle(
                screen,
                YELLOW,
                (
                    int(self.x),
                    int(self.y)
                ),
                self.radius
            )


# ============================================================
# NORMALIZE LANDMARKS
# ============================================================

def normalize_landmarks(
    hand_landmarks
):

    wrist = hand_landmarks[0]

    points = []

    for landmark in hand_landmarks:

        x = (
            landmark.x -
            wrist.x
        )

        y = (
            landmark.y -
            wrist.y
        )

        z = (
            landmark.z -
            wrist.z
        )

        points.append(
            [
                x,
                y,
                z
            ]
        )

    max_distance = 0

    for point in points:

        distance = math.sqrt(
            point[0] ** 2 +
            point[1] ** 2 +
            point[2] ** 2
        )

        if distance > max_distance:

            max_distance = distance

    if max_distance == 0:

        max_distance = 1

    normalized = []

    for point in points:

        normalized.append(
            [
                point[0] /
                max_distance,

                point[1] /
                max_distance,

                point[2] /
                max_distance
            ]
        )

    return normalized


# ============================================================
# DETECT GESTURE
# ============================================================

def detect_gesture(frame):

    global current_gesture

    global confidence

    if (
        landmarker is None
        or
        model is None
    ):

        current_gesture = "no_gesture"

        confidence = 0

        return None, None

    try:

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = landmarker.detect(
            mp_image
        )

        if not result.hand_landmarks:

            current_gesture = (
                "no_gesture"
            )

            confidence = 0

            return None, None

        hand = (
            result.hand_landmarks[0]
        )

        normalized = (
            normalize_landmarks(
                hand
            )
        )

        features = []

        for point in normalized:

            features.extend(
                point
            )

        prediction = model.predict(
            [features]
        )[0]

        probabilities = (
            model.predict_proba(
                [features]
            )[0]
        )

        confidence_value = max(
            probabilities
        )

        current_gesture = (
            prediction
        )

        confidence = (
            confidence_value
        )

        wrist = hand[0]

        return wrist, hand

    except Exception as e:

        print(
            "Gesture detection error:",
            e
        )

        current_gesture = (
            "no_gesture"
        )

        confidence = 0

        return None, None


# ============================================================
# CREATE DEATH EFFECT
# ============================================================

def create_death_effect(
    x,
    y
):

    death_effects.append(
        {
            "x": x,
            "y": y,
            "timer": 25
        }
    )


# ============================================================
# SHOOT
# ============================================================

def shoot():

    global ammo

    global last_action

    global muzzle_timer

    if ammo <= 0:

        last_action = "NO AMMO"

        return

    if len(zombies) == 0:

        last_action = "NO TARGET"

        return

    target = min(
        zombies,
        key=lambda z:
        math.sqrt(
            (z.x - player_x) ** 2 +
            (z.y - player_y) ** 2
        )
    )

    bullet = Bullet(
        player_x + 35,
        player_y - 5,
        target
    )

    bullets.append(
        bullet
    )

    ammo -= 1

    muzzle_timer = 8

    last_action = "SHOOT"


# ============================================================
# RELOAD
# ============================================================

def reload_weapon():

    global ammo

    global last_action

    global reload_timer

    ammo = max_ammo

    reload_timer = 30

    last_action = "RELOAD"


# ============================================================
# SPECIAL ATTACK
# ============================================================

def special_attack():

    global score

    global kills

    global special_cooldown

    global last_action

    global special_timer

    if special_cooldown > 0:

        last_action = (
            "SPECIAL COOLDOWN"
        )

        return

    radius = 190

    killed = []

    for zombie in zombies:

        distance = math.sqrt(
            (zombie.x - player_x) ** 2 +
            (zombie.y - player_y) ** 2
        )

        if distance <= radius:

            zombie.health -= 5

            if zombie.health <= 0:

                killed.append(
                    zombie
                )

    for zombie in killed:

        if zombie in zombies:

            zombies.remove(
                zombie
            )

            create_death_effect(
                zombie.x,
                zombie.y
            )

            score += 25

            kills += 1

    special_cooldown = 120

    special_timer = 35

    last_action = (
        "SPECIAL ATTACK"
    )


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global player_x
    global player_y
    global health
    global ammo
    global score
    global kills
    global wave
    global zombies
    global bullets
    global spawn_timer
    global game_over
    global current_gesture
    global confidence
    global last_action
    global shield_active
    global paused
    global muzzle_timer
    global reload_timer
    global special_timer
    global gesture_cooldown
    global special_cooldown
    global reload_cooldown
    global death_effects
    global player_hit_timer

    player_x = WIDTH // 2

    player_y = (
        GAME_TOP +
        GAME_HEIGHT // 2
    )

    health = max_health

    ammo = max_ammo

    score = 0

    kills = 0

    wave = 1

    zombies = []

    bullets = []

    death_effects = []

    spawn_timer = 0

    game_over = False

    paused = False

    current_gesture = (
        "no_gesture"
    )

    confidence = 0

    last_action = "READY"

    shield_active = False

    muzzle_timer = 0

    reload_timer = 0

    special_timer = 0

    player_hit_timer = 0

    gesture_cooldown = 0

    special_cooldown = 0

    reload_cooldown = 0


# ============================================================
# DRAW BACKGROUND
# ============================================================

def draw_background():

    if game_background is not None:

        screen.blit(
            game_background,
            (
                0,
                GAME_TOP
            )
        )

    else:

        pygame.draw.rect(
            screen,
            (15, 20, 25),
            (
                0,
                GAME_TOP,
                WIDTH,
                GAME_HEIGHT
            )
        )


# ============================================================
# DRAW PLAYER
# ============================================================

def draw_player():

    if shield_active:

        if shield_image is not None:

            shield_rect = (
                shield_image.get_rect(
                    center=(
                        int(player_x),
                        int(player_y)
                    )
                )
            )

            screen.blit(
                shield_image,
                shield_rect
            )

        else:

            pygame.draw.circle(
                screen,
                CYAN,
                (
                    int(player_x),
                    int(player_y)
                ),
                65,
                5
            )

    if player_image is not None:

        player_rect = (
            player_image.get_rect(
                center=(
                    int(player_x),
                    int(player_y)
                )
            )
        )

        screen.blit(
            player_image,
            player_rect
        )

    else:

        pygame.draw.circle(
            screen,
            BLUE,
            (
                int(player_x),
                int(player_y)
            ),
            25
        )

    if muzzle_timer > 0:

        if muzzle_image is not None:

            muzzle_rect = (
                muzzle_image.get_rect(
                    center=(
                        int(player_x + 55),
                        int(player_y - 15)
                    )
                )
            )

            screen.blit(
                muzzle_image,
                muzzle_rect
            )

        # Player damage flash
    if player_hit_timer > 0:

        damage_overlay = pygame.Surface(
            (
                WIDTH,
                HEIGHT
            ),
            pygame.SRCALPHA
        )

        alpha = int(
            80 *
            player_hit_timer
        )

        damage_overlay.fill(
            (
                255,
                0,
                0,
                alpha
            )
        )

        screen.blit(
            damage_overlay,
            (
                0,
                0
            )
        )
# ============================================================
# DRAW HEALTH HEARTS
# ============================================================

def draw_health_hearts():

    heart_count = 5

    health_per_heart = (
        max_health /
        heart_count
    )

    for i in range(
        heart_count
    ):

        if health >= (
            (i + 1) *
            health_per_heart
        ):

            image = heart_image

        else:

            image = empty_heart_image

        if image is not None:

            screen.blit(
                image,
                (
                    30 + i * 38,
                    74
                )
            )


# ============================================================
# DRAW TOP HUD
# ============================================================

def draw_hud():

    pygame.draw.rect(
        screen,
        (8, 13, 20),
        (
            0,
            0,
            WIDTH,
            TOP_BAR_HEIGHT
        )
    )

    pygame.draw.line(
        screen,
        GREEN,
        (
            0,
            TOP_BAR_HEIGHT - 1
        ),
        (
            WIDTH,
            TOP_BAR_HEIGHT - 1
        ),
        2
    )

    title = FONT_MEDIUM.render(
        "ZOMBiX",
        True,
        GREEN
    )

    screen.blit(
        title,
        (25, 18)
    )

    draw_health_hearts()

    ammo_text = FONT_NORMAL.render(
        f"AMMO  {ammo}/{max_ammo}",
        True,
        YELLOW
    )

    screen.blit(
        ammo_text,
        (300, 28)
    )

    score_text = FONT_NORMAL.render(
        f"SCORE  {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (500, 28)
    )

    wave_text = FONT_NORMAL.render(
        f"LEVEL  {wave}",
        True,
        ORANGE
    )

    screen.blit(
        wave_text,
        (690, 28)
    )

    kills_text = FONT_SMALL.render(
        f"ZOMBIES DEFEATED: {kills}",
        True,
        GRAY
    )

    screen.blit(
        kills_text,
        (500, 67)
    )

    if pause_image is not None:

        screen.blit(
            pause_image,
            (
                WIDTH - 65,
                20
            )
        )

    else:

        pygame.draw.rect(
            screen,
            PANEL,
            (
                WIDTH - 65,
                20,
                45,
                45
            ),
            border_radius=8
        )

        pause_text = FONT_NORMAL.render(
            "II",
            True,
            WHITE
        )

        screen.blit(
            pause_text,
            (
                WIDTH - 55,
                28
            )
        )


# ============================================================
# DRAW BOTTOM ACTION BAR
# ============================================================

def draw_action_bar():

    pygame.draw.rect(
        screen,
        (9, 14, 21),
        (
            0,
            GAME_BOTTOM,
            WIDTH,
            BOTTOM_BAR_HEIGHT
        )
    )

    pygame.draw.line(
        screen,
        GREEN,
        (
            0,
            GAME_BOTTOM
        ),
        (
            WIDTH,
            GAME_BOTTOM
        ),
        2
    )

    gesture_text = FONT_NORMAL.render(
        f"GESTURE: {current_gesture.upper()}",
        True,
        CYAN
    )

    screen.blit(
        gesture_text,
        (
            25,
            GAME_BOTTOM + 12
        )
    )

    action_text = FONT_NORMAL.render(
        f"ACTION: {last_action}",
        True,
        YELLOW
    )

    screen.blit(
        action_text,
        (
            360,
            GAME_BOTTOM + 12
        )
    )

    confidence_text = FONT_NORMAL.render(
        f"{confidence * 100:.0f}%",
        True,
        GREEN
    )

    screen.blit(
        confidence_text,
        (
            780,
            GAME_BOTTOM + 12
        )
    )

    pygame.draw.rect(
        screen,
        DARK_GREEN,
        (
            780,
            GAME_BOTTOM + 45,
            150,
            8
        ),
        border_radius=4
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (
            780,
            GAME_BOTTOM + 45,
            int(
                150 *
                min(
                    1,
                    confidence
                )
            ),
            8
        ),
        border_radius=4
    )


# ============================================================
# DRAW WEBCAM PREVIEW
# ============================================================

def draw_camera_preview(frame):

    if frame is None:

        return

    preview = cv2.resize(
        frame,
        (
            200,
            150
        )
    )

    preview = cv2.cvtColor(
        preview,
        cv2.COLOR_BGR2RGB
    )

    surface = pygame.surfarray.make_surface(
        preview.swapaxes(
            0,
            1
        )
    )

    x = 20

    y = GAME_BOTTOM - 170

    pygame.draw.rect(
        screen,
        BLACK,
        (
            x - 4,
            y - 4,
            208,
            158
        ),
        border_radius=8
    )

    screen.blit(
        surface,
        (
            x,
            y
        )
    )

    pygame.draw.rect(
        screen,
        CYAN,
        (
            x,
            y,
            200,
            150
        ),
        2,
        border_radius=6
    )

    label = FONT_SMALL.render(
        "LIVE CAMERA",
        True,
        WHITE
    )

    screen.blit(
        label,
        (
            x + 8,
            y + 8
        )
    )


# ============================================================
# DRAW RELOAD EFFECT
# ============================================================

def draw_reload_effect():

    if reload_timer <= 0:

        return

    if reload_image is None:

        return

    image = reload_image.copy()

    alpha = min(
        255,
        reload_timer * 8
    )

    image.set_alpha(
        alpha
    )

    rect = image.get_rect(
        center=(
            int(player_x),
            int(player_y)
        )
    )

    screen.blit(
        image,
        rect
    )


# ============================================================
# DRAW SPECIAL EFFECT
# ============================================================

def draw_special_effect():

    if special_timer <= 0:

        return

    if special_image is None:

        return

    image = special_image.copy()

    alpha = min(
        255,
        special_timer * 8
    )

    image.set_alpha(
        alpha
    )

    rect = image.get_rect(
        center=(
            int(player_x),
            int(player_y)
        )
    )

    screen.blit(
        image,
        rect
    )


# ============================================================
# DRAW DEATH EFFECTS
# ============================================================

def draw_death_effects():

    for effect in death_effects:

        if death_image is None:

            continue

        image = death_image.copy()

        alpha = int(
            255 *
            (
                effect["timer"] /
                25
            )
        )

        image.set_alpha(
            max(
                0,
                alpha
            )
        )

        rect = image.get_rect(
            center=(
                int(effect["x"]),
                int(effect["y"])
            )
        )

        screen.blit(
            image,
            rect
        )


# ============================================================
# UPDATE DEATH EFFECTS
# ============================================================

def update_death_effects():

    for effect in death_effects[:]:

        effect["timer"] -= 1

        if effect["timer"] <= 0:

            death_effects.remove(
                effect
            )


# ============================================================
# UPDATE ZOMBIES
# ============================================================

def update_zombies(dt):

    global health

    global game_over

    global last_action

    global player_hit_timer

    for zombie in zombies:

        zombie.update(dt)

        distance = math.sqrt(
            (zombie.x - player_x) ** 2 +
            (zombie.y - player_y) ** 2
        )

        if distance < 50:

            if not shield_active:

                health -= 21 * dt

                last_action = (
                    "ZOMBIE ATTACK"
                )

                # Red damage effect on player
                player_hit_timer = 1.0


            else:

                last_action = (
                    "SHIELD BLOCK"
                )

            if distance > 0:

                zombie.x -= (
                    (
                        player_x -
                        zombie.x
                    ) * 0.015
                )

                zombie.y -= (
                    (
                        player_y -
                        zombie.y
                    ) * 0.015
                )

    if health <= 0:

        health = 0

        game_over = True


# ============================================================
# UPDATE BULLETS
# ============================================================

def update_bullets(dt):

    global score

    global kills

    for bullet in bullets[:]:

        bullet.update(dt)

        if (
            bullet.x < -50
            or
            bullet.x > WIDTH + 50
            or
            bullet.y < GAME_TOP - 50
            or
            bullet.y > GAME_BOTTOM + 50
        ):

            if bullet in bullets:

                bullets.remove(
                    bullet
                )

            continue

        for zombie in zombies[:]:

            distance = math.sqrt(
                (
                    bullet.x -
                    zombie.x
                ) ** 2 +
                (
                    bullet.y -
                    zombie.y
                ) ** 2
            )

            if distance < (
                zombie.radius +
                bullet.radius +
                10
            ):

                zombie.health -= 1
                zombie.hit_timer = 0.15

                if bullet in bullets:

                    bullets.remove(
                        bullet
                    )

                if zombie.health <= 0:

                    if zombie in zombies:

                        zombies.remove(
                            zombie
                        )

                    create_death_effect(
                        zombie.x,
                        zombie.y
                    )

                    score += 10

                    kills += 1

                break


# ============================================================
# SPAWN ZOMBIES
# ============================================================

def spawn_zombies():

    global spawn_timer

    spawn_timer += 1

    max_allowed = min(
        MAX_ZOMBIES + wave,
        12
    )

    if (
        spawn_timer >
        max(
            25,
            80 - wave * 4
        )
        and
        len(zombies) <
        max_allowed
    ):

        zombies.append(
            Zombie()
        )

        spawn_timer = 0


# ============================================================
# WAVE SYSTEM
# ============================================================

def update_wave():

    global wave

    target_wave = (
        1 +
        kills // 10
    )

    if target_wave > wave:

        wave = target_wave


# ============================================================
# PLAYER MOVEMENT
# ============================================================

def move_player(wrist, dt):

    global player_x

    global player_y

    if wrist is None:

        return

    x = wrist.x

    y = wrist.y

    move_amount = PLAYER_SPEED * 60 * dt

    # Dead-zone based movement prevents jitter.
    if x < 0.35:

        player_x -= move_amount

    elif x > 0.65:

        player_x += move_amount

    if y < 0.35:

        player_y -= move_amount

    elif y > 0.65:

        player_y += move_amount

    player_x = max(
        60,
        min(
            WIDTH - 60,
            player_x
        )
    )

    player_y = max(
        GAME_TOP + 80,
        min(
            GAME_BOTTOM - 70,
            player_y
        )
    )


# ============================================================
# UPDATE VISUAL TIMERS
# ============================================================

def update_effect_timers():

    global muzzle_timer

    global reload_timer

    global special_timer

    global player_hit_timer

    if muzzle_timer > 0:

        muzzle_timer -= 1

    if reload_timer > 0:

        reload_timer -= 1

    if special_timer > 0:

        special_timer -= 1

    if player_hit_timer > 0:

        player_hit_timer -= 0.08

    if player_hit_timer < 0:

            player_hit_timer = 0

# ============================================================
# DRAW GAME OVER BUTTON
# ============================================================

def draw_game_over_button(
    text,
    rect,
    color
):

    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(
        mouse_pos
    ):

        button_color = (
            min(color[0] + 30, 255),
            min(color[1] + 30, 255),
            min(color[2] + 30, 255)
        )

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

    text_surface = FONT_NORMAL.render(
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


# ============================================================
# GAME OVER SCREEN
# ============================================================

def draw_game_over():

    if game_over_background is not None:

        screen.blit(
            game_over_background,
            (
                0,
                0
            )
        )

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            0,
            0,
            0,
            145
        )
    )

    screen.blit(
        overlay,
        (
            0,
            0
        )
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title = FONT_TITLE.render(
        "GAME OVER",
        True,
        RED
    )

    screen.blit(
        title,
        (
            WIDTH // 2 -
            title.get_width() // 2,
            150
        )
    )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    score_text = FONT_MEDIUM.render(
        f"FINAL SCORE: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (
            WIDTH // 2 -
            score_text.get_width() // 2,
            245
        )
    )

    # --------------------------------------------------------
    # KILLS
    # --------------------------------------------------------

    kills_text = FONT_NORMAL.render(
        f"ZOMBIES DEFEATED: {kills}",
        True,
        GRAY
    )

    screen.blit(
        kills_text,
        (
            WIDTH // 2 -
            kills_text.get_width() // 2,
            295
        )
    )

    # --------------------------------------------------------
    # LEVEL
    # --------------------------------------------------------

    wave_text = FONT_NORMAL.render(
        f"LEVEL REACHED: {wave}",
        True,
        ORANGE
    )

    screen.blit(
        wave_text,
        (
            WIDTH // 2 -
            wave_text.get_width() // 2,
            335
        )
    )

    # --------------------------------------------------------
    # PLAY AGAIN
    # --------------------------------------------------------

    draw_game_over_button(
        "PLAY AGAIN",
        GAME_OVER_PLAY_BUTTON,
        DARK_GREEN
    )

    # --------------------------------------------------------
    # BACK TO MENU
    # --------------------------------------------------------

    draw_game_over_button(
        "BACK TO MENU",
        GAME_OVER_BACK_BUTTON,
        DARK_RED
    )


# ============================================================
# PAUSE SCREEN
# ============================================================

def draw_pause_button(
    text,
    rect,
    color
):

    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):

        button_color = (
            min(color[0] + 30, 255),
            min(color[1] + 30, 255),
            min(color[2] + 30, 255)
        )

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

    text_surface = FONT_NORMAL.render(
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


def draw_pause_screen():

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            0,
            0,
            0,
            175
        )
    )

    screen.blit(
        overlay,
        (
            0,
            0
        )
    )

    title = FONT_TITLE.render(
        "PAUSED",
        True,
        GREEN
    )

    screen.blit(
        title,
        (
            WIDTH // 2 -
            title.get_width() // 2,
            205
        )
    )

    draw_pause_button(
        "RESUME",
        PAUSE_RESUME_BUTTON,
        DARK_GREEN
    )

    draw_pause_button(
        "BACK TO MENU",
        PAUSE_MENU_BUTTON,
        DARK_RED
    )




# ============================================================
# RETURN TO MAIN MENU
# ============================================================

def return_to_main_menu():

    # Release webcam
    try:
        camera.release()
    except Exception:
        pass

    # Close MediaPipe
    if landmarker is not None:
        try:
            landmarker.close()
        except Exception:
            pass

    # Close current game window
    pygame.quit()

    # Path to main.py
    main_path = os.path.join(
        BASE_DIR,
        "main.py"
    )

    # Start main menu without opening console
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

    sys.exit()


# ============================================================
# RETURN TO MAIN MENU
# ============================================================

def return_to_main_menu():

    # Release webcam
    try:
        camera.release()
    except Exception:
        pass

    # Close MediaPipe
    if landmarker is not None:
        try:
            landmarker.close()
        except Exception:
            pass

    # Close current game window
    pygame.quit()

    # Path to main.py
    main_path = os.path.join(
        BASE_DIR,
        "main.py"
    )

    # Start main menu without opening console
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

    sys.exit()


# ============================================================
# RETURN TO MAIN MENU
# ============================================================

def return_to_main_menu():

    # Release webcam
    try:
        camera.release()
    except Exception:
        pass

    # Close MediaPipe
    if landmarker is not None:
        try:
            landmarker.close()
        except Exception:
            pass

    # Close current game window
    pygame.quit()

    # Path to main.py
    main_path = os.path.join(
        BASE_DIR,
        "main.py"
    )

    # Start main menu without opening console
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

    sys.exit()



# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True

reset_game()

while running:

    dt = clock.tick(60) / 1000.0

    # Prevent a large movement jump if the window is temporarily frozen.
    dt = min(dt, 0.05)

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        # ----------------------------------------------------
        # WINDOW CLOSE
        # ----------------------------------------------------

        if event.type == QUIT:

            running = False

        # ----------------------------------------------------
        # KEYBOARD
        # ----------------------------------------------------

        if event.type == KEYDOWN:

            # ESC remains an optional keyboard shortcut.
            # Main navigation is provided by clickable buttons.

            if event.key == K_ESCAPE:

                if not game_over and not paused:

                    running = False

            # P = Pause

            if event.key == pygame.K_p:

                if not game_over:

                    paused = not paused

        # ----------------------------------------------------
        # MOUSE
        # ----------------------------------------------------

        if event.type == MOUSEBUTTONDOWN:

            if event.button == 1:

                mouse_x, mouse_y = event.pos

                # =================================================
                # GAME OVER BUTTONS
                # =================================================

                if game_over:

                    # PLAY AGAIN

                    if GAME_OVER_PLAY_BUTTON.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        reset_game()

                    # BACK TO MENU

                    elif GAME_OVER_BACK_BUTTON.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        return_to_main_menu()

                # =================================================
                # PAUSE SCREEN BUTTONS
                # =================================================

                elif paused:

                    if PAUSE_RESUME_BUTTON.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        paused = False

                    elif PAUSE_MENU_BUTTON.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        running = False

                # =================================================
                # PAUSE BUTTON
                # =================================================

                else:

                    pause_rect = pygame.Rect(
                        WIDTH - 70,
                        15,
                        60,
                        60
                    )

                    if pause_rect.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        paused = True

    # ========================================================
    # CAMERA
    # ========================================================

    ret, frame = camera.read()

    wrist = None

    if ret:

        frame = cv2.flip(
            frame,
            1
        )

        wrist, hand = detect_gesture(
            frame
        )

    # ========================================================
    # GAME UPDATE
    # ========================================================

    if (
        not game_over
        and
        not paused
    ):

        # ----------------------------------------------------
        # MOVEMENT
        # ----------------------------------------------------

        move_player(
            wrist,
            dt
        )

        # ----------------------------------------------------
        # GESTURE ACTIONS
        # ----------------------------------------------------

        if confidence >= 0.70:

            # FIST = SHOOT

            if current_gesture == "fist":

                shield_active = False

                if gesture_cooldown <= 0:

                    shoot()

                    gesture_cooldown = 18

            # PALM = SHIELD

            elif current_gesture == "palm":

                shield_active = True

                last_action = "SHIELD"

            # PEACE = SPECIAL ATTACK

            elif current_gesture == "peace":

                shield_active = False

                if gesture_cooldown <= 0:

                    special_attack()

                    gesture_cooldown = 35

            # LIKE = RELOAD

            elif current_gesture == "like":

                shield_active = False

                if reload_cooldown <= 0:

                    reload_weapon()

                    reload_cooldown = 60

            else:

                shield_active = False

        else:

            shield_active = False

        # ----------------------------------------------------
        # COOLDOWNS
        # ----------------------------------------------------

        if gesture_cooldown > 0:

            gesture_cooldown -= 1

        if special_cooldown > 0:

            special_cooldown -= 1

        if reload_cooldown > 0:

            reload_cooldown -= 1

        # ----------------------------------------------------
        # EFFECTS
        # ----------------------------------------------------

        update_effect_timers()

        update_death_effects()

        # ----------------------------------------------------
        # SPAWN
        # ----------------------------------------------------

        spawn_zombies()

        # ----------------------------------------------------
        # ZOMBIES
        # ----------------------------------------------------

        update_zombies(dt)

        # ----------------------------------------------------
        # BULLETS
        # ----------------------------------------------------

        update_bullets(dt)

        # ----------------------------------------------------
        # WAVE
        # ----------------------------------------------------

        update_wave()

    # ========================================================
    # DRAW
    # ========================================================

    screen.fill(
        BLACK
    )

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    draw_background()

    # --------------------------------------------------------
    # ZOMBIES
    # --------------------------------------------------------

    for zombie in zombies:

        zombie.draw()

    # --------------------------------------------------------
    # BULLETS
    # --------------------------------------------------------

    for bullet in bullets:

        bullet.draw()

    # --------------------------------------------------------
    # DEATH EFFECTS
    # --------------------------------------------------------

    draw_death_effects()

    # --------------------------------------------------------
    # SPECIAL ATTACK
    # --------------------------------------------------------

    draw_special_effect()

    # --------------------------------------------------------
    # PLAYER
    # --------------------------------------------------------

    draw_player()

    # --------------------------------------------------------
    # RELOAD
    # --------------------------------------------------------

    draw_reload_effect()

    # --------------------------------------------------------
    # HUD
    # --------------------------------------------------------

    draw_hud()

    # --------------------------------------------------------
    # CAMERA
    # --------------------------------------------------------

    if ret:

        draw_camera_preview(
            frame
        )

    # --------------------------------------------------------
    # ACTION BAR
    # --------------------------------------------------------

    draw_action_bar()

    # --------------------------------------------------------
    # PAUSE
    # --------------------------------------------------------

    if paused:

        draw_pause_screen()

    # --------------------------------------------------------
    # GAME OVER
    # --------------------------------------------------------

    if game_over:

        draw_game_over()

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    pygame.display.flip()


# ============================================================
# CLEANUP
# ============================================================

camera.release()

if landmarker is not None:

    try:

        landmarker.close()

    except Exception:

        pass

pygame.quit()

print(
    "ZOMBiX game closed."
)