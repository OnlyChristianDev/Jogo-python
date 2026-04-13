import pygame
from pathlib import Path
import code.consts.Window

pygame.init()
window = code.consts.Window

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
MENU_MUSIC = ASSETS_DIR / "menuMusic.wav"

class Menu:
    def __init__(self):
        pygame.display.set_mode((window.WIDTH, window.HEIGTH))
        pygame.display.set_caption("Frog game")

        self.fonte = pygame.font.SysFont("PressStart2P-Regular.ttf", 50)
        self.opcoes = ["Start", "Settings", "Exit"]
        self.opcao_selecionada = 0
        self.fundo_menu = pygame.image.load(str(ASSETS_DIR / "menu.png"))
        self.fundo_menu = pygame.transform.scale(self.fundo_menu, (window.WIDTH, window.HEIGTH))
        self.option_rects = []
        self.initMusic()

    def openMenu(self):
        tela = pygame.display.get_surface()
        tela.blit(self.fundo_menu, (0, 0))
        self.initOptions()
    
    def initMusic(self):
        pygame.mixer.init()
        pygame.mixer.music.load(str(MENU_MUSIC))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def initOptions(self):
        tela = pygame.display.get_surface()

        self.option_rects = []

        for i, opcao in enumerate(self.opcoes):
            cor = (255, 255, 255)

            if i == self.opcao_selecionada:
                cor = (31, 161, 19)

            texto = self.fonte.render(opcao, True, cor)

            x = window.WIDTH // 2 - texto.get_width() // 2
            y = 200 + i * 60

            rect = texto.get_rect(topleft=(x, y))
            self.option_rects.append((i, rect))
            tela.blit(texto, rect)

    def executeOption(self):
        opcao = self.opcoes[self.opcao_selecionada]

        if opcao == "Start":
            print("Iniciar jogo 🚀")

        elif opcao == "Settings":
            print("Abrir configurações ⚙️")

        elif opcao == "Exit":
            pygame.quit()
            exit()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for i, rect in self.option_rects:
                if rect.collidepoint(pos):
                    self.opcao_selecionada = i
                    self.executeOption()
                    break
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            for i, rect in self.option_rects:
                if rect.collidepoint(pos):
                    self.opcao_selecionada = i
                    break
