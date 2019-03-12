# Fox 4
# Made by Sean Shin. Project started on 29/1/2019.

import pygame, time, random
from game_states import *
from game_classes import *

# Here begins the code for the main loop.
pygame.init()

FPS = 60
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
DISPLAY = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])

clock = pygame.time.Clock()
def main_loop():
    state = Game_State()
    while True:

        state.handle_events()
        state.update(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        DISPLAY.fill(BLACK)
        state.render(DISPLAY, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        pygame.display.update()

        clock.tick(FPS)

main_loop()