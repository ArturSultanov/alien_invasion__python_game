import sys
import pygame
from settings import Settings
from ship import Ship
from game_functions import *


def run_game():
    # Initializes  pygame, settings and creates a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Ship creation
    ship = Ship(ai_settings, screen)

    # Starting the main game cycle.
    while True:
        # Tracking keyboard and mouse events.
        check_events(ship)
        ship.update_moving()                        # ship position check
        update_screen(ai_settings, screen, ship)    # screen refresh


run_game()
