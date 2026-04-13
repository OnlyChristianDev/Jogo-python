import pygame
pygame.init()
import code.Menu

class Game:
    def init(self):
        self.menu = code.Menu.Menu()

        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                else:
                    self.menu.handle_event(evento)

            self.menu.openMenu()
            pygame.display.flip()

        pygame.quit()


