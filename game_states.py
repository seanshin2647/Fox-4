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