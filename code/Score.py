import pygame

class Score:
    def __init__(self):
        self.value = 0
        self.won = False
        self.font = pygame.font.SysFont("monoespace", 30, bold=True)

    def update(self, dt):
        if self.won:
            return

        self.value += dt * 10
        if self.value >= 1000:
            self.value = 1000
            self.won = True

    def draw(self, screen):
        text = self.font.render(f"Score: {int(self.value)}/1000", True, (255, 255, 255))
        screen.blit(text, (10, 40)) 