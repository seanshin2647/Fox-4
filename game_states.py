from game_classes import *

class State():
    def __init__(self):
        pass

    def render(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self):
        raise NotImplementedError

class Game_State(State):
    def __init__(self):
        super().__init__()

        self.all_sprites_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.enemy_bullet_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        # This list is not strictly necessary but to take advantage of 
        # pygame's collision detection I added it here.
        self.player_list = pygame.sprite.Group()

        self.player = Player()
        append_list(self.player, self.player_list)

        self.score = 0
        self.lives = 3
        self.bullets_fired = 0
        self.bullets_hit = 0

        self.enemy_spawn_countdown = 0
        self.shotgun_cooldown = 600
        self.spread = -20

    def render(self, display):
        self.all_sprites_list.draw(display)
        self.shotgun_display(self.shotgun_cooldown)

    def update(self):

    def handle_events(self):

    # For appending things to lists. I addd this to make the code cleaner.
    def append_list(self, append_object, append_list):
        append_list.add(append_object)

    def shotgun_display(self, display, display_width, display_height):
        pygame.draw.rect(display, BLUE, [(display_width * 0.75), (display_height * 0.9), (self.shotgun_cooldown / 4), 15])
    
    def fire_bullets(self):
        # Bullet on the right side.
        self.right_bullet = Bullet()
        self.right_bullet.rect.x = self.player.rect.x + (self.player.side_length * 0.75)
        self.right_bullet.rect.y = self.player.rect.y

        self.all_sprites_list.add(self.right_bullet)
        self.bullet_list.add(self.right_bullet)
        
        # Bullet on the left side.
        self.left_bullet = Bullet()
        self.left_bullet.rect.x = self.player.rect.x + (self.player.side_length * 0.25)
        self.left_bullet.rect.y = self.player.rect.y

        self.all_sprites_list.add(self.left_bullet)
        self.bullet_list.add(self.left_bullet)
        
        self.bullets_fired += 1