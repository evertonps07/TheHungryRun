# -*- coding: utf-8 -*-
import pygame
from code.entity import Entity
from code.const import WIN_WIDTH, WIN_HEIGHT, ASSET_BG_LAYER1, ASSET_BG_LAYER2

class Background(Entity):
    def __init__(self, window):
        super().__init__()
        self.window = window

        # Carrega e redimensiona a camada inicial do deserto
        self.layer1 = pygame.image.load(ASSET_BG_LAYER1).convert()
        self.layer1 = pygame.transform.scale(self.layer1, (WIN_WIDTH, WIN_HEIGHT))

        # Carrega e deixa pronta a segunda camada para a transição
        self.layer2 = pygame.image.load(ASSET_BG_LAYER2).convert()
        self.layer2 = pygame.transform.scale(self.layer2, (WIN_WIDTH, WIN_HEIGHT))

        # Define a camada atual que será renderizada e a posição X inicial
        self.current_layer = self.layer1
        self.x = 0

    def alterar_cenario(self):
        # Altera o fundo atual para a segunda camada (quando a carne estiver perto)
        self.current_layer = self.layer2

    def draw(self):
        # Desenha duas imagens lado a lado para criar o efeito de continuidade
        self.window.blit(self.current_layer, (self.x, 0))
        self.window.blit(self.current_layer, (self.x + WIN_WIDTH, 0))

    def update(self, speed):
        # Move o cenário para a esquerda com base na velocidade do jogo
        self.x -= speed

        # Se a primeira imagem saiu totalmente da tela, reset na posição criando o loop infinito
        if self.x <= -WIN_WIDTH:
            self.x = 0