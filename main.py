import os
import sys
import subprocess
import pygame


# ============================================================
# HIDE CONSOLE WINDOW ON WINDOWS
# ============================================================

def hide_console():

    if os.name != "nt":
        return

    try:
        import ctypes

        hwnd = ctypes.windll.kernel32.GetConsoleWindow()

        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)

    except Exception:
        pass


hide_console()


# ============================================================
# INITIALIZE
# ============================================================

pygame.init()

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

GAME_PATH = os.path.join(
    BASE_DIR,
    "game",
    "gesture_game.py"
)

LEARN_PATH = os.path.join(
    BASE_DIR,
    "game",
    "learn_gestures.py"
)


# ============================================================
# FULLSCREEN
# ============================================================

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



# ============================================================
# RETURN TO MAIN MENU
# ============================================================

def return_to_main_menu():

    # --------------------------------------------------------
    # RELEASE CAMERA
    # --------------------------------------------------------

    try:
        camera.release()
    except Exception:
        pass

    # --------------------------------------------------------
    # CLOSE MEDIAPIPE
    # --------------------------------------------------------

    if landmarker is not None:

        try:
            landmarker.close()
        except Exception:
            pass

    # --------------------------------------------------------
    # CLOSE GAME WINDOW
    # --------------------------------------------------------

    pygame.quit()

    # --------------------------------------------------------
    # FIND MAIN.PY
    # --------------------------------------------------------

    main_path = os.path.join(
        BASE_DIR,
        "main.py"
    )

    # --------------------------------------------------------
    # START MAIN MENU WITHOUT TERMINAL
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # CLOSE CURRENT GAME PROCESS
    # --------------------------------------------------------

    sys.exit()


# ============================================================
# COLORS
# ============================================================

WHITE = (255, 255, 255)

GREEN = (40, 200, 90)
DARK_GREEN = (20, 100, 50)

BLUE = (40, 120, 220)
DARK_BLUE = (20, 50, 100)

GRAY = (90, 90, 90)
DARK_GRAY = (30, 30, 30)

RED = (180, 40, 40)

BLACK = (0, 0, 0)


# ============================================================
# FONTS
# ============================================================

TITLE_FONT = pygame.font.Font(
    None,
    80
)

BUTTON_FONT = pygame.font.Font(
    None,
    32
)

SMALL_FONT = pygame.font.Font(
    None,
    24
)


# ============================================================
# BACKGROUND
# ============================================================

MENU_BG_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "backgrounds",
    "menu_bg.png"
)


def load_background():

    try:

        image = pygame.image.load(
            MENU_BG_PATH
        ).convert()

        return pygame.transform.scale(
            image,
            (
                WIDTH,
                HEIGHT
            )
        )

    except Exception:

        return None


background = load_background()

# ============================================================
# ZOMBiX LOGO
# ============================================================

LOGO_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "ui",
    "zombix_logo.png"
)

try:
    logo_image = pygame.image.load(
        LOGO_PATH
    ).convert_alpha()

    logo_width = 650

    logo_height = int(
        logo_image.get_height()
        * logo_width
        / logo_image.get_width()
    )

    logo_image = pygame.transform.smoothscale(
        logo_image,
        (
            logo_width,
            logo_height
        )
    )

except Exception:
    logo_image = None

# ============================================================
# BUTTON
# ============================================================

def draw_button(
    text,
    rect,
    color
):

    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):

        hover_color = (
            min(color[0] + 30, 255),
            min(color[1] + 30, 255),
            min(color[2] + 30, 255)
        )

    else:

        hover_color = color

    pygame.draw.rect(
        screen,
        hover_color,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        WHITE,
        rect,
        2,
        border_radius=12
    )

    text_surface = BUTTON_FONT.render(
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
# RUN GAME WITHOUT TERMINAL
# ============================================================

def launch_program(program_path):

    if os.name == "nt":

        startupinfo = subprocess.STARTUPINFO()

        startupinfo.dwFlags |= (
            subprocess.STARTF_USESHOWWINDOW
        )

        startupinfo.wShowWindow = (
            subprocess.SW_HIDE
        )

        subprocess.run(
            [
                sys.executable,
                program_path
            ],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    else:

        subprocess.run(
            [
                sys.executable,
                program_path
            ]
        )


# ============================================================
# PLAY
# ============================================================

def launch_game():

    global screen

    pygame.quit()

    launch_program(
        GAME_PATH
    )

    pygame.init()

    screen = pygame.display.set_mode(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.FULLSCREEN
    )

    pygame.display.set_caption(
        "ZOMBiX - Gesture Controlled Zombie Survival"
    )


# ============================================================
# LEARN GESTURES
# ============================================================

def launch_learning():

    global screen

    pygame.quit()

    launch_program(
        LEARN_PATH
    )

    pygame.init()

    screen = pygame.display.set_mode(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.FULLSCREEN
    )

    pygame.display.set_caption(
        "ZOMBiX - Learn Gestures"
    )


# ============================================================
# SETTINGS
# ============================================================

def settings_screen():

    running = True

    # Back button
    back_button = pygame.Rect(
        40,
        40,
        160,
        55
    )

    while running:

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        if background:

            screen.blit(
                background,
                (0, 0)
            )

        else:

            screen.fill(
                DARK_GRAY
            )

        # ----------------------------------------------------
        # DARK OVERLAY
        # ----------------------------------------------------

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
                150
            )
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = TITLE_FONT.render(
            "SETTINGS",
            True,
            WHITE
        )

        screen.blit(
            title,
            (
                WIDTH // 2 -
                title.get_width() // 2,
                130
            )
        )

        # ----------------------------------------------------
        # INFORMATION
        # ----------------------------------------------------

        info = SMALL_FONT.render(
            "ZOMBiX - Gesture Controlled Zombie Survival",
            True,
            WHITE
        )

        screen.blit(
            info,
            (
                WIDTH // 2 -
                info.get_width() // 2,
                250
            )
        )

        # ----------------------------------------------------
        # BACK BUTTON
        # ----------------------------------------------------

        draw_button(
            "BACK",
            back_button,
            DARK_BLUE
        )

        # ----------------------------------------------------
        # EVENTS
        # ----------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if back_button.collidepoint(
                        event.pos
                    ):

                        running = False

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        pygame.display.flip()

# ============================================================
# MAIN MENU
# ============================================================

def main_menu():

    running = True

    button_width = 380
    button_height = 60

    center_x = (
        WIDTH -
        button_width
    ) // 2

    play_button = pygame.Rect(
        center_x,
        int(HEIGHT * 0.55),
        button_width,
        button_height
    )

    learn_button = pygame.Rect(
        center_x,
        int(HEIGHT * 0.55) + 75,
        button_width,
        button_height
    )

    settings_button = pygame.Rect(
        center_x,
        int(HEIGHT * 0.55) + 150,
        button_width,
        button_height
    )

    quit_button = pygame.Rect(
        center_x,
        int(HEIGHT * 0.55) + 225,
        button_width,
        button_height
    )

    while running:

        if background:

            screen.blit(
                background,
                (
                    0,
                    0
                )
            )

        else:

            screen.fill(
                BLACK
            )

        # Dark overlay
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
                80
            )
        )

        screen.blit(
            overlay,
            (
                0,
                0
            )
        )

        
# ============================================================
# ZOMBiX TITLE
# ============================================================

       # ============================================================
# ZOMBiX LOGO
# ============================================================

        if logo_image is not None:

            logo_rect = logo_image.get_rect(
                center=(
                    WIDTH // 2,
                    105
                )
            )

            screen.blit(
                logo_image,
                logo_rect
            )
        # ============================================================
# SUBTITLE
# ============================================================

        subtitle = BUTTON_FONT.render(
            "GESTURE CONTROLLED ZOMBIE SURVIVAL",
            True,
            WHITE
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                WIDTH // 2,
                205
            )
        )

        screen.blit(
            subtitle,
            subtitle_rect
        )
        # ====================================================
        # BUTTONS
        # ====================================================

        draw_button(
            "PLAY",
            play_button,
            DARK_GREEN
        )

        draw_button(
            "LEARN GESTURES",
            learn_button,
            DARK_BLUE
        )

        draw_button(
            "SETTINGS",
            settings_button,
            GRAY
        )

        draw_button(
            "QUIT",
            quit_button,
            RED
        )

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if play_button.collidepoint(
                        event.pos
                    ):

                        launch_game()

                    elif learn_button.collidepoint(
                        event.pos
                    ):

                        launch_learning()

                    elif settings_button.collidepoint(
                        event.pos
                    ):

                        settings_screen()

                    elif quit_button.collidepoint(
                        event.pos
                    ):

                        running = False

        pygame.display.flip()

    pygame.quit()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main_menu()