import pygame

class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.SysFont("monoespace", 30, bold=True)

    def update(self, dt):
        self.value += dt * 10 

    def draw(self, screen):
        text = self.font.render(f"Score: {int(self.value)}", True, (255, 255, 255))
        screen.blit(text, (30, 80)) 