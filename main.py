import pygame
import random
import sys

pygame.init()
pygame.mixer.init()



screen = pygame.display.set_mode(
    (0, 0),
    pygame.FULLSCREEN
)

WIDTH = screen.get_width()
HEIGHT = screen.get_height()

pygame.display.set_caption("Forentale")

clock = pygame.time.Clock()

FPS = 60



pygame.mixer.music.load("assets/music/menu.mp3")
pygame.mixer.music.play(-1)



def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()

    if size:
        image = pygame.transform.scale(
            image,
            size
        )

    return image




menu_bg = pygame.transform.scale(
    pygame.image.load(
        "assets/images/backgrounds/fon1.png"
    ).convert(),
    (WIDTH, HEIGHT)
)

intro_bg = pygame.transform.scale(
    pygame.image.load(
        "assets/images/backgrounds/fon2.png"
    ).convert(),
    (WIDTH, HEIGHT)
)

game_map = pygame.transform.scale(
    pygame.image.load(
        "assets/images/backgrounds/kar1.png"
    ).convert(),
    (WIDTH, HEIGHT)

)

game_map_2 = pygame.transform.scale(
    pygame.image.load(
        "assets/images/backgrounds/fon3.png"
    ).convert(),
    (WIDTH, HEIGHT)
)

after_boss_map = pygame.transform.scale(
    pygame.image.load(
        "assets/images/backgrounds/aftbs1.png"
    ).convert(),
    (WIDTH, HEIGHT)
)

end_screen_image = pygame.transform.scale(
    pygame.image.load(
        "assets/images/backgrounds/kar3.png"
    ).convert(),
    (WIDTH, HEIGHT)
)



logo = load_image(
    "assets/images/backgrounds/n1.png",
    (560, 230)
)

textbox = load_image(
    "assets/images/backgrounds/tt1.png",
    (1100, 220)
)
textbox2 = load_image(
    "assets/images/backgrounds/tt2.png",
    (1100, 220)
)
textbox3 = load_image(
    "assets/images/backgrounds/tt3.png",
    (1100, 220)
)



note_image = load_image(
    "assets/images/backgrounds/note1.png",
    (100, 100)
)


play_normal = load_image(
    "assets/images/buttons/k1.png",
    (200, 100)
)

play_hover = load_image(
    "assets/images/buttons/k2.png",
    (200, 100)
)

exit_normal = load_image(
    "assets/images/buttons/k3.png",
    (200, 100)
)

exit_hover = load_image(
    "assets/images/buttons/k4.png",
    (200, 100)
)



# DOWN
g1 = load_image("assets/images/player/g1.png", (96, 174))
g2 = load_image("assets/images/player/g2.png", (96, 174))
g3 = load_image("assets/images/player/g3.png", (96, 174))

# UP
g4 = load_image("assets/images/player/g4.png", (96, 174))
g5 = load_image("assets/images/player/g5.png", (96, 174))
g6 = load_image("assets/images/player/g6.png", (96, 174))

# LEFT
g7 = load_image("assets/images/player/g7.png", (96, 174))
g8 = load_image("assets/images/player/g8.png", (96, 174))
g9 = load_image("assets/images/player/g9.png", (96, 174))

# RIGHT
g10 = load_image("assets/images/player/g10.png", (96, 174))
g11 = load_image("assets/images/player/g11.png", (96, 174))
g12 = load_image("assets/images/player/g12.png", (96, 174))


npc_image = load_image("assets/images/backgrounds/npc.png", (140, 94)) # Замініть на свій розмір/шлях

bullet1 = load_image("assets/images/bullets/b1.png", (32, 32))
bullet2 = load_image("assets/images/bullets/b2.png", (32, 32))
bullet3 = load_image("assets/images/bullets/b3.png", (32, 32))

bullet_images = [bullet1, bullet2, bullet3]



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




class IntroScene:

    def __init__(self):

        # первая музыка
        pygame.mixer.music.load("assets/music/intro.wav")
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
            "*Я побачив дуже велику записку яка більше мене...*",
            "Що за...",
            "...",
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

                        pygame.mixer.music.load(
                            "assets/music/map1.mp3"
                        )

                        pygame.mixer.music.play(-1)

                        return "game"




class GameScene:

    def __init__(self):


        self.current_map = 1
        self.monster_alive = True
        self.stage = "PLAY"



        self.x = WIDTH // 2
        self.y = HEIGHT - 250
        self.speed = 3
        self.direction = "down"
        self.image = g1
        self.frame = 0
        self.anim_timer = 0
        self.moving = False

        self.after_death_return = False

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
            "*Лежить дуже велика та мокра записка від дощу.*",
            "Тут майже нічого не видно...",
            "Але здається тут написано...",
            "*Привіт!",
            "Я написала тобі записку за допомогою магії та телепортувала її сюди...*",
            "ось чому записка така велитенська...",
            "кхм...давайте далі",
            "*..Я не встигла віднести тебе до табору.",
            "Але, схоже, за всіма канонами цієї гри ти маєш дістатися туди сам...",
            "Будь обережним...",
            "...Лаурель*",
            "що за...",
            "гра?!?!",
            "що тут твориться!!!",
            "треба йти далі,і тоді я знайду відповідь на це питання"
        ]


        self.map2_text = "що за..."
        self.map2_visible = 0
        self.map2_timer = 0


        self.map2_text3 = "СРАЖАЙСЯ АБО ВМРИ!"
        self.map2_visible3 = 0
        self.map2_timer3 = 0




        self.monster_phase = 1


        self.font = pygame.font.SysFont("arial", 35)



        self.monster_image = load_image(
            "assets/images/backgrounds/monster.png",
            (160, 230)
        )

        self.monster_x = WIDTH // 2 - 90
        self.monster_y = HEIGHT // 2 - 140



        self.map_change_zone = pygame.Rect(WIDTH // 2 - 80, 0, 160, 60)



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


        self.npc_x = WIDTH // 2 - 48
        self.npc_y = HEIGHT // 2 - 100


        self.npc_rect = pygame.Rect(self.npc_x, self.npc_y, 96, 174)


        self.npc_dialog = [

            ("YOU", "То це ти?.."),
            ("YOU", "Лау..."),
            ("YOU", "Лару...."),

            ("NPC", "Лаурель!"),
            ("NPC", "Я тебе чекала!"),
            ("YOU", "Де я?Чому я тут опинився?!?!"),
            ("NPC", "А це вже ми дізнаємося в повній грі)"),
            ("NPC", "Бета версія закінчилась,дякую всім за увагу"),

        ]

        self.npc_index = 0
        self.npc_visible = 0
        self.npc_timer = 0



    def typewriter(self, text, visible, timer):
        timer += 1
        if timer >= 2:
            timer = 0
            if visible < len(text):
                visible += 1
        return visible, timer

    def typewriter2(self, text2, visible, timer):
        timer += 1
        if timer >= 2:
            timer = 0
            if visible < len(text2):
                visible += 1
        return visible, timer

    def typewriter3(self, text3, visible, timer):
        timer += 1
        if timer >= 2:
            timer = 0
            if visible < len(text3):
                visible += 1
        return visible, timer


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


    def update_idle(self):
        if self.direction == "down":
            self.image = g1
        elif self.direction == "up":
            self.image = g4
        elif self.direction == "left":
            self.image = g7
        elif self.direction == "right":
            self.image = g10



    def animate(self, a, b):
        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_timer = 0
            self.frame = 1 - self.frame
        return a if self.frame == 0 else b

    def update(self):


        if self.current_map == 1:
            screen.blit(game_map, (0, 0))
        elif self.current_map == 2:
            screen.blit(game_map_2, (0, 0))
        else:
            screen.blit(end_screen_image, (0, 0))



        if self.current_map == 1:
            screen.blit(note_image, (self.note_x, self.note_y))


        if self.current_map == 2 and self.monster_alive:
            screen.blit(self.monster_image, (self.monster_x, self.monster_y))


        if self.current_map == 3:
            screen.blit(npc_image, (self.npc_x, self.npc_y))


        if self.stage == "NPC_TEXT":

            speaker, current_text = self.npc_dialog[self.npc_index]


            if speaker == "YOU":
                screen.blit(textbox, (90, HEIGHT - 260))
            else:
                screen.blit(textbox2, (90, HEIGHT - 260))

            self.npc_visible, self.npc_timer = self.typewriter2(
                current_text,
                self.npc_visible,
                self.npc_timer
            )

            text = current_text[:self.npc_visible]


            name = "" if speaker == "YOU" else ""

            name_surface = self.font.render(
                name,
                True,
                (0, 0, 0)
            )

            screen.blit(name_surface, (140, HEIGHT - 220))

            # текст
            text_surface = self.font.render(
                text,
                True,
                (0, 0, 0)
            )

            screen.blit(text_surface, (150, HEIGHT - 170))


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


        if not self.moving:
            self.update_idle()


        rect = pygame.Rect(new_x, new_y, 64, 116)
        if not self.collision(rect):
            self.x = new_x
            self.y = new_y

        player_rect = pygame.Rect(self.x, self.y, 64, 116)


        if self.current_map == 1:
            if player_rect.colliderect(self.map_change_zone):
                self.current_map = 2
                self.x = WIDTH // 2
                self.y = HEIGHT - 200
                self.stage = "MONSTER_TEXT"

        elif self.current_map == 2 and not self.monster_alive:
            if player_rect.colliderect(self.map_change_zone):
                self.current_map = 3
                self.x = WIDTH // 2
                self.y = HEIGHT - 200
                self.stage = "PLAY"


        screen.blit(self.image, (self.x, self.y))


        if self.show_note:
            screen.blit(textbox, (90, HEIGHT - 260))
            current = self.note_texts[self.note_index]
            self.note_visible, self.note_timer = self.typewriter(current, self.note_visible, self.note_timer)
            text = current[:self.note_visible]
            screen.blit(self.font.render(text, True, (255, 255, 255)), (130, HEIGHT - 170))


        if self.stage == "MONSTER_TEXT":

            # ===== ПЕРВАЯ ТАБЛИЧКА tt1 =====
            if self.monster_phase == 1:

                screen.blit(textbox, (90, HEIGHT - 260))

                self.map2_visible, self.map2_timer = self.typewriter(
                    self.map2_text,
                    self.map2_visible,
                    self.map2_timer
                )

                text = self.map2_text[:self.map2_visible]

                screen.blit(
                    self.font.render(text, True, (255, 255, 255)),
                    (150, HEIGHT - 170)
                )

            elif self.monster_phase == 3:

                screen.blit(textbox3, (90, HEIGHT - 260))

                self.map2_visible3, self.map2_timer3 = self.typewriter3(
                    self.map2_text3,
                    self.map2_visible3,
                    self.map2_timer3
                )

                text3 = self.map2_text3[:self.map2_visible3]

                screen.blit(
                    self.font.render(text3, True, (255, 255, 255)),
                    (150, HEIGHT - 170)
                )




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RETURN:

                    if self.current_map == 1:
                        if player_rect.colliderect(self.note_rect):
                            if not self.show_note:
                                self.show_note = True
                                self.note_index = 0
                                self.note_visible = 0
                            else:
                                if self.note_visible >= len(self.note_texts[self.note_index]):
                                    self.note_index += 1
                                    self.note_visible = 0
                                    if self.note_index >= len(self.note_texts):
                                        self.show_note = False

                    elif self.stage == "MONSTER_TEXT" and self.current_map == 2:

                        if self.monster_phase == 1:

                            if self.map2_visible >= len(self.map2_text):
                                self.monster_phase = 3

                                self.map2_visible3 = 0
                                self.map2_timer3 = 0


                        elif self.monster_phase == 3:

                            if self.map2_visible3 >= len(self.map2_text3):
                                pygame.mixer.music.load("assets/music/batle.mp3")
                                pygame.mixer.music.play(-1)

                                return "battle"


                    elif self.current_map == 3:

                        if self.stage == "NPC_TEXT":

                            speaker, current_text = self.npc_dialog[self.npc_index]

                            if self.npc_visible >= len(current_text):

                                self.npc_index += 1
                                self.npc_visible = 0
                                self.npc_timer = 0


                                if self.npc_index >= len(self.npc_dialog):
                                    self.stage = "PLAY"
                                    self.npc_spoken = True


                        elif getattr(self, 'npc_spoken', False):
                            return "to_menu"


                        elif self.stage == "PLAY" and not getattr(self, 'npc_spoken', False):
                            if player_rect.colliderect(self.npc_rect):
                                self.stage = "NPC_TEXT"
                                self.npc_visible = 0
                                self.npc_timer = 0
                                self.npc_index = 0
        return None

class Bullet:

    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

        self.image = random.choice(bullet_images)
        self.rect_size = self.image.get_width()

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        screen.blit(self.image, (int(self.x), int(self.y)))

    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.rect_size,
            self.rect_size
        )

class BattleScene:

    def __init__(self):
        self.player_hp = 100
        self.enemy_hp = 100
        self.heals = 1
        self.font = pygame.font.SysFont(
            "arial",
            40
        )

        self.state = "MENU"
        self.options = [
            "ATTACK",
            "DEFEND",
            "HEAL"
        ]

        self.selected = 0
        self.pointer_x = 300
        self.pointer_speed = 10
        self.hit_zone = (500, 600)
        self.monster = load_image(
            "assets/images/backgrounds/monster.png",
            (220, 270)
        )



        self.shake = 0
        self.soul_x = WIDTH // 2
        self.soul_y = HEIGHT - 170
        self.soul_speed = 6
        self.bullets = []
        self.attack_timer = 0
        self.attack_duration = 360
        self.phase = 1
        self.invincible_timer = 0

    def draw_text(self, text, x, y, color=(255,255,255)):

        img = self.font.render(
            text,
            True,
            color
        )

        screen.blit(img, (x, y))

    def spawn_bullets(self):

        import random


        if self.phase == 1:

            for i in range(3):

                x = random.randint(420, 880)
                y = 390

                self.bullets.append(
                    Bullet(
                        x,
                        y,
                        0,
                        random.randint(5, 8)
                    )
                )

        elif self.phase == 2:

            for i in range(5):

                x = random.randint(420, 880)
                y = 390

                self.bullets.append(
                    Bullet(
                        x,
                        y,
                        random.randint(-2, 2),
                        random.randint(7, 11)
                    )
                )

        elif self.phase == 3:

            for i in range(8):

                x = random.randint(420, 880)
                y = 390

                self.bullets.append(
                    Bullet(
                        x,
                        y,
                        random.randint(-4, 4),
                        random.randint(10, 14)
                    )
                )

    def update(self):

        screen.fill((0, 0, 0))

        if self.enemy_hp <= 60:
            self.phase = 2

        if self.enemy_hp <= 25:
            self.phase = 3

        offset = 0

        if self.shake > 0:

            offset = -10 if self.shake % 2 == 0 else 10

            self.shake -= 1


        pygame.draw.rect(
            screen,
            (120, 0, 0),
            (0, 0, 0, 0)
        )
        screen.blit(
            self.monster,
            (550 + offset, 150)
        )

        self.draw_text(
            f"PLAYER HP: {self.player_hp}",
            80,
            80
        )

        self.draw_text(
            f"MONSTER HP: {self.enemy_hp}",
            80,
            140
        )

        self.draw_text(
            f"PHASE: {self.phase}",
            80,
            200
        )

        self.draw_text(
            f"HEALS: {self.heals}",
            80,
            260
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
                            self.selected = len(self.options) - 1

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

                            self.state = "DODGE"

                            self.attack_timer = 0


                        elif choice == "HEAL":

                            if self.heals > 0:

                                self.player_hp += 30

                                if self.player_hp > 100:
                                    self.player_hp = 100

                                self.heals -= 1

                            self.state = "DODGE"

                            self.attack_timer = 0

                elif self.state == "ATTACK":

                    if event.key == pygame.K_RETURN:

                        self.shake = 10

                        if self.hit_zone[0] <= self.pointer_x <= self.hit_zone[1]:

                            damage = 8

                        elif 450 <= self.pointer_x <= 650:

                            damage = 5

                        else:

                            damage = 2

                        self.enemy_hp -= damage

                        if self.enemy_hp <= 0:

                            game_scene.monster_alive = False
                            game_scene.stage = "PLAY"

                            game_scene.x = WIDTH // 2
                            game_scene.y = HEIGHT - 220

                            pygame.mixer.music.load(
                                "assets/music/map2.mp3"
                            )

                            pygame.mixer.music.play(-1)

                            return "game"

                        self.state = "DODGE"

                        self.attack_timer = 0

        if self.state == "MENU":

            self.draw_text(
                "Choose action:",
                80,
                340
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
                    420 + i * 70,
                    color
                )

        elif self.state == "ATTACK":

            pygame.draw.rect(
                screen,
                (100,100,100),
                (300, 650, 400, 30)
            )

            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    self.hit_zone[0],
                    650,
                    self.hit_zone[1] - self.hit_zone[0],
                    30
                )
            )

            pygame.draw.rect(
                screen,
                (255,0,0),
                (
                    self.pointer_x,
                    650,
                    10,
                    30
                )
            )

            self.pointer_x += self.pointer_speed

            if self.pointer_x <= 300:

                self.pointer_x = 300
                self.pointer_speed *= -1

            elif self.pointer_x >= 690:

                self.pointer_x = 690
                self.pointer_speed *= -1

            self.draw_text(
                "PRESS ENTER!",
                80,
                340
            )

        elif self.state == "DODGE":

            arena_x = 400
            arena_y = 420
            arena_w = 500
            arena_h = 250

            pygame.draw.rect(
                screen,
                (255,255,255),
                (arena_x, arena_y, arena_w, arena_h),
                4
            )

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.soul_x -= self.soul_speed

            if keys[pygame.K_d]:
                self.soul_x += self.soul_speed

            if keys[pygame.K_w]:
                self.soul_y -= self.soul_speed

            if keys[pygame.K_s]:
                self.soul_y += self.soul_speed

            self.soul_x = max(
                arena_x + 10,
                min(arena_x + arena_w - 10, self.soul_x)
            )

            self.soul_y = max(
                arena_y + 10,
                min(arena_y + arena_h - 10, self.soul_y)
            )

            self.attack_timer += 1

            if self.attack_timer % 20 == 0:
                self.spawn_bullets()

            soul_rect = pygame.Rect(
                self.soul_x - 8,
                self.soul_y - 8,
                16,
                16
            )

            if self.invincible_timer > 0:
                self.invincible_timer -= 1

            for bullet in self.bullets[:]:
                bullet.update()
                bullet.draw()

                if bullet.rect().colliderect(soul_rect):

                    if self.invincible_timer <= 0:
                        damage = 6

                        if self.phase == 2:
                            damage = 8

                        if self.phase == 3:
                            damage = 12

                        self.player_hp -= damage
                        self.invincible_timer = 30
                if bullet.y > HEIGHT + 100:

                    self.bullets.remove(bullet)

            pygame.draw.circle(
                screen,
                (255,0,0),
                (self.soul_x, self.soul_y),
                8
            )

            if self.attack_timer >= self.attack_duration:
                self.attack_timer = 0
                self.bullets.clear()
                self.state = "MENU"

        if self.player_hp <= 0:
            # возвращаем состояние игры
            game_scene.current_map = 2
            game_scene.stage = "MONSTER_TEXT"

            game_scene.monster_alive = True
            game_scene.x = WIDTH // 2
            game_scene.y = HEIGHT - 220


            game_scene.monster_phase = 1
            game_scene.map2_visible = 0
            game_scene.map2_timer = 0
            game_scene.map2_visible3 = 0
            game_scene.map2_timer3 = 0


            self.bullets.clear()
            self.player_hp = 100
            self.enemy_hp = 100
            self.state = "MENU"

            pygame.mixer.music.load("assets/music/map2.mp3")
            pygame.mixer.music.play(-1)

            return "game"

        return None


game_scene = None
scene = MenuScene()



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

    if result == "to_menu":
        game_scene = None
        scene = MenuScene()
        pygame.mixer.music.load("assets/music/menu.mp3")
        pygame.mixer.music.play(-1)

    pygame.display.update()

    clock.tick(FPS)
