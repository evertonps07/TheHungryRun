import pygame
from code.entity import Entity

class Obstaculo(Entity):
    # Representa um obstáculo ou item coletável no jogo.
    def __init__(self, window, info):
        super().__init__()
        self.window = window
        self.tipo = info["tipo"]

        # Carrega e processa a imagem do obstáculo
        self.image_original = pygame.image.load(f"asset/{info['img']}").convert_alpha()

        # Define as dimensões conforme o tipo de objeto
        if self.tipo == "pterodatilo":
            tamanho = (180, 130)
        elif self.tipo == "carne":
            tamanho = (100, 100)
        elif self.tipo == "estegossauro":
            tamanho = (200, 140)
        else:  # Para as pedras
            tamanho = (120, 120)

        self.image = pygame.transform.scale(self.image_original, tamanho)
        self.rect = self.image.get_rect()

        # Posição inicial fora da área visível (à direita)
        self.rect.x = 800
        self.rect.y = 400

    def update(self, speed):
        # Atualiza a posição horizontal movendo o objeto para a esquerda.
        self.rect.x -= speed

    def draw(self):
        # Renderiza o obstáculo na janela.
        self.window.blit(self.image, self.rect)