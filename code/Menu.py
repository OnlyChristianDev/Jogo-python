import pygame
from pathlib import Path
import code.consts.Window

pygame.init()
pygame.mixer.init()
window = code.consts.Window

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
MENU_MUSIC = ASSETS_DIR / "menuMusic.wav"

class Menu:
    def __init__(self):
        pygame.display.set_mode((window.WIDTH, window.HEIGHT))
        pygame.display.set_caption("Poopocalypse Frog")

        self.fonte = pygame.font.SysFont("monoespace", 50, bold=True)
        self.opcoes = ["Start", "Exit"]
        self.opcao_selecionada = 0
        self.fundo_menu = pygame.image.load(str(ASSETS_DIR / "menu.png"))
        self.fundo_menu = pygame.transform.scale(self.fundo_menu, (window.WIDTH, window.HEIGHT))
        self.option_rects = []
        self.initMusic()

    def openMenu(self):
        tela = pygame.display.get_surface()
        tela.blit(self.fundo_menu, (0, 0))
        self.initOptions()
    
    def initMusic(self):
        pygame.mixer.music.load(str(MENU_MUSIC))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def initOptions(self):
        tela = pygame.display.get_surface()

        self.option_rects = []
        
        total_height = len(self.opcoes) * 40
        start_y = (window.HEIGHT - total_height) // 2

        for i, opcao in enumerate(self.opcoes):
            cor = (255, 255, 255)

            if i == self.opcao_selecionada:
                cor = (252, 186, 3)

            texto = self.fonte.render(opcao, True, cor)

            x = window.WIDTH // 2 - texto.get_width() // 2
            y = start_y + i * 40

            rect = texto.get_rect(topleft=(x, y))
            self.option_rects.append((i, rect))
            tela.blit(texto, rect)

    def executeOption(self):
        opcao = self.opcoes[self.opcao_selecionada]

        if opcao == "Start":
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            level_music = ASSETS_DIR / "levelMusic.wav"
            pygame.mixer.music.load(str(level_music))
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

            return "start"

        elif opcao == "Exit":
            pygame.quit()
            exit()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for i, rect in self.option_rects:
                if rect.collidepoint(pos):
                    self.opcao_selecionada = i
                    return self.executeOption()
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            cursor_over_option = False
            for i, rect in self.option_rects:
                if rect.collidepoint(pos):
                    self.opcao_selecionada = i
                    cursor_over_option = True
                    break
            
            if cursor_over_option:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return None
