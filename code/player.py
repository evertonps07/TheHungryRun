import pygame
from code.entity import Entity

class Player(Entity):
    # Representa o personagem controlado pelo jogador e sua física de movimento.
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.image_original = pygame.image.load("asset/TRex1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (130, 150))
        self.rect = self.image.get_rect()

        # Posicionamento inicial na tela
        self.rect.x = 100
        self.rect.y = 400

        # Estados de controle
        self.is_jumping = False
        self.is_accelerating = False
        self.lives = 3

        # Parâmetros físicos do pulo
        self.velocity_y = 0
        self.gravity = 0.9
        self.jump_speed = -22

    def handle_event(self, event):
        # Processa entradas de teclado para pulo e aceleração.
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not self.is_jumping:
                self.is_jumping = True
                self.velocity_y = self.jump_speed

            if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                self.is_accelerating = True

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                self.is_accelerating = False

    def update(self):
        # Atualiza a posição vertical do jogador aplicando a gravidade.
        if self.is_jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity

            # Colisão com o solo: reseta o estado de pulo ao tocar a base
            if self.rect.y >= 400:
                self.rect.y = 400
                self.is_jumping = False
                self.velocity_y = 0

    def draw(self):
        # Renderiza a imagem do jogador na janela.
        self.window.blit(self.image, self.rect)