import pygame
import random
import math

# ---------------------------------------
# Initialize Pygame
# ---------------------------------------

pygame.init()

WIDTH = 1000
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ZombiX - Gesture Controlled Zombie Game")

clock = pygame.time.Clock()


# ---------------------------------------
# Colors
# ---------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 80)
BLUE = (50, 120, 255)
YELLOW = (255, 220, 50)
GRAY = (100, 100, 100)


# ---------------------------------------
# Fonts
# ---------------------------------------

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 50)


# ---------------------------------------
# Player
# ---------------------------------------

player_x = WIDTH // 2
player_y = HEIGHT // 2

player_radius = 25
player_speed = 5

health = 100
score = 0

ammo = 10
max_ammo = 10


# ---------------------------------------
# Zombies
# ---------------------------------------

zombies = []

for i in range(5):

    x = random.choice([
        random.randint(0, WIDTH),
        random.choice([0, WIDTH])
    ])

    y = random.choice([
        random.randint(0, HEIGHT),
        random.choice([0, HEIGHT])
    ])

    zombies.append({
        "x": x,
        "y": y,
        "speed": random.uniform(1.0, 2.0),
        "radius": 25
    })


# ---------------------------------------
# Bullets
# ---------------------------------------

bullets = []


# ---------------------------------------
# Shoot bullet
# ---------------------------------------

def shoot():

    global ammo

    if ammo <= 0:
        return

    ammo -= 1

    mouse_x, mouse_y = pygame.mouse.get_pos()

    dx = mouse_x - player_x
    dy = mouse_y - player_y

    distance = math.sqrt(dx * dx + dy * dy)

    if distance == 0:
        return

    dx /= distance
    dy /= distance

    bullets.append({
        "x": player_x,
        "y": player_y,
        "dx": dx,
        "dy": dy
    })


# ---------------------------------------
# Reload
# ---------------------------------------

def reload_weapon():

    global ammo

    ammo = max_ammo


# ---------------------------------------
# Game loop
# ---------------------------------------

running = True

while running:

    clock.tick(60)

    # -----------------------------------
    # Events
    # -----------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Mouse shooting
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                shoot()

        # Keyboard controls
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                reload_weapon()

            if event.key == pygame.K_ESCAPE:
                running = False


    # -----------------------------------
    # Player movement
    # -----------------------------------

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed


    # Keep player inside screen

    player_x = max(
        player_radius,
        min(WIDTH - player_radius, player_x)
    )

    player_y = max(
        player_radius,
        min(HEIGHT - player_radius, player_y)
    )


    # -----------------------------------
    # Move bullets
    # -----------------------------------

    for bullet in bullets[:]:

        bullet["x"] += bullet["dx"] * 12
        bullet["y"] += bullet["dy"] * 12

        # Remove bullet outside screen

        if (
            bullet["x"] < 0
            or bullet["x"] > WIDTH
            or bullet["y"] < 0
            or bullet["y"] > HEIGHT
        ):

            bullets.remove(bullet)


    # -----------------------------------
    # Move zombies
    # -----------------------------------

    for zombie in zombies:

        dx = player_x - zombie["x"]
        dy = player_y - zombie["y"]

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        if distance > 0:

            dx /= distance
            dy /= distance

            zombie["x"] += dx * zombie["speed"]
            zombie["y"] += dy * zombie["speed"]


    # -----------------------------------
    # Bullet-Zombie collision
    # -----------------------------------

    for bullet in bullets[:]:

        for zombie in zombies[:]:

            dx = bullet["x"] - zombie["x"]
            dy = bullet["y"] - zombie["y"]

            distance = math.sqrt(
                dx * dx + dy * dy
            )

            if distance < zombie["radius"]:

                if bullet in bullets:
                    bullets.remove(bullet)

                if zombie in zombies:
                    zombies.remove(zombie)

                score += 10

                # Spawn new zombie

                x = random.choice([
                    random.randint(0, WIDTH),
                    random.choice([0, WIDTH])
                ])

                y = random.choice([
                    random.randint(0, HEIGHT),
                    random.choice([0, HEIGHT])
                ])

                zombies.append({
                    "x": x,
                    "y": y,
                    "speed": random.uniform(1.0, 2.0),
                    "radius": 25
                })

                break


    # -----------------------------------
    # Zombie-player collision
    # -----------------------------------

    for zombie in zombies:

        dx = player_x - zombie["x"]
        dy = player_y - zombie["y"]

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        if distance < player_radius + zombie["radius"]:

            health -= 0.3


    # -----------------------------------
    # Draw background
    # -----------------------------------

    screen.fill((20, 25, 30))


    # -----------------------------------
    # Draw bullets
    # -----------------------------------

    for bullet in bullets:

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                int(bullet["x"]),
                int(bullet["y"])
            ),
            5
        )


    # -----------------------------------
    # Draw zombies
    # -----------------------------------

    for zombie in zombies:

        pygame.draw.circle(
            screen,
            GREEN,
            (
                int(zombie["x"]),
                int(zombie["y"])
            ),
            zombie["radius"]
        )

        # Zombie eyes

        pygame.draw.circle(
            screen,
            RED,
            (
                int(zombie["x"] - 8),
                int(zombie["y"] - 5)
            ),
            4
        )

        pygame.draw.circle(
            screen,
            RED,
            (
                int(zombie["x"] + 8),
                int(zombie["y"] - 5)
            ),
            4
        )


    # -----------------------------------
    # Draw player
    # -----------------------------------

    pygame.draw.circle(
        screen,
        BLUE,
        (
            int(player_x),
            int(player_y)
        ),
        player_radius
    )


    # -----------------------------------
    # HUD
    # -----------------------------------

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    ammo_text = font.render(
        f"Ammo: {ammo}/{max_ammo}",
        True,
        WHITE
    )

    health_text = font.render(
        f"Health: {int(health)}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    screen.blit(
        ammo_text,
        (20, 55)
    )

    screen.blit(
        health_text,
        (20, 90)
    )


    # -----------------------------------
    # Game over
    # -----------------------------------

    if health <= 0:

        game_over = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            game_over,
            (
                WIDTH // 2 - 150,
                HEIGHT // 2 - 50
            )
        )

        pygame.display.flip()

        pygame.time.wait(3000)

        running = False


    pygame.display.flip()


# ---------------------------------------
# Quit
# ---------------------------------------

pygame.quit()