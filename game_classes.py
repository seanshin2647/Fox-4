import pygame, random

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

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

    def fire(self, player_x, all_sprites_list, enemy_bullet_list):
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
        self.image.fill(GREEN)
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