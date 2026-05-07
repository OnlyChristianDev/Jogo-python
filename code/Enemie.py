import pygame
import random
import code.consts.Window as window

class Enemie:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, window.WIDTH - 50), random.randint(0, int(window.HEIGHT * 0.65) - 30), 50, 30)
        self.speed = 100
        self.direction = 1 
        self.spawn_timer = 0
        self.spawn_interval = random.uniform(1, 3) 
        self.squares = [] 

    def update(self, dt, ground_rect):

        self.rect.x += self.speed * dt * self.direction
        if self.rect.right > window.WIDTH or self.rect.left < 0:
            self.direction *= -1


        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0

            square = pygame.Rect(self.rect.centerx - 10, self.rect.centery, 20, 20)
            self.squares.append(square)


        for square in self.squares[:]:
            square.y += 200 * dt 
            if square.colliderect(ground_rect):
                self.squares.remove(square)
            elif square.top > window.HEIGHT:
                self.squares.remove(square)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect) 
        for square in self.squares:
            pygame.draw.rect(screen, (0, 255, 0), square)  