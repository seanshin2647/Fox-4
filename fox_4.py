# Fox 4
# Made by Sean Shin. Project started on 29/1/2019.

# This game will have the following aspects, the player will be a triangle and will be moved with the mouse.
# The bullets will be fired by clicking the mouse. The enemies will be red triangles and move down the screen.
# Once they reach a certain point, they will turn back. They will fire when they get within "range".
# The sprites will just consist of basic geometric shapes. No fancy graphics for now. Those come later.

# Its time. Let us begin.

import pygame, time, random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (200, 0, 0)
BLUE = (0, 200, 0)
GREEN = (0, 0, 200)

YELLOW = (200, 200, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # This part will be later changed to make these trianlges.
        self.side_length = 25

        self.image = pygame.Surface([self.side_length, self.side_length])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        self.rect.y = 0
        self.rect.x = random.randrange(0, DISPLAY_WIDTH - self.side_length)

        # I couldn't think of a better name for this variable. Sorry.
        random_number = random.randint(0, 2)

        if random_number == 0:
            self.side_speed = 0
        elif random_number == 1:
            self.side_speed = -3
        elif random_number == 2:
            self.side_speed = 3

        self.speed = 6
        self.turn_back = random.randrange((DISPLAY_HEIGHT * 0.3), (DISPLAY_HEIGHT * 0.8))

    def fire(self, player_x):
        if self.rect.x > player_x:
            enemy_bullet = Enemy_Bullet(-3, self.rect.x, self.rect.y)

            enemy_bullet_list.add(enemy_bullet)
            all_sprites_list.add(enemy_bullet)
        elif self.rect.x < player_x:
            enemy_bullet = Enemy_Bullet(3, self.rect.x, self.rect.y)

            enemy_bullet_list.add(enemy_bullet)
            all_sprites_list.add(enemy_bullet)
        else:
            enemy_bullet = Enemy_Bullet(0, self.rect.x, self.rect.y)

            enemy_bullet_list.add(enemy_bullet)
            all_sprites_list.add(enemy_bullet)

    def check_retreat(self):
        if self.rect.y >= self.turn_back:
            self.speed *= -1
            return True

        
    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.side_speed

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.side_length = 30

        self.image = pygame.Surface([self.side_length, self.side_length])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        self.rect.y = 200

    # Instead of using keybindings to move, I have opted to use the mouse until I decide not to.
    def update(self):
        x_pos, y_pos = pygame.mouse.get_pos()

        self.rect.x = x_pos - self.side_length / 2
        self.rect.y = y_pos - self.side_length / 2

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 4
        self.length = 14

        self.image = pygame.Surface([self.width, self.length])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 15

class Enemy_Bullet(Bullet):
    def __init__(self, angle_direction, enemy_location_x, enemy_location_y):
        super().__init__()
        
        self.image.fill(YELLOW)
        self.angle_direction = angle_direction

        self.length = 18

        self.rect.x = enemy_location_x
        self.rect.y = enemy_location_y

    def update(self):
        self.rect.y += 10
        self.rect.x += self.angle_direction

class Shotgun_Bullet(Bullet):
    def __init__(self, player_x, player_y, spread):
        super().__init__()

        self.image.fill(GREEN)

        self.spread = spread

        self.rect.x = player_x + 18
        self.rect.y = player_y + 15

        self.side_length = 8
        self.width = self.side_length
        self.length = self.side_length

    def update(self):
        self.rect.y -= 20
        self.rect.x += self.spread

# OOB stands for Out Of Bounds
def sprite_oob_check(current_x_position):
    if current_x_position < 0 or current_x_position > DISPLAY_WIDTH:
        return True
    else:
        return False

# This chunk of code is 100% foreign code. I didn't want to make my own text display
# function so I just copied this over.
def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    game_display.blit(TextSurf, TextRect)

    pygame.display.update()

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
                enemy.fire(player.rect.x)

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
        pygame.display.update()

        clock.tick(FPS)

    print("Enemies killed:", score)
    # Doing this to get a round percentage for the acuracy.
    print(str(int((bullets_hit/bullets_fired) * 100)) + "% Accuracy")
    pygame.quit()
    quit()

main_loop()
