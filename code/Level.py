import pygame
from pathlib import Path
import code.consts.Window
from code.Player import Player

window = code.consts.Window

class Level:
    def __init__(self):
        self.background_color = (20, 24, 82)
        self.ground_color = (48, 110, 46)
        self.ground_rect = pygame.Rect(0, window.HEIGHT - 60, window.WIDTH, 60)
        self.player = Player()

    def handle_event(self, event):
        pass

    def update(self, dt):
        self.player.handle_input()
        self.player.update(dt, self.ground_rect)

    def draw(self, screen):
        screen.fill(self.background_color)
        pygame.draw.rect(screen, self.ground_color, self.ground_rect)
        self.player.draw(screen)
