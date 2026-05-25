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

game_map_2 = pygame.transform.scale(
    pygame.image.load(
        "assets/images/fon3.png"
    ).convert(),
    (WIDTH, HEIGHT)
)

after_boss_map = pygame.transform.scale(
    pygame.image.load(
        "assets/images/aftbs1.png"
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

        # первая музыка
        pygame.mixer.music.load("intro.wav")
        pygame.mixer.music.play(-1)

        self.second_music = False

        self.font = pygame.font.SysFont(
            "arial",
            40
        )

        self.texts = [
            "Де я?..",
            "Що це за місто?..",
            "...",
            " *Ти побачив записку* ",
            "Мені треба йти до записки",
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
                        # вторая музыка
                        pygame.mixer.music.load(
                            "1s-part.mp3"
                        )

                        pygame.mixer.music.play(-1)

                        return "game"


# =========================
# GAME
# =========================

class GameScene:

    def __init__(self):

        # =========================
        # MAP
        # =========================

        self.current_map = 1

        self.monster_alive = True

        self.stage = "PLAY"

        # =========================
        # PLAYER
        # =========================

        self.x = WIDTH // 2
        self.y = HEIGHT - 250

        self.speed = 3

        self.direction = "down"

        self.image = g1

        self.frame = 0
        self.anim_timer = 0

        self.moving = False

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

        self.note_index = 0

        self.note_visible = 0
        self.note_timer = 0

        self.note_texts = [
            "*Лежить мокра записка від дощу.*",
            "Тут майже нічого не видно...",
            "Але здається тут написано...",
            "*Привіт!*",
            "Я написала тобі записку...",
            "Будь обережним...",
            "...Лаурель*"
        ]

        # =========================
        # MONSTER TEXT
        # =========================

        self.map2_text = "ЩО ЦЕ ЗА МОНСТР?!"

        self.map2_visible = 0
        self.map2_timer = 0

        # =========================
        # FONT
        # =========================

        self.font = pygame.font.SysFont(
            "arial",
            35
        )

        # =========================
        # MONSTER
        # =========================

        self.monster_image = load_image(
            "assets/images/monster.png",
            (250, 300)
        )

        self.monster_x = WIDTH // 2 - 120
        self.monster_y = HEIGHT // 2 - 180

        # =========================
        # MAP CHANGE
        # =========================

        self.map_change_zone = pygame.Rect(
            WIDTH // 2 - 80,
            0,
            160,
            60
        )

        # =========================
        # WALLS
        # =========================

        self.walls_map1 = [
            pygame.Rect(0, HEIGHT - 50, WIDTH, 50),
            pygame.Rect(0, 0, 50, HEIGHT),
            pygame.Rect(WIDTH - 50, 0, 50, HEIGHT),
        ]

        self.walls_map2 = [
            pygame.Rect(0, HEIGHT - 50, WIDTH, 50),
            pygame.Rect(0, 0, 50, HEIGHT),
            pygame.Rect(WIDTH - 50, 0, 50, HEIGHT),
        ]

        self.walls_map3 = [
            pygame.Rect(0, HEIGHT - 50, WIDTH, 50),
            pygame.Rect(0, 0, 50, HEIGHT),
            pygame.Rect(WIDTH - 50, 0, 50, HEIGHT),
        ]

    # =========================
    # TYPEWRITER
    # =========================

    def typewriter(self, text, visible, timer):

        timer += 1

        if timer >= 2:

            timer = 0

            if visible < len(text):

                visible += 1

        return visible, timer

    # =========================
    # COLLISION
    # =========================

    def collision(self, rect):

        if self.current_map == 1:
            walls = self.walls_map1

        elif self.current_map == 2:
            walls = self.walls_map2

        else:
            walls = self.walls_map3

        for wall in walls:

            if rect.colliderect(wall):

                return True

        return False

    # =========================
    # IDLE
    # =========================

    def update_idle(self):

        if self.direction == "down":
            self.image = g1

        elif self.direction == "up":
            self.image = g4

        elif self.direction == "left":
            self.image = g7

        elif self.direction == "right":
            self.image = g10

    # =========================
    # ANIMATION
    # =========================

    def animate(self, a, b):

        self.anim_timer += 1

        if self.anim_timer >= 10:

            self.anim_timer = 0

            self.frame = 1 - self.frame

        return a if self.frame == 0 else b

    # =========================
    # UPDATE
    # =========================

    def update(self):

        # =========================
        # DRAW MAP
        # =========================

        if self.current_map == 1:

            screen.blit(game_map, (0, 0))

        elif self.current_map == 2:

            screen.blit(game_map_2, (0, 0))

        else:

            screen.blit(after_boss_map, (0, 0))

        # =========================
        # NOTE
        # =========================

        if self.current_map == 1:

            screen.blit(
                note_image,
                (self.note_x, self.note_y)
            )

        # =========================
        # MONSTER
        # =========================

        if self.current_map == 2 and self.monster_alive:

            screen.blit(
                self.monster_image,
                (self.monster_x, self.monster_y)
            )

        # =========================
        # MOVEMENT
        # =========================

        new_x = self.x
        new_y = self.y

        self.moving = False

        keys = pygame.key.get_pressed()

        if self.stage == "PLAY":

            if keys[pygame.K_a]:

                new_x -= self.speed

                self.image = self.animate(g8, g9)

                self.direction = "left"

                self.moving = True

            elif keys[pygame.K_d]:

                new_x += self.speed

                self.image = self.animate(g11, g12)

                self.direction = "right"

                self.moving = True

            elif keys[pygame.K_w]:

                new_y -= self.speed

                self.image = self.animate(g5, g6)

                self.direction = "up"

                self.moving = True

            elif keys[pygame.K_s]:

                new_y += self.speed

                self.image = self.animate(g2, g3)

                self.direction = "down"

                self.moving = True

        # =========================
        # IDLE FIX
        # =========================

        if not self.moving:

            self.update_idle()

        # =========================
        # COLLISION
        # =========================

        rect = pygame.Rect(
            new_x,
            new_y,
            64,
            116
        )

        if not self.collision(rect):

            self.x = new_x
            self.y = new_y

        player_rect = pygame.Rect(
            self.x,
            self.y,
            64,
            116
        )

        # =========================
        # MAP CHANGE
        # =========================

        if self.current_map == 1:

            if player_rect.colliderect(self.map_change_zone):

                self.current_map = 2

                self.x = WIDTH // 2
                self.y = HEIGHT - 200

                self.stage = "MONSTER_TEXT"

        # =========================
        # PLAYER
        # =========================

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

            current = self.note_texts[
                self.note_index
            ]

            self.note_visible, self.note_timer = self.typewriter(
                current,
                self.note_visible,
                self.note_timer
            )

            text = current[:self.note_visible]

            screen.blit(
                self.font.render(
                    text,
                    True,
                    (255,255,255)
                ),
                (130, HEIGHT - 170)
            )

        # =========================
        # MONSTER TEXT
        # =========================

        if self.stage == "MONSTER_TEXT":

            # ТАБЛИЦА ПОВЕРХ ПЕРСОНАЖА

            screen.blit(
                textbox,
                (90, HEIGHT - 260)
            )

            self.map2_visible, self.map2_timer = self.typewriter(
                self.map2_text,
                self.map2_visible,
                self.map2_timer
            )

            text = self.map2_text[:self.map2_visible]

            screen.blit(
                self.font.render(
                    text,
                    True,
                    (255,255,255)
                ),
                (150, HEIGHT - 170)
            )

        # =========================
        # EVENTS
        # =========================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RETURN:

                    # NOTE
                    if self.current_map == 1:

                        if player_rect.colliderect(
                            self.note_rect
                        ):

                            if not self.show_note:

                                self.show_note = True

                                self.note_index = 0
                                self.note_visible = 0

                            else:

                                if self.note_visible >= len(
                                    self.note_texts[self.note_index]
                                ):

                                    self.note_index += 1

                                    self.note_visible = 0

                                    if self.note_index >= len(
                                        self.note_texts
                                    ):

                                        self.show_note = False

                    # MONSTER
                    if self.stage == "MONSTER_TEXT":

                        if self.map2_visible >= len(
                            self.map2_text
                        ):

                            pygame.mixer.music.load(
                                "batle.mp3"
                            )

                            pygame.mixer.music.play(-1)

                            return "battle"

        return None


class BattleScene:

    def __init__(self):

        self.player_hp = 100
        self.enemy_hp = 100

        self.font = pygame.font.SysFont(
            "arial",
            40
        )

        self.state = "MENU"

        self.options = [
            "ATTACK",
            "DEFEND",
            "RUN"
        ]

        self.selected = 0

        self.pointer_x = 300

        self.pointer_speed = 8

        self.hit_zone = (
            500,
            600
        )

        self.enemy_timer = 0

        self.defending = False

        # MONSTER IMAGE
        self.monster = load_image(
            "assets/images/monster.png",
            (350, 420)
        )

        self.shake = 0

    # =========================
    # TEXT
    # =========================

    def draw_text(self, text, x, y, color=(255,255,255)):

        img = self.font.render(
            text,
            True,
            color
        )

        screen.blit(img, (x,y))

    # =========================
    # UPDATE
    # =========================

    def update(self):

        screen.fill((0,0,0))

        # MONSTER BG
        pygame.draw.rect(
            screen,
            (120,0,0),
            (820,120,400,500)
        )

        # SHAKE
        offset = 0

        if self.shake > 0:

            offset = -10 if self.shake % 2 == 0 else 10

            self.shake -= 1

        # MONSTER
        screen.blit(
            self.monster,
            (850 + offset, 140)
        )

        # HP
        self.draw_text(
            f"PLAYER HP: {self.player_hp}",
            100,
            100
        )

        self.draw_text(
            f"MONSTER HP: {self.enemy_hp}",
            100,
            160
        )

        # EVENTS
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if self.state == "MENU":

                    if event.key == pygame.K_UP:

                        self.selected -= 1

                        if self.selected < 0:

                            self.selected = len(self.options)-1

                    if event.key == pygame.K_DOWN:

                        self.selected += 1

                        if self.selected >= len(self.options):

                            self.selected = 0

                    if event.key == pygame.K_RETURN:

                        choice = self.options[self.selected]

                        if choice == "ATTACK":

                            self.state = "ATTACK"

                            self.pointer_x = 300

                        elif choice == "DEFEND":

                            self.defending = True

                            self.state = "ENEMY"

                        elif choice == "RUN":

                            return "game"

                elif self.state == "ATTACK":

                    if event.key == pygame.K_RETURN:

                        self.shake = 10

                        if self.hit_zone[0] <= self.pointer_x <= self.hit_zone[1]:

                            self.enemy_hp -= 25

                        else:

                            self.enemy_hp -= 10

                        if self.enemy_hp <= 0:

                            game_scene.boss_dead = True

                            pygame.mixer.music.load(
                                "1s-part.mp3"
                            )

                            pygame.mixer.music.play(-1)

                            return "game"

                        else:

                            self.state = "ENEMY"

        # MENU
        if self.state == "MENU":

            self.draw_text(
                "Choose action:",
                100,
                260
            )

            for i, option in enumerate(self.options):

                color = (
                    (255,255,0)
                    if i == self.selected
                    else
                    (255,255,255)
                )

                self.draw_text(
                    option,
                    100,
                    340 + i*60,
                    color
                )

        # ATTACK
        elif self.state == "ATTACK":

            pygame.draw.rect(
                screen,
                (100,100,100),
                (300,450,400,30)
            )

            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    self.hit_zone[0],
                    450,
                    self.hit_zone[1]-self.hit_zone[0],
                    30
                )
            )

            pygame.draw.rect(
                screen,
                (255,0,0),
                (
                    self.pointer_x,
                    450,
                    10,
                    30
                )
            )

            self.pointer_x += self.pointer_speed

            if self.pointer_x <= 300 or self.pointer_x >= 700:

                self.pointer_speed *= -1

        # ENEMY
        elif self.state == "ENEMY":

            self.draw_text(
                "Enemy attacks...",
                100,
                300
            )

            self.enemy_timer += 1

            if self.enemy_timer >= 60:

                self.enemy_timer = 0

                damage = 10

                if self.defending:

                    damage = 3

                    self.defending = False

                self.player_hp -= damage

                if self.player_hp <= 0:

                    self.player_hp = 0

                self.state = "MENU"

        return None


# =========================
# START
# =========================
game_scene = None
scene = MenuScene()

# =========================
# MAIN LOOP
# =========================

while True:

    result = scene.update()

    if result == "intro":

        scene = IntroScene()

    if result == "game":

        if game_scene is None:
            game_scene = GameScene()

        scene = game_scene

    if result == "battle":
        game_scene = scene

        scene = BattleScene()

    pygame.display.update()

    clock.tick(FPS)


class BattleScene:

    def __init__(self):

        self.player_hp = 100
        self.enemy_hp = 100

        self.font = pygame.font.SysFont(
            "arial",
            40
        )

        self.state = "MENU"

        self.options = [
            "ATTACK",
            "DEFEND",
            "RUN"
        ]

        self.selected = 0

        self.pointer_x = 300

        self.pointer_speed = 8

        self.hit_zone = (
            500,
            600
        )

        self.enemy_timer = 0

        self.defending = False

        self.monster = load_image(
            "assets/images/monster.png",
            (350, 420)
        )

        self.shake = 0

    def draw_text(self, text, x, y, color=(255,255,255)):

        img = self.font.render(
            text,
            True,
            color
        )

        screen.blit(img, (x,y))

    def update(self):

        screen.fill((0,0,0))

        pygame.draw.rect(
            screen,
            (120,0,0),
            (820,120,400,500)
        )

        offset = 0

        if self.shake > 0:

            offset = -10 if self.shake % 2 == 0 else 10

            self.shake -= 1

        screen.blit(
            self.monster,
            (850 + offset, 140)
        )

        self.draw_text(
            f"PLAYER HP: {self.player_hp}",
            100,
            100
        )

        self.draw_text(
            f"MONSTER HP: {self.enemy_hp}",
            100,
            160
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if self.state == "MENU":

                    if event.key == pygame.K_UP:

                        self.selected -= 1

                        if self.selected < 0:

                            self.selected = len(self.options)-1

                    if event.key == pygame.K_DOWN:

                        self.selected += 1

                        if self.selected >= len(self.options):

                            self.selected = 0

                    if event.key == pygame.K_RETURN:

                        choice = self.options[self.selected]

                        if choice == "ATTACK":

                            self.state = "ATTACK"

                            self.pointer_x = 300

                        elif choice == "DEFEND":

                            self.defending = True

                            self.state = "ENEMY"

                        elif choice == "RUN":

                            return "game"

                elif self.state == "ATTACK":

                    if event.key == pygame.K_RETURN:

                        self.shake = 10

                        if self.hit_zone[0] <= self.pointer_x <= self.hit_zone[1]:

                            self.enemy_hp -= 25

                        else:

                            self.enemy_hp -= 10

                        if self.enemy_hp <= 0:

                            game_scene.monster_alive = False

                            game_scene.stage = "PLAY"

                            game_scene.current_map = 3

                            game_scene.x = WIDTH // 2
                            game_scene.y = HEIGHT - 220

                            pygame.mixer.music.load(
                                "son2p.mp3"
                            )

                            pygame.mixer.music.play(-1)

                            return "game"

                        else:

                            self.state = "ENEMY"

        if self.state == "MENU":

            self.draw_text(
                "Choose action:",
                100,
                260
            )

            for i, option in enumerate(self.options):

                color = (
                    (255,255,0)
                    if i == self.selected
                    else
                    (255,255,255)
                )

                self.draw_text(
                    option,
                    100,
                    340 + i*60,
                    color
                )

        elif self.state == "ATTACK":

            pygame.draw.rect(
                screen,
                (100,100,100),
                (300,450,400,30)
            )

            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    self.hit_zone[0],
                    450,
                    self.hit_zone[1]-self.hit_zone[0],
                    30
                )
            )

            pygame.draw.rect(
                screen,
                (255,0,0),
                (
                    self.pointer_x,
                    450,
                    10,
                    30
                )
            )

            self.pointer_x += self.pointer_speed

            if self.pointer_x <= 300 or self.pointer_x >= 700:

                self.pointer_speed *= -1

            self.draw_text(
                "PRESS ENTER!",
                100,
                300
            )

        elif self.state == "ENEMY":

            self.draw_text(
                "Enemy attacks...",
                100,
                300
            )

            self.enemy_timer += 1

            if self.enemy_timer >= 60:

                self.enemy_timer = 0

                damage = 10

                if self.defending:

                    damage = 3

                    self.defending = False

                self.player_hp -= damage

                self.state = "MENU"

        return None


# =========================
# START
# =========================
game_scene = None
scene = MenuScene()

# =========================
# MAIN LOOP
# =========================

while True:

    result = scene.update()

    if result == "intro":

        scene = IntroScene()

    if result == "game":

        if game_scene is None:
            game_scene = GameScene()

        scene = game_scene

    if result == "battle":
        game_scene = scene

        scene = BattleScene()

    pygame.display.update()

    clock.tick(FPS)
