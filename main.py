import pgzrun
import random
import pygame.mixer

WIDTH = 800
HEIGHT = 600
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_SPEED = 10
LIVES = 3
ENEMY_COUNT = 5

pygame.mixer.init()
pygame.mixer.music.load("music/music.mp3")
pygame.mixer.music.play(-1)

footstep_sound = pygame.mixer.Sound("music/step.mp3")
footstep_timer = 0
footstep_duration = 0.5


class AnimatedSprite:
    def __init__(self, image, position, anchor=('center', 'center')):
        self.actor = Actor(image, position, anchor=anchor)
        self.frame_count = 0

    def draw(self):
        self.actor.draw()

    def update_frame_count(self):
        self.frame_count += 1

    def update_animation(self):
        if self.frame_count % 20 == 0:
            if self.actor.image == "enemy1":
                self.actor.image = "enemy2"
            else:
                self.actor.image = "enemy1"


player = AnimatedSprite("hero1", (WIDTH / 2, HEIGHT - 50))
enemies = [AnimatedSprite("enemy1", (random.randint(50, WIDTH - 50), random.randint(0, 100))) for _ in
           range(ENEMY_COUNT)]
enemy_speeds = [random.uniform(1.0, 3.0) for _ in range(ENEMY_COUNT)]

platform = Actor("grass", (WIDTH / 2, HEIGHT - 10), anchor=('center', 'bottom'), height=20)

platform_blocks = []
for x in range(0, WIDTH, 50):
    block = Actor("grass", (x + 25, HEIGHT - 10), anchor=('center', 'bottom'))
    platform_blocks.append(block)

# Добавляем единичные блоки
for _ in range(20):
    x_pos = random.randint(0, WIDTH)
    y_pos = random.randint(0, HEIGHT)
    block = Actor("grass", (x_pos, y_pos), anchor=('center', 'bottom'))
    platform_blocks.append(block)

game_over = False
score = 0
lives = LIVES
timer = 0
player_flash_timer = 0
player_flash_interval = 20

menu_active = True
music_enabled = True
sound_enabled = True
footstep_sound_enabled = True

is_jumping = False
jump_height = 100
jump_velocity = 0


def draw():
    screen.fill((135, 206, 250))

    if menu_active:
        draw_menu()
    else:
        for block in platform_blocks:
            block.draw()

        if not game_over or (game_over and player_flash_timer % player_flash_interval < player_flash_interval / 2):
            player.draw()

        for enemy in enemies:
            enemy.draw()

        screen.draw.text("Score: " + str(score), color="black", topright=(WIDTH - 20, 10))
        screen.draw.text("Lives: " + str(lives), color="black", topleft=(20, 10))
        if game_over:
            screen.draw.text("Game Over!", color="black", center=(WIDTH / 2, HEIGHT / 2), fontsize=60)


def update():
    global game_over, timer, player_flash_timer

    if not game_over and not menu_active:
        update_player()
        update_enemies()

        on_platform = False
        for block in platform_blocks:
            if player.actor.colliderect(block):
                on_platform = True
                if jump_velocity <= 0:
                    player.actor.y = block.y - player.actor.height
                break

        if not on_platform and not is_jumping:
            player.actor.y += GRAVITY

        if player.actor.left < 0:
            player.actor.left = 0
        elif player.actor.right > WIDTH:
            player.actor.right = WIDTH

        for enemy in enemies:
            if player.actor.colliderect(enemy.actor):
                player_hit()

        timer += 1

    if lives <= 0:
        game_over = True
        player_flash_timer = 0

    if game_over:
        player_flash_timer += 1


def update_player():
    global score, is_jumping, jump_velocity

    on_platform = False  # Флаг, указывающий, находится ли игрок на платформе

    # Проверка, находится ли игрок на платформе
    for block in platform_blocks:
        if player.actor.colliderect(block):
            if player.actor.bottom <= block.top + 5:  # Игрок стоит на платформе
                on_platform = True
                player.actor.y = block.y - player.actor.height
                break

    # Управление игроком
    if keyboard.right:
        player.actor.x += PLAYER_SPEED
        player.actor.image = "hero2"
    elif keyboard.left:
        player.actor.x -= PLAYER_SPEED
        player.actor.image = "hero2"
    else:
        player.actor.image = "hero1"

    # Обработка прыжка
    if keyboard.space:
        if on_platform:  # Прыжок возможен только если игрок на платформе
            is_jumping = True
            jump_velocity = JUMP_SPEED


    if is_jumping:
        player.actor.y -= jump_velocity
        jump_velocity -= GRAVITY


        for block in platform_blocks:
            if player.actor.colliderect(block):
                if player.actor.bottom <= block.top + 5:
                    player.actor.y = block.y - player.actor.height
                    is_jumping = False
                    jump_velocity = 0
                    break


        if player.actor.y >= HEIGHT - player.actor.height:
            player.actor.y = HEIGHT - player.actor.height
            is_jumping = False
            jump_velocity = 0

    score += 1


def update_enemies():
    for enemy, speed in zip(enemies, enemy_speeds):
        enemy.actor.y += speed

        if enemy.actor.top > HEIGHT:
            enemy.actor.pos = (random.randint(50, WIDTH - 50), 0)
            speed = random.uniform(1.0, 3.0)

        enemy.update_frame_count()
        if enemy.frame_count % 40 == 0:
            enemy.update_animation()


def player_hit():
    global lives
    player.actor.pos = (WIDTH / 2, HEIGHT - 50)
    lives -= 1
    player_flash_timer = 1


def draw_menu():
    screen.draw.text("Main Menu", center=(WIDTH / 2, 100), fontsize=60, color="black")

    screen.draw.text("Начать игру", center=(WIDTH / 2, 200), fontsize=40, color="black")
    screen.draw.text("Вкл/Выкл музыку", center=(WIDTH / 2, 300), fontsize=40, color="black")
    screen.draw.text("Вкл/Выкл звуки", center=(WIDTH / 2, 400), fontsize=40, color="black")
    screen.draw.text("Выход", center=(WIDTH / 2, 500), fontsize=40, color="black")


def on_key_down(key):
    global menu_active

    if menu_active:
        if key == keys.ENTER:
            menu_active = False
        elif key == keys.ESCAPE:
            exit()


def on_mouse_down(pos):
    global menu_active, music_enabled, sound_enabled, footstep_sound_enabled

    if menu_active:
        if 150 <= pos[1] <= 250:
            menu_active = False
        elif 250 <= pos[1] <= 350:
            music_enabled = not music_enabled

            if music_enabled:
                print("Музыка включена")
                pygame.mixer.music.load("music/music.mp3")
                pygame.mixer.music.play(-1)
            else:
                print("Музыка выключена")
                pygame.mixer.music.stop()

        elif 350 <= pos[1] <= 450:

            footstep_sound_enabled = not footstep_sound_enabled

            if footstep_sound_enabled:
                print("Звуки ходьбы включены")
            else:
                print("Звуки ходьбы выключены")

        elif 450 <= pos[1] <= 550:
            exit()


pgzrun.go()