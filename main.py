# Fox 4
# Made by Sean Shin. Project started on 29/1/2019.

import pygame, time, random
from game_states import *

# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)

# RED = (200, 0, 0)
# GREEN = (0, 200, 0)
# BLUE = (0, 0, 200)

# YELLOW = (200, 200, 0)

# OOB stands for Out Of Bounds
def sprite_oob_check(current_x_position):
    if current_x_position < 0 or current_x_position > DISPLAY_WIDTH:
        return True
    else:
        return False

# This chunk of code is ~~100% foreign~~ partly my own code. I didn't want to make my own text display
# function so I just copied ^and edited^ this over.
def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def message_display(x_location, y_location, text):
    largeText = pygame.font.Font('freesansbold.ttf', 30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x_location, y_location)
    game_display.blit(TextSurf, TextRect)

    pygame.display.update()

def shotgun_display(shotgun_cooldown):
    pygame.draw.rect(DISPLAY, BLUE, [(DISPLAY_WIDTH * 0.75), (DISPLAY_HEIGHT * 0.9), (shotgun_cooldown / 4), 15])

# Here begins the code for the main loop.
pygame.init()

FPS = 60
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

DISPLAY = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])

all_sprites_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
enemy_bullet_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

# I don't really need this list.
# However, to use pygame's collision detection, I need a group/list.
# Which is why I have this list.
player_list = pygame.sprite.Group()

clock = pygame.time.Clock()

def main_loop():
    game_exit = False

    player = Player()
    all_sprites_list.add(player)
    player_lives = 3
    score = 0

    bullets_fired = 0
    bullets_hit = 0

    enemy_spawn_countdown = 0
    shotgun_cooldown = 600
    spread = -20

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Bullet on the right side.
                right_bullet = Bullet()
                right_bullet.rect.x = player.rect.x + (player.side_length * 0.75)
                right_bullet.rect.y = player.rect.y

                all_sprites_list.add(right_bullet)
                bullet_list.add(right_bullet)
                
                # Bullet on the left side.
                left_bullet = Bullet()
                left_bullet.rect.x = player.rect.x + (player.side_length * 0.25)
                left_bullet.rect.y = player.rect.y

                all_sprites_list.add(left_bullet)
                bullet_list.add(left_bullet)
                
                bullets_fired += 1

            pressed_button = pygame.key.get_pressed()
            if pressed_button[pygame.K_SPACE]:
                if shotgun_cooldown == 600:
                    for create_bullets in range (20):
                        shotgun_bullet = Shotgun_Bullet(player.rect.x, player.rect.y, spread)
                        all_sprites_list.add(shotgun_bullet)
                        bullet_list.add(shotgun_bullet)
                        spread += 2

                    shotgun_cooldown = 0
                    spread = -20

        if player_lives == 0:
            game_exit = True

        if shotgun_cooldown < 600:
            shotgun_cooldown += 1

        enemy_spawn_countdown += random.randrange(1, 5)
        
        if enemy_spawn_countdown >= 30:
            enemy = Enemy()
            enemy_list.add(enemy)
            all_sprites_list.add(enemy)

            enemy_spawn_countdown = 0

        for enemy in enemy_list:
            if enemy.check_retreat():
                enemy.fire(player.rect.x, all_sprites_list, enemy_bullet_list)

            if sprite_oob_check(enemy.rect.x):
                enemy.side_speed *= -1
            
            if enemy.rect.y < 0:
                enemy.kill()

            if pygame.sprite.spritecollide(player, enemy_list, True):
                player_lives -= 1

            
        for bullet in bullet_list:
            hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)

            for enemies in hit_list:
                bullet.kill()
                score += 1
                bullets_hit += 1

            if bullet.rect.y < 0:
                bullet.kill()

        for enemy_bullet in enemy_bullet_list:
            if enemy_bullet.rect.y > DISPLAY_HEIGHT:
                enemy_bullet.kill()

            if pygame.sprite.spritecollide(player, enemy_bullet_list, True):
                player_lives -= 1

        all_sprites_list.update()


        DISPLAY.fill(BLACK)
        all_sprites_list.draw(DISPLAY)
        shotgun_display(shotgun_cooldown)
        pygame.display.update()

        clock.tick(FPS)

    print("Enemies killed:", score)
    # Doing this to get a round percentage for the acuracy.
    print(str(int((bullets_hit/bullets_fired) * 100)) + "% Accuracy")
    pygame.quit()
    quit()

main_loop()