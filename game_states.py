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

# WIP. Work on this later.
class Main_Menu(State):
    def __init__(self):
        super().__init__()

        self.title_font = pygame.font.SysFont('Roboto', 56)
        self.subtitle_font = pygame.font.SysFont('Arial', 24)
        self.MAIN_MENU_COLOR = (110, 173, 153)
        self.TITLE_COLOR = (165, 173, 110)

    def render(self, display, display_width, display_height):
        display.fill(MAIN_MENU_COLOR)
        title = self.font.render('Fox 4', True, self.TITLE_COLOR)
        instructions = self.font.render('Press <enter> To Start Game', True, self.TITLE_COLOR)
        display.blit(title, ((display_width * 0.5), (display_height * 0.5)))
        display.blit(instructions, ((display_width * 0.5), (display_height * 0.7)))

    def update(self):
        pass

    def handle_events(self):
        # SUG: Think about changing this part to have events be passed in as an argument and not use pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                self.state_manager.change_state(Game_State)

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
        self.all_sprites_list.add(self.player)

        self.score = 0
        self.lives = 3
        self.bullets_fired = 0
        self.bullets_hit = 0

        self.enemy_spawn_countdown = 0
        self.shotgun_cooldown = 600
        self.spread = -20

    def render(self, display, display_width, display_height):
        self.all_sprites_list.draw(display)
        self.shotgun_display(display, display_width, display_height)

    # display_height is added here for enemy_bullet_collision.
    def update(self, display_width, display_height):
        self.enemy_spawn_countdown += random.randrange(1, 5)
        
        if self.enemy_spawn_countdown >= 30:
            self.spawn_enemy()

        self.enemy_fire(display_width)
        self.bullet_collision()
        self.enemy_bullet_collision(display_height)

        if self.shotgun_cooldown < 600:
            self.shotgun_cooldown += 1

        self.all_sprites_list.update()
        
    def handle_events(self):
        self.pressed_buttons = pygame.key.get_pressed()

        # SUG: Think about changing this part to have events be passed in as an argument and not use pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.fire_bullets()
        
            if self.pressed_buttons[pygame.K_SPACE]:
                if self.shotgun_cooldown == 600:
                    for create_bullets in range (20):
                        self.fire_shotgun()

                    self.shotgun_cooldown = 0
                    self.spread = -20

        if self.lives == 0:
            print("Enemies killed:", self.score)
            # Doing this to get a round percentage for the acuracy.
            print(str(int((self.bullets_hit/self.bullets_fired) * 100)) + "% Accuracy")
            pygame.quit()
            quit()
            # Make some way for this to change to gameover screen. For now, I will just have it end game.

    def shotgun_display(self, display, display_width, display_height):
        pygame.draw.rect(display, BLUE, [(display_width * 0.75), (display_height * 0.9), (self.shotgun_cooldown / 4), 15])
    
    def spawn_enemy(self):
        self.enemy = Enemy()
        self.enemy_list.add(self.enemy)
        self.all_sprites_list.add(self.enemy)

        self.enemy_spawn_countdown = 0

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

    def fire_shotgun(self):
        self.shotgun_bullet = Shotgun_Bullet(self.player.rect.x, self.player.rect.y, self.spread)
        self.all_sprites_list.add(self.shotgun_bullet)
        self.bullet_list.add(self.shotgun_bullet)
        self.spread += 2

    def sprite_oob_check(self, current_x_position, display_width):
        if current_x_position < 0 or current_x_position > DISPLAY_WIDTH:
            return True
        else:
            return False

    def enemy_fire(self, display_width):
        for enemy in self.enemy_list:
            if enemy.check_retreat():
                enemy.fire(self.player.rect.x, self.all_sprites_list, self.enemy_bullet_list)

            if self.sprite_oob_check(enemy.rect.x, display_width):
                enemy.side_speed *= -1
            
            if enemy.rect.y < 0:
                enemy.kill()

            if pygame.sprite.spritecollide(self.player, self.enemy_list, True):
                self.lives -= 1

    def bullet_collision(self):
        for bullet in self.bullet_list:
            self.hit_list = pygame.sprite.spritecollide(bullet, self.enemy_list, True)

            for enemies in self.hit_list:
                bullet.kill()
                self.score += 1
                self.bullets_hit += 1

            if bullet.rect.y < 0:
                bullet.kill()

    def enemy_bullet_collision(self, display_height):            
        for enemy_bullet in self.enemy_bullet_list:
            if enemy_bullet.rect.y > DISPLAY_HEIGHT:
                enemy_bullet.kill()

            if pygame.sprite.spritecollide(self.player, self.enemy_bullet_list, True):
                self.lives -= 1

class State_Manager():
    def __init__():
        self.change_state(Main_Menu())

    def change_state(self, state):
        self.state = state
        self.state.manager = self