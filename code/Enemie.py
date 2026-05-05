import pygame
import code.consts.Window as window

class Enemie:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 50, 30)
        self.speed = 100
        self.direction = 1 
        self.spawn_timer = 0
        self.spawn_interval = 5  
        self.squares = [] 

    def update(self, dt):

        self.rect.x += self.speed * dt * self.direction
        if self.rect.right > window.WIDTH or self.rect.left < 0:
            self.direction *= -1


        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0

            square = pygame.Rect(self.rect.centerx - 10, self.rect.centery, 20, 20)
            self.squares.append(square)


        for square in self.squares:
            square.y += 200 * dt 


        self.squares = [s for s in self.squares if s.top < window.HEIGHT]

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect) 
        for square in self.squares:
            pygame.draw.rect(screen, (0, 255, 0), square)  