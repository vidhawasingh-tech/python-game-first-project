import pygame
import sys
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultra Retro Car Game")

clock = pygame.time.Clock()

# Colors (Game Boy style)
GRASS = (48, 88, 48)
ROAD = (32, 32, 32)
TEXT = (200, 200, 200)
YELLOW = (220, 220, 0)

# ASCII pixel-art sprites
PLAYER_SPRITE = [
    "   ██   ",
    " ██████ ",
    "████████",
    "██ ███ ██",
    "████████",
    "██ ███ ██",
    "████████",
    " ██████ ",
    "   ██   "
]

ENEMY_SPRITE = [
    "   ██   ",
    " ██████ ",
    "██ ███ ██",
    "████████",
    "██ ███ ██",
    "████████",
    "██ ███ ██",
    " ██████ ",
    "   ██   "
]

# Convert ASCII to surfaces
def sprite_to_surface(sprite, color):
    surf = pygame.Surface((len(sprite[0]) * 6, len(sprite) * 6), pygame.SRCALPHA)
    for y, row in enumerate(sprite):
        for x, ch in enumerate(row):
            if ch == "█":
                pygame.draw.rect(surf, color, (x * 6, y * 6, 6, 6))
    return surf

player_img = sprite_to_surface(PLAYER_SPRITE, (0, 200, 0))
enemy_img = sprite_to_surface(ENEMY_SPRITE, (200, 0, 0))

car_w, car_h = player_img.get_width(), player_img.get_height()

font = pygame.font.SysFont("Courier", 32)
big_font = pygame.font.SysFont("Courier", 60)

def reset_game():
    return {
        "car_x": WIDTH // 2 - car_w // 2,
        "car_y": HEIGHT - car_h - 40,
        "score": 0,
        "enemies": [],
        "lines": [[WIDTH//2 - 5, i * 80] for i in range(10)],
        "spawn_timer": 0,
        "game_over": False
    }

game = reset_game()

enemy_speed = 5
car_speed = 6
line_speed = 5

def spawn_enemy():
    x = random.randint(80, WIDTH - 80 - enemy_img.get_width())
    y = -enemy_img.get_height()
    game["enemies"].append([x, y])

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart on game over
        if game["game_over"]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game = reset_game()

    keys = pygame.key.get_pressed()

    if not game["game_over"]:
        # Movement
        if keys[pygame.K_LEFT] and game["car_x"] > 80:
            game["car_x"] -= car_speed
        if keys[pygame.K_RIGHT] and game["car_x"] < WIDTH - 80 - car_w:
            game["car_x"] += car_speed

        # Spawn enemies
        game["spawn_timer"] += 1
        if game["spawn_timer"] > 45:
            spawn_enemy()
            game["spawn_timer"] = 0

        # Move enemies
        for enemy in game["enemies"]:
            enemy[1] += enemy_speed

        # Move road lines
        for line in game["lines"]:
            line[1] += line_speed
            if line[1] > HEIGHT:
                line[1] = -40

        # Collision detection
        for enemy in game["enemies"]:
            if (game["car_x"] < enemy[0] + enemy_img.get_width() and
                game["car_x"] + car_w > enemy[0] and
                game["car_y"] < enemy[1] + enemy_img.get_height() and
                game["car_y"] + car_h > enemy[1]):
                game["game_over"] = True

        # Remove off-screen enemies
        game["enemies"] = [e for e in game["enemies"] if e[1] < HEIGHT]

        game["score"] += 1

    # Draw everything
    screen.fill(GRASS)
    pygame.draw.rect(screen, ROAD, (70, 0, WIDTH - 140, HEIGHT))

    # Road lines
    for line in game["lines"]:
        pygame.draw.rect(screen, YELLOW, (line[0], line[1], 10, 40))

    # Player
    screen.blit(player_img, (game["car_x"], game["car_y"]))

    # Enemies
    for enemy in game["enemies"]:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

    # Score
    score_text = font.render(str(game["score"]), True, TEXT)
    screen.blit(score_text, (10, 10))

    # Game Over screen
    if game["game_over"]:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        go_text = big_font.render("GAME OVER", True, (255, 50, 50))
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 80))

        restart_text = font.render("Press R to Restart", True, TEXT)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()
    clock.tick(60)
