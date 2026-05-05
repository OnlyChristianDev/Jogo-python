import pygame
from pathlib import Path
import code.consts.Window
from code.Player import Player
from code.Enemie import Enemie

window = code.consts.Window
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
GRASS_TILESET = ASSETS_DIR / "tilesetgrass.png"
SKY_IMAGE = ASSETS_DIR / "sky.png"
CLOUD1_IMAGE = ASSETS_DIR / "cloud1.png"
CLOUD2_IMAGE = ASSETS_DIR / "cloud2.png"
HEART_IMAGE = ASSETS_DIR / "Heart.png"
ORIGINAL_TILE_SIZE = 27
GROUND_HEIGHT = 60

class Level:
    def __init__(self):
        self.ground_rect = pygame.Rect(0, window.HEIGHT - GROUND_HEIGHT, window.WIDTH, GROUND_HEIGHT)
        
        sky_img = pygame.image.load(str(SKY_IMAGE)).convert_alpha()
        self.sky = pygame.transform.scale(sky_img, (window.WIDTH, window.HEIGHT - GROUND_HEIGHT))
        
        grass_tile = pygame.image.load(str(GRASS_TILESET)).convert_alpha()
        scaled_tile_size = GROUND_HEIGHT
        self.grass_tile = pygame.transform.scale(grass_tile, (scaled_tile_size, scaled_tile_size))
        
        cloud1_img = pygame.image.load(str(CLOUD1_IMAGE)).convert_alpha()
        cloud2_img = pygame.image.load(str(CLOUD2_IMAGE)).convert_alpha()
        
        heart_img = pygame.image.load(str(HEART_IMAGE)).convert_alpha()
        self.heart = pygame.transform.scale(heart_img, (100, 100))
        
        self.clouds = [
            {"image": cloud1_img, "x": 200, "y": 420, "speed": 30},
            {"image": cloud2_img, "x": 600, "y": 420, "speed": 20},
            {"image": cloud1_img, "x": 1000, "y": 420, "speed": 25},
        ]
        
        self.player = Player()
        self.enemy = Enemie()

    def handle_event(self, event):
        pass

    def update(self, dt):
        self.player.handle_input()
        self.player.update(dt, self.ground_rect)
        self.enemy.update(dt)
        
        for cloud in self.clouds:
            cloud["x"] -= cloud["speed"] * dt
            if cloud["x"] + cloud["image"].get_width() < 0:
                cloud["x"] = window.WIDTH

    def draw(self, screen):
        screen.blit(self.sky, (0, 0))
        screen.blit(self.heart, (10, 10))
        
        for cloud in self.clouds:
            screen.blit(cloud["image"], (cloud["x"], cloud["y"]))
        
        ground_y = window.HEIGHT - GROUND_HEIGHT
        tile_width = self.grass_tile.get_width()
        x = 0
        while x < window.WIDTH:
            screen.blit(self.grass_tile, (x, ground_y))
            x += tile_width
        self.player.draw(screen)
        self.enemy.draw(screen)
