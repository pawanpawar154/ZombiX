import pygame
import sys
import subprocess

pygame.init()

# =========================================================
# WINDOW
# =========================================================

pygame.init()

display_info = pygame.display.Info()

WIDTH = display_info.current_w
HEIGHT = display_info.current_h

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.FULLSCREEN,
    pygame.display.set_caption("ZOMBiX - Gesture Controlled Zombie Game")
)
clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================

WHITE = (245, 245, 245)
LIGHT_GREEN = (50, 220, 130)
GREEN = (20, 170, 90)
DARK_GREEN = (10, 80, 55)

DARK_BG = (5, 18, 25)
BLUE_BG = (10, 35, 55)

GRAY = (130, 145, 155)
DARK_GRAY = (35, 55, 65)

RED = (220, 50, 60)

# =========================================================
# FONTS
# =========================================================

title_font = pygame.font.Font(None, 110)
subtitle_font = pygame.font.Font(None, 38)
button_font = pygame.font.Font(None, 42)
small_font = pygame.font.Font(None, 26)

# =========================================================
# BUTTONS
# =========================================================

button_width = 340
button_height = 65
button_x = (WIDTH - button_width) // 2

play_button = pygame.Rect(
    button_x, 255, button_width, button_height
)

learn_button = pygame.Rect(
    button_x, 335, button_width, button_height
)

settings_button = pygame.Rect(
    button_x, 415, button_width, button_height
)

quit_button = pygame.Rect(
    button_x, 495, button_width, button_height
)

# =========================================================
# BACKGROUND
# =========================================================

def draw_background():

    screen.fill(DARK_BG)

    # Large moon
    pygame.draw.circle(
        screen,
        (190, 205, 205),
        (800, 120),
        75
    )

    # Moon shadow spots
    pygame.draw.circle(
        screen,
        (165, 180, 180),
        (775, 100),
        12
    )

    pygame.draw.circle(
        screen,
        (165, 180, 180),
        (820, 145),
        18
    )

    pygame.draw.circle(
        screen,
        (165, 180, 180),
        (825, 95),
        10
    )

    # Buildings
    pygame.draw.rect(
        screen,
        (8, 25, 32),
        (0, 400, 150, 250)
    )

    pygame.draw.rect(
        screen,
        (7, 23, 30),
        (130, 340, 130, 310)
    )

    pygame.draw.rect(
        screen,
        (8, 27, 35),
        (250, 390, 150, 260)
    )

    pygame.draw.rect(
        screen,
        (7, 23, 30),
        (390, 350, 130, 300)
    )

    pygame.draw.rect(
        screen,
        (6, 22, 30),
        (520, 400, 170, 250)
    )

    pygame.draw.rect(
        screen,
        (7, 25, 32),
        (680, 350, 140, 300)
    )

    pygame.draw.rect(
        screen,
        (5, 20, 28),
        (820, 390, 180, 260)
    )

    # Building windows
    for x in range(20, 140, 40):
        for y in range(430, 590, 50):
            pygame.draw.rect(
                screen,
                (70, 90, 75),
                (x, y, 12, 20)
            )

    for x in range(150, 250, 35):
        for y in range(370, 590, 45):
            pygame.draw.rect(
                screen,
                (65, 85, 70),
                (x, y, 10, 18)
            )

    for x in range(410, 510, 35):
        for y in range(380, 590, 45):
            pygame.draw.rect(
                screen,
                (65, 85, 70),
                (x, y, 10, 18)
            )

    # Ground
    pygame.draw.rect(
        screen,
        (8, 15, 18),
        (0, 600, WIDTH, 50)
    )


# =========================================================
# ZOMBIE SILHOUETTES
# =========================================================

def draw_zombie(x, y, scale=1):

    # Head
    pygame.draw.circle(
        screen,
        (20, 30, 28),
        (x, y),
        int(25 * scale)
    )

    # Body
    pygame.draw.rect(
        screen,
        (18, 28, 27),
        (
            x - int(25 * scale),
            y + int(20 * scale),
            int(50 * scale),
            int(75 * scale)
        ),
        border_radius=10
    )

    # Arms
    pygame.draw.line(
        screen,
        (18, 28, 27),
        (x - int(20 * scale), y + int(35 * scale)),
        (x - int(55 * scale), y + int(70 * scale)),
        int(12 * scale)
    )

    pygame.draw.line(
        screen,
        (18, 28, 27),
        (x + int(20 * scale), y + int(35 * scale)),
        (x + int(55 * scale), y + int(70 * scale)),
        int(12 * scale)
    )

    # Eyes
    pygame.draw.circle(
        screen,
        RED,
        (
            x - int(9 * scale),
            y - int(3 * scale)
        ),
        max(2, int(4 * scale))
    )

    pygame.draw.circle(
        screen,
        RED,
        (
            x + int(9 * scale),
            y - int(3 * scale)
        ),
        max(2, int(4 * scale))
    )


# =========================================================
# BUTTON DRAWING
# =========================================================

def draw_button(rect, text, active=True):

    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):

        if active:
            color = GREEN
        else:
            color = DARK_GRAY

    else:

        if active:
            color = DARK_GREEN
        else:
            color = DARK_GRAY

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        (80, 110, 120),
        rect,
        2,
        border_radius=12
    )

    text_surface = button_font.render(
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
# TITLE
# =========================================================

def draw_title():

    title = title_font.render(
        "ZOMBiX",
        True,
        WHITE
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, 100)
    )

    screen.blit(
        title,
        title_rect
    )

    # Red X
    x_text = title_font.render(
        "X",
        True,
        RED
    )

    x_rect = x_text.get_rect(
        center=(650, 100)
    )

    screen.blit(
        x_text,
        x_rect
    )

    subtitle = subtitle_font.render(
        "Gesture Controlled Zombie Game",
        True,
        WHITE
    )

    subtitle_rect = subtitle.get_rect(
        center=(WIDTH // 2, 175)
    )

    screen.blit(
        subtitle,
        subtitle_rect
    )


# =========================================================
# PLAY GAME
# =========================================================

def start_game():

    pygame.quit()

    subprocess.run(
        [
            sys.executable,
            "game/gesture_game.py"
        ]
    )

    pygame.init()

    global screen

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        "ZOMBiX - Gesture Controlled Zombie Game"
    )


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    draw_background()

    # Zombies in background
    draw_zombie(100, 500, 1.1)
    draw_zombie(900, 500, 0.9)
    draw_zombie(300, 530, 0.7)

    draw_title()

    # Buttons
    draw_button(
        play_button,
        "PLAY"
    )

    draw_button(
        learn_button,
        "LEARN GESTURES"
    )

    draw_button(
        settings_button,
        "SETTINGS"
    )

    draw_button(
        quit_button,
        "QUIT"
    )

    # Bottom text
    info = small_font.render(
        "Use your hand gestures to survive the zombie attack!",
        True,
        GRAY
    )

    info_rect = info.get_rect(
        center=(WIDTH // 2, 625)
    )

    screen.blit(
        info,
        info_rect
    )

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # PLAY
            if play_button.collidepoint(event.pos):

                start_game()

            # LEARN GESTURES
            elif learn_button.collidepoint(event.pos):

                print("Learn Gestures screen will be added next.")

            # SETTINGS
            elif settings_button.collidepoint(event.pos):

                print("Settings screen will be added later.")

            # QUIT
            elif quit_button.collidepoint(event.pos):

                running = False

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
sys.exit()