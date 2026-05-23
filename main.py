import pygame
import sys

pygame.init()
pygame.mixer.init()

# =========================
# SCREEN
# =========================

screen = pygame.display.set_mode(
    (0, 0),
    pygame.FULLSCREEN
)

WIDTH = screen.get_width()
HEIGHT = screen.get_height()

pygame.display.set_caption("Forentale")

clock = pygame.time.Clock()

FPS = 60

# =========================
# MUSIC
# =========================

pygame.mixer.music.load("menu.mp3")
pygame.mixer.music.play(-1)

# =========================
# LOAD IMAGE
# =========================

def load_image(path, size=None):

    image = pygame.image.load(path).convert_alpha()

    if size:

        image = pygame.transform.scale(
            image,
            size
        )

    return image

# =========================
# BACKGROUNDS
# =========================

menu_bg = pygame.transform.scale(
    pygame.image.load(
        "assets/images/fon1.png"
    ).convert(),
    (WIDTH, HEIGHT)
)

intro_bg = pygame.transform.scale(
    pygame.image.load(
        "assets/images/fon2.png"
    ).convert(),
    (WIDTH, HEIGHT)
)

game_map = pygame.transform.scale(
    pygame.image.load(
        "assets/images/kar1.png"
    ).convert(),
    (WIDTH, HEIGHT)
)

# =========================
# UI
# =========================

logo = load_image(
    "assets/images/n1.png",
    (560,230)
)

textbox = load_image(
    "assets/images/tt1.png",
    (1100, 220)
)

# =========================
# NOTE IMAGE
# =========================

# РАЗМЕР ЗАПИСКИ:
# 80x80 или 100x100 идеально

note_image = load_image(
    "assets/images/note1.png",
    (100, 100)
)

# =========================
# BUTTONS
# =========================

play_normal = load_image(
    "assets/images/k1.png",
    (200, 100)
)

play_hover = load_image(
    "assets/images/k2.png",
    (200, 100)
)

exit_normal = load_image(
    "assets/images/k3.png",
    (200, 100)
)

exit_hover = load_image(
    "assets/images/k4.png",
    (200, 100)
)

# =========================
# PLAYER SPRITES
# =========================

# DOWN
g1 = load_image("assets/images/g1.png", (96, 174))
g2 = load_image("assets/images/g2.png", (96, 174))
g3 = load_image("assets/images/g3.png", (96, 174))

# UP
g4 = load_image("assets/images/g4.png", (96, 174))
g5 = load_image("assets/images/g5.png", (96, 174))
g6 = load_image("assets/images/g6.png", (96, 174))

# LEFT
g7 = load_image("assets/images/g7.png", (96, 174))
g8 = load_image("assets/images/g8.png", (96, 174))
g9 = load_image("assets/images/g9.png", (96, 174))

# RIGHT
g10 = load_image("assets/images/g10.png", (96, 174))
g11 = load_image("assets/images/g11.png", (96, 174))
g12 = load_image("assets/images/g12.png", (96, 174))

# =========================
# BUTTON CLASS
# =========================

class Button:

    def __init__(self, normal, hover, x, y):

        self.normal = normal
        self.hover = hover

        self.image = self.normal

        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def draw(self):

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):

            self.image = self.hover

        else:

            self.image = self.normal

        screen.blit(self.image, self.rect)

    def clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):

                return True

        return False

# =========================
# MENU
# =========================

class MenuScene:

    def __init__(self):

        self.play = Button(
            play_normal,
            play_hover,
            WIDTH // 2,
            HEIGHT // 2 - 50
        )

        self.exit = Button(
            exit_normal,
            exit_hover,
            WIDTH // 2,
            HEIGHT // 2 + 120
        )

        self.fade = 0
        self.start = False

    def update(self):

        screen.blit(menu_bg, (0, 0))

        screen.blit(
            logo,
            (WIDTH // 2 - 250, 40)
        )

        self.play.draw()
        self.exit.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

            if self.play.clicked(event):

                self.start = True

            if self.exit.clicked(event):

                pygame.quit()
                sys.exit()

        # fade
        if self.start:

            self.fade += 5

            fade_surface = pygame.Surface(
                (WIDTH, HEIGHT)
            )

            fade_surface.fill((0, 0, 0))

            fade_surface.set_alpha(self.fade)

            screen.blit(fade_surface, (0, 0))

            if self.fade >= 255:

                return "intro"

# =========================
# INTRO
# =========================

class IntroScene:

    def __init__(self):

        pygame.mixer.music.load("intro.wav")
        pygame.mixer.music.play(-1)

        self.font = pygame.font.SysFont(
            "arial",
            40
        )

        self.texts = [
            "Где я?..",
            "Что это за место?..",
            "Мне нужно идти дальше..."
        ]

        self.current_text = 0

        self.visible_characters = 0

        self.timer = 0

        self.fade = 255

    def update(self):

        screen.blit(intro_bg, (0, 0))

        screen.blit(
            textbox,
            (90, HEIGHT - 260)
        )

        # typewriter
        self.timer += 1

        if self.timer >= 2:

            self.timer = 0

            if self.visible_characters < len(
                self.texts[self.current_text]
            ):

                self.visible_characters += 1

        text = self.texts[
            self.current_text
        ][:self.visible_characters]

        text_surface = self.font.render(
            text,
            True,
            (255, 255, 255)
        )

        screen.blit(
            text_surface,
            (150, HEIGHT - 170)
        )

        # fade
        if self.fade > 0:

            self.fade -= 3

            fade_surface = pygame.Surface(
                (WIDTH, HEIGHT)
            )

            fade_surface.fill((0, 0, 0))

            fade_surface.set_alpha(self.fade)

            screen.blit(fade_surface, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RETURN:

                    self.current_text += 1

                    self.visible_characters = 0

                    if self.current_text >= len(
                        self.texts
                    ):

                        return "game"

# =========================
# GAME
# =========================

class GameScene:

    def __init__(self):

        # player
        self.x = WIDTH // 2
        self.y = HEIGHT - 250

        self.speed = 3

        # animation
        self.frame = 0
        self.timer = 0

        self.image = g1

        self.direction = "down"

        # =========================
        # WALLS
        # =========================

        self.walls = [

            # screen borders
            pygame.Rect(0, 0, WIDTH, 50),
            pygame.Rect(0, HEIGHT - 50, WIDTH, 50),
            pygame.Rect(0, 0, 50, HEIGHT),
            pygame.Rect(WIDTH - 50, 0, 50, HEIGHT),

            # trees
            pygame.Rect(230, 40, 20, 40),

            pygame.Rect(1200, 500, 200, 250),

            pygame.Rect(800, 700, 300, 150),
        ]

        # =========================
        # NOTE
        # =========================

        self.note_x = 900
        self.note_y = 400

        self.note_rect = pygame.Rect(
            self.note_x,
            self.note_y,
            100,
            100
        )

        self.show_note = False

        self.note_text = (
            "Лежит мокрая записка от дождя..."
        )

        self.font = pygame.font.SysFont(
            "arial",
            35
        )

    # =========================
    # COLLISION
    # =========================

    def collision(self, rect):

        for wall in self.walls:

            if rect.colliderect(wall):

                return True

        return False

    # =========================
    # ANIMATION
    # =========================

    def animate(self, img1, img2):

        self.timer += 1

        if self.timer >= 10:

            self.timer = 0

            self.frame = 1 - self.frame

        if self.frame == 0:

            return img1

        else:

            return img2

    # =========================
    # UPDATE
    # =========================

    def update(self):

        # map
        screen.blit(game_map, (0, 0))

        # =========================
        # NOTE IMAGE
        # =========================

        screen.blit(
            note_image,
            (self.note_x, self.note_y)
        )

        # movement
        new_x = self.x
        new_y = self.y

        keys = pygame.key.get_pressed()

        moving = False

        # LEFT
        if keys[pygame.K_a]:

            new_x -= self.speed

            self.image = self.animate(
                g8,
                g9
            )

            self.direction = "left"

            moving = True

        # RIGHT
        elif keys[pygame.K_d]:

            new_x += self.speed

            self.image = self.animate(
                g11,
                g12
            )

            self.direction = "right"

            moving = True

        # UP
        elif keys[pygame.K_w]:

            new_y -= self.speed

            self.image = self.animate(
                g5,
                g6
            )

            self.direction = "up"

            moving = True

        # DOWN
        elif keys[pygame.K_s]:

            new_y += self.speed

            self.image = self.animate(
                g2,
                g3
            )

            self.direction = "down"

            moving = True

        # idle
        if not moving:

            self.frame = 0

            if self.direction == "down":

                self.image = g1

            elif self.direction == "up":

                self.image = g4

            elif self.direction == "left":

                self.image = g7

            elif self.direction == "right":

                self.image = g10

        # collision
        rect = pygame.Rect(
            new_x,
            new_y,
            64,
            116
        )

        if not self.collision(rect):

            self.x = new_x
            self.y = new_y

        # draw player
        screen.blit(
            self.image,
            (self.x, self.y)
        )

        # =========================
        # NOTE TEXT
        # =========================

        if self.show_note:

            screen.blit(
                textbox,
                (90, HEIGHT - 260)
            )

            text_surface = self.font.render(
                self.note_text,
                True,
                (255, 255, 255)
            )

            screen.blit(
                text_surface,
                (140, HEIGHT - 170)
            )

        # =========================
        # EVENTS
        # =========================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # ESC
                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                # ENTER
                if event.key == pygame.K_RETURN:

                    player_rect = pygame.Rect(
                        self.x,
                        self.y,
                        64,
                        116
                    )

                    # interaction
                    if player_rect.colliderect(
                        self.note_rect
                    ):

                        self.show_note = not self.show_note

# =========================
# START
# =========================

scene = MenuScene()

# =========================
# MAIN LOOP
# =========================

while True:

    result = scene.update()

    if result == "intro":

        scene = IntroScene()

    if result == "game":

        scene = GameScene()

    pygame.display.update()

    clock.tick(FPS)