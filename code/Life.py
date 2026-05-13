import pygame
from code.consts.Assets import get_asset_file
import code.consts.Window as window

class Life:
    def __init__(self, lives=3):
        self.lives = lives
        heart_img = pygame.image.load(str(get_asset_file("Heart.png"))).convert_alpha()
        self.heart = pygame.transform.scale(heart_img, (20, 20))
        self.spacing = self.heart.get_width() + 5
        self.font = pygame.font.SysFont("monoespace", 24, bold=True)
        
        hurt_sound_path = get_asset_file("hurt.mp3")
        self.hurt_sound = pygame.mixer.Sound(str(hurt_sound_path))
        self.game_over_played = False

    def remove_life(self):
        if self.lives > 0:
            self.hurt_sound.play()
            self.lives -= 1
    def draw(self, screen):
        for i in range(self.lives):
            x = 10 + i * self.spacing
            screen.blit(self.heart, (x, 10))
        if self.lives <= 0:
            if not self.game_over_played:
                pygame.mixer.music.stop()

                game_over_sound = pygame.mixer.Sound(str(get_asset_file("gameOver.mp3")))
                game_over_sound.set_volume(0.5)
                game_over_sound.play()

                self.game_over_played = True

            game_over_img = pygame.image.load(str(get_asset_file("gameOver.png"))).convert_alpha()
            game_over_img = pygame.transform.scale(game_over_img, (window.WIDTH, window.HEIGHT))
            screen.blit(game_over_img, (0, 0))
            text = self.font.render("Aperte Enter para voltar ao menu", True, (255, 255, 255))
            text_y = window.HEIGHT - 50
            screen.blit(text, (window.WIDTH // 2 - text.get_width() // 2, text_y))
