import pygame
from code.entity import Entity

class Background(Entity):
    def __init__(self, window):
        super().__init__()
        self.window = window

        # Carrega e redimensiona as camadas do cenário
        self.layer1 = pygame.image.load("asset/deserto01.jpeg").convert()
        self.layer1 = pygame.transform.scale(self.layer1, (800, 600))

        self.layer2 = pygame.image.load("asset/deserto02.jpeg").convert()
        self.layer2 = pygame.transform.scale(self.layer2, (800, 600))

        # Camada de fundo inicial exibida
        self.current_layer = self.layer1
        self.x = 0

    def alterar_cenario(self):
        # Alterna para a segunda camada do cenário.
        self.current_layer = self.layer2

    def draw(self):
        # Desenha a camada ativa duas vezes para criar o efeito de rolagem contínua
        self.window.blit(self.current_layer, (self.x, 0))
        self.window.blit(self.current_layer, (self.x + 800, 0))

    def update(self, speed):
        # Desloca a posição horizontal e reseta ao atingir o limite da tela
        self.x -= speed
        if self.x <= -800:
            self.x = 0