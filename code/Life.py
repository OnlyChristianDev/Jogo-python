import pygame
from pathlib import Path
import code.consts.Window as window

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
HEART_IMAGE = ASSETS_DIR / "Heart.png"
GAME_OVER_IMAGE = ASSETS_DIR / "gameOver.png"

class Life:
    def __init__(self, lives=3):
        self.lives = lives
        heart_img = pygame.image.load(str(HEART_IMAGE)).convert_alpha()
        self.heart = pygame.transform.scale(heart_img, (20, 20))
        self.spacing = self.heart.get_width() + 5
        self.font = pygame.font.SysFont("monoespace", 24, bold=True)

    def remove_life(self):
        if self.lives > 0:
            self.lives -= 1

    def draw(self, screen):
        for i in range(self.lives):
            x = 10 + i * self.spacing
            screen.blit(self.heart, (x, 10))
        if self.lives <= 0:
            pygame.mixer.music.stop()
            game_over_img = pygame.image.load(str(GAME_OVER_IMAGE)).convert_alpha()
            game_over_img = pygame.transform.scale(game_over_img, (window.WIDTH, window.HEIGHT))
            screen.blit(game_over_img, (0, 0))
            text = self.font.render("Aperte Enter para voltar ao menu", True, (255, 255, 255))
            text_y = window.HEIGHT - 50
            screen.blit(text, (window.WIDTH // 2 - text.get_width() // 2, text_y))
