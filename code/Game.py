import pygame
pygame.init()
import code.Level
import code.Menu

class Game:
    def init(self):
        self.menu = code.Menu.Menu()
        self.level = code.Level.Level()
        self.state = "menu"
        self.clock = pygame.time.Clock()

        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                else:
                    if self.state == "menu":
                        action = self.menu.handle_event(evento)
                        if action == "start":
                            self.state = "level"
                    elif self.state == "level":
                        self.level.handle_event(evento)

            dt = self.clock.tick(60) / 1000

            if self.state == "menu":
                self.menu.openMenu()
            elif self.state == "level":
                self.level.update(dt)
                self.level.draw(pygame.display.get_surface())

            pygame.display.flip()

        pygame.quit()


