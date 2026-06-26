import pygame
from code.entity import Entity
# Importa as configurações físicas e visuais do jogador
from code.const import (
    ASSET_PLAYER, SIZE_PLAYER, PLAYER_INITIAL_LIVES,
    PLAYER_GRAVITY, PLAYER_JUMP_SPEED, PLAYER_START_X, PLAYER_FLOOR_Y
)

class Player(Entity):
    # Representa o personagem controlado pelo jogador e sua física de movimento.
    def __init__(self, window):
        super().__init__()
        self.window = window

        # Carrega a imagem e redimensiona usando as constantes do projeto
        self.image_original = pygame.image.load(ASSET_PLAYER).convert_alpha()
        self.image = pygame.transform.scale(self.image_original, SIZE_PLAYER)
        self.rect = self.image.get_rect()

        # Posicionamento inicial estruturado por constantes
        self.rect.x = PLAYER_START_X
        self.rect.y = PLAYER_FLOOR_Y

        # Estados de controle
        self.is_jumping = False
        self.is_accelerating = False
        self.lives = PLAYER_INITIAL_LIVES

        # Parâmetros físicos do pulo totalmente customizáveis pelo const.py
        self.velocity_y = 0
        self.gravity = PLAYER_GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED

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

            # Colisão com o solo: utiliza a constante de altura do chão para resetar o estado
            if self.rect.y >= PLAYER_FLOOR_Y:
                self.rect.y = PLAYER_FLOOR_Y
                self.is_jumping = False
                self.velocity_y = 0

    def draw(self):
        # Renderiza a imagem do jogador na janela.
        self.window.blit(self.image, self.rect)