# -*- coding: utf-8 -*-
import pygame
from code.const import (
    ASSET_FOLDER, OBS_PTERODATILO, OBS_ESTEGOSSAURO, OBS_PEDRA, OBS_CARNE,
    SIZE_PTERODATILO, SIZE_ESTEGOSSAURO, SIZE_PEDRA, SIZE_CARNE
)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, window, extra):
        super().__init__()
        self.window = window
        self.type = extra.get("tipo") if extra else None
        self.image_path = extra.get("img") if extra else None

        # Define as dimensões com base nas constantes de tamanho do obstáculo
        tamanho = (100, 100)
        if self.type == OBS_PTERODATILO:
            tamanho = SIZE_PTERODATILO
        elif self.type == OBS_ESTEGOSSAURO:
            tamanho = SIZE_ESTEGOSSAURO
        elif self.type == OBS_PEDRA:
            tamanho = SIZE_PEDRA
        elif self.type == OBS_CARNE:
            tamanho = SIZE_CARNE

        try:
            # Carrega a sprite mantendo o canal alpha para transparências de fundo
            img_original = pygame.image.load(f"{ASSET_FOLDER}{self.image_path}").convert_alpha()
            self.image = pygame.transform.scale(img_original, tamanho)
        except pygame.error:
            # Caso o arquivo de imagem falhe, cria um bloco vermelho como fallback de segurança
            self.image = pygame.Surface(tamanho)
            self.image.fill((255, 0, 0))

        # Cria a caixa de colisão baseada nas dimensões finais da sprite carregada
        self.rect = self.image.get_rect()

    def update(self, speed):
        # Desloca o obstáculo para a esquerda acompanhando o movimento do cenário
        self.rect.x -= speed

    def draw(self):
        self.window.blit(self.image, self.rect)