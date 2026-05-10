import pygame
import random
from pathlib import Path
import code.consts.Window as window

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
POOP_IMAGE = ASSETS_DIR / "poop.png"
BIRD_IMAGE = ASSETS_DIR / "Bird.png"

class Enemie:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, window.WIDTH - 40), random.randint(0, int(window.HEIGHT * 0.65) - 30), 40, 30)
        self.speed = 100
        self.direction = 1 
        self.spawn_timer = 0
        self.spawn_interval = random.uniform(1, 3) 
        self.squares = [] 
        self.poop_image = pygame.image.load(str(POOP_IMAGE)).convert_alpha()
        self.poop_image = pygame.transform.scale(self.poop_image, (18, 18))

        self.poop_sheet = pygame.image.load(str(POOP_IMAGE)).convert_alpha()
        self.poop_frames = []
        for i in range(5):
            frame = self.poop_sheet.subsurface((i * 89, 0, 89, 89))
            scaled_frame = pygame.transform.scale(frame, (18, 18))
            self.poop_frames.append(scaled_frame)
        
        self.poop_animation_frames = {} 

        self.bird_sheet = pygame.image.load(str(BIRD_IMAGE)).convert_alpha()
        self.frames = []
        for i in range(8):
            frame = self.bird_sheet.subsurface((i * 16, 0, 16, 15))
            self.frames.append(frame)
        self.scaled_frames = [pygame.transform.scale(frame, (40, 30)) for frame in self.frames]
        self.flipped_frames = [pygame.transform.flip(frame, True, False) for frame in self.scaled_frames]

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15 

    def update(self, dt, ground_rect, target_x=None):

        if target_x is not None:
            if target_x > self.rect.x:
                self.direction = 1
            elif target_x < self.rect.x:
                self.direction = -1
            else:
                self.direction = 0

        self.rect.x += self.speed * dt * self.direction
        if self.rect.right > window.WIDTH or self.rect.left < 0:
            self.direction *= -1

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0

            square = pygame.Rect(self.rect.centerx - 10, self.rect.centery, 20, 20)
            self.squares.append(square)
            self.poop_animation_frames[id(square)] = {'frame': 0, 'timer': 0}


        for square in self.squares[:]:
            square.y += 200 * dt 
            if square.colliderect(ground_rect):
                self.squares.remove(square)
                if id(square) in self.poop_animation_frames:
                    del self.poop_animation_frames[id(square)]
            elif square.top > window.HEIGHT:
                self.squares.remove(square)
                if id(square) in self.poop_animation_frames:
                    del self.poop_animation_frames[id(square)]
            else:
                poop_id = id(square)
                if poop_id in self.poop_animation_frames:
                    self.poop_animation_frames[poop_id]['timer'] += dt
                    if self.poop_animation_frames[poop_id]['timer'] >= 0.15:
                        self.poop_animation_frames[poop_id]['timer'] = 0
                        self.poop_animation_frames[poop_id]['frame'] = (self.poop_animation_frames[poop_id]['frame'] + 1) % 5

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % 8

    def draw(self, screen):
        if self.direction > 0:
            frame = self.flipped_frames[self.frame_index]
        else:
            frame = self.scaled_frames[self.frame_index]
        screen.blit(frame, self.rect)
        for square in self.squares:
            poop_id = id(square)
            if poop_id in self.poop_animation_frames:
                frame_idx = self.poop_animation_frames[poop_id]['frame']
                screen.blit(self.poop_frames[frame_idx], square)
            else:
                screen.blit(self.poop_frames[0], square)
