import pgzrun
import random
import pygame.mixer

WIDTH = 800
HEIGHT = 600
GRAVITY = 0.5
PLAYER_SPEED = 5
LIVES = 3
ENEMY_COUNT = 5

pygame.mixer.init()
pygame.mixer.music.load("music/music.mp3")
pygame.mixer.music.play(-1)

footstep_sound = pygame.mixer.Sound("music/step.mp3")
footstep_timer = 0
footstep_duration = 0.5

player = Actor("hero1", (WIDTH / 2, HEIGHT - 50))
enemies = [Actor("enemy1", (random.randint(50, WIDTH - 50), random.randint(0, 100))) for _ in range(ENEMY_COUNT)]
enemy_speeds = [random.uniform(1.0, 3.0) for _ in range(ENEMY_COUNT)]


platform = Actor("grass", (WIDTH / 2, HEIGHT - 10), anchor=('center', 'bottom'), height=20)


platform_blocks = []
for x in range(0, WIDTH, 50):
    block = Actor("grass", (x + 25, HEIGHT - 10), anchor=('center', 'bottom'))
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
            if player.colliderect(block):
                on_platform = True
                player.y = block.y - player.height
                break

        if not on_platform:
            player.y += GRAVITY

        if player.left < 0:
            player.left = 0
        elif player.right > WIDTH:
            player.right = WIDTH

        for enemy in enemies:
            if player.colliderect(enemy):
                player_hit()

        timer += 1

    if lives <= 0:
        game_over = True
        player_flash_timer = 0

    if game_over:
        player_flash_timer += 1


def update_player():
    global score, footstep_timer

    if keyboard.right:
        player.x += PLAYER_SPEED
        player.image = "hero2"

        if footstep_timer >= footstep_duration and sound_enabled and footstep_sound_enabled:
            footstep_sound.play()
            footstep_timer = 0
    elif keyboard.left:
        player.x -= PLAYER_SPEED
        player.image = "hero2"

        if footstep_timer >= footstep_duration and sound_enabled and footstep_sound_enabled:
            footstep_sound.play()
            footstep_timer = 0
    else:
        player.image = "hero1"

    footstep_timer += 1 / 60

    score += 1


def update_enemies():
    for enemy, speed in zip(enemies, enemy_speeds):
        enemy.y += speed

        if enemy.top > HEIGHT:
            enemy.pos = (random.randint(50, WIDTH - 50), 0)
            speed = random.uniform(1.0, 3.0)


def player_hit():
    global lives
    player.pos = (WIDTH / 2, HEIGHT - 50)
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
