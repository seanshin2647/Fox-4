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

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # This part will be later changed to make these trianlges.
        self.side_length = 25

        self.image = pygame.Surface([self.side_length, self.side_length])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        self.speed = 6
        self.turn_back = random.randrange((DISLAY_HEIGHT * 0.5), (DISPLAY_HEIGHT * 0.8))

    def check_retreat(self):
        if self.rect.y >= turn_back:
            self.speed *= -1
        
    def update(self):
        self.rect.y -= self.speed

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

        self.rect.x = x_pos + self.side_length / 2
        self.rect.y = y_pos + self.side_length / 2

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 3
        self.length = 10

        self.image = pygame.Surface([self.width, self.length])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 7

# Here begins the code for the main loop.
pygame.init()

FPS = 60
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

DISPLAY = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])

all_sprites_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

clock = pygame.time.Clock()

def main_loop():
    game_exit = False

    player = Player()
    all_sprites_list.add(player)

    enemy_spawn_countdown = 0

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet()
                bullet.rect.x = player.rect.x + (player.side_length/2)
                bullet.rect.y = player.rect.y

                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

        enemy_spawn_countdown += random.randgrange(1, 5)
        
        if enemy_spawn_countdown >= 45:
            enemy = Enemy()
            
            enemy_list.add(enemy)
            all_sprites_list.add(enemy)
            
        for enemy in enemy_list:
            enemy.check_retreat()
            
            if enemy.rect.y < 0:
                enemy_list.remove(enemy)
                all_sprites_list.remove(enemy)
            
        for bullet in bullet_list:
            hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)

            for enemies in hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

            if bullet.rect.y < 0:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        all_sprites_list.update()

        DISPLAY.fill(BLACK)
        all_sprites_list.draw(DISPLAY)
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()

main_loop()
