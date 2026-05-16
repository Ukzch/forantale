import pygame
import sys

pygame.init()

# =========================
# ЭКРАН
# =========================

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Big Map")

clock = pygame.time.Clock()

# =========================
# РАЗМЕРЫ БОЛЬШОЙ КАРТЫ
# =========================

MAP_WIDTH = 3000
MAP_HEIGHT = 2000

# =========================
# ЦВЕТА
# =========================

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

# =========================
# PLAYER
# =========================

class Player:

    def __init__(self, x, y, speed):

        self.x = x
        self.y = y

        self.speed = speed

        self.width = 50
        self.height = 50

    def move(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.speed

        if keys[pygame.K_d]:
            self.x += self.speed

        if keys[pygame.K_w]:
            self.y -= self.speed

        if keys[pygame.K_s]:
            self.y += self.speed

        # границы карты
        if self.x < 0:
            self.x = 0

        if self.y < 0:
            self.y = 0

        if self.x > MAP_WIDTH - self.width:
            self.x = MAP_WIDTH - self.width

        if self.y > MAP_HEIGHT - self.height:
            self.y = MAP_HEIGHT - self.height

    def draw(self, camera_x, camera_y):

        pygame.draw.rect(
            screen,
            RED,
            (
                self.x - camera_x,
                self.y - camera_y,
                self.width,
                self.height
            )
        )

# =========================
# ИГРОК
# =========================

player = Player(100, 300, 5)

# =========================
# КАРТЫ
# =========================

current_map = 1

# ДВЕРЬ В БЕЛУЮ КОМНАТУ
door_to_white = pygame.Rect(700, 250, 120, 220)

# ДВЕРЬ ОБРАТНО
door_to_black = pygame.Rect(200, 250, 120, 220)

# =========================
# GAME LOOP
# =========================

while True:

    # =========================
    # СОБЫТИЯ
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # =========================
    # ДВИЖЕНИЕ
    # =========================

    player.move()

    # =========================
    # RECT ИГРОКА
    # =========================

    player_rect = pygame.Rect(
        player.x,
        player.y,
        player.width,
        player.height
    )

    # =========================
    # ПЕРЕХОДЫ
    # =========================

    if current_map == 1:

        if player_rect.colliderect(door_to_white):

            current_map = 2

            player.x = 400
            player.y = 300

    elif current_map == 2:

        if player_rect.colliderect(door_to_black):

            current_map = 1

            player.x = 500
            player.y = 300

    # =========================
    # КАМЕРА
    # =========================

    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

    # ограничения камеры
    if camera_x < 0:
        camera_x = 0

    if camera_y < 0:
        camera_y = 0

    if camera_x > MAP_WIDTH - WIDTH:
        camera_x = MAP_WIDTH - WIDTH

    if camera_y > MAP_HEIGHT - HEIGHT:
        camera_y = MAP_HEIGHT - HEIGHT

    # =========================
    # ОТРИСОВКА КАРТ
    # =========================

    if current_map == 1:

        # чёрная карта
        screen.fill(BLACK)

        # зелёная дверь
        pygame.draw.rect(
            screen,
            GREEN,
            (
                door_to_white.x - camera_x,
                door_to_white.y - camera_y,
                door_to_white.width,
                door_to_white.height
            )
        )

    elif current_map == 2:

        # белая карта
        screen.fill(WHITE)

        # синяя дверь обратно
        pygame.draw.rect(
            screen,
            BLUE,
            (
                door_to_black.x - camera_x,
                door_to_black.y - camera_y,
                door_to_black.width,
                door_to_black.height
            )
        )

    # =========================
    # ИГРОК
    # =========================

    player.draw(camera_x, camera_y)

    # =========================
    # ОБНОВЛЕНИЕ
    # =========================

    pygame.display.update()

    clock.tick(100)