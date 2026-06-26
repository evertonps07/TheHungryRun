import pygame
# Importação cirúrgica de absolutamente todas as configurações
from code.const import (
    WIN_WIDTH, WIN_HEIGHT, ASSET_MENU_BG, ASSET_MENU_BGM,
    C_BLACK, C_BOX_NORMAL, C_BOX_HOVER, C_BORDER,
    MENU_OPTION, MENU_BOX_WIDTH, MENU_BOX_HEIGHT,
    MENU_Y_START, MENU_Y_SPACING, MUSIC_VOLUME,
    FONT_NAME, FONT_SIZE_NORMAL, FONT_SIZE_SELECTED,
    MENU_BOX_RADIUS, MENU_BORDER_WIDTH, MOUSE_LEFT_BUTTON,
    RETURN_START, RETURN_SCORE
)

class Menu:
    # Responsável por renderizar o menu principal e gerenciar a navegação do jogador.
    def __init__(self, window):
        self.window = window

        # Carrega e ajusta a imagem de fundo do menu usando as constantes
        self.surf = pygame.image.load(ASSET_MENU_BG)
        self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect(left=0, top=0)

        # Inicializa fontes parametrizadas pelo const.py
        pygame.font.init()
        self.font_normal = pygame.font.SysFont(FONT_NAME, FONT_SIZE_NORMAL, bold=True)
        self.font_selected = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SELECTED, bold=True)

        self.options = MENU_OPTION
        self.selected_index = 0

        # Configurações de áudio do menu usando constantes
        pygame.mixer.init()
        pygame.mixer.music.load(ASSET_MENU_BGM)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)

    def run(self):
        # Loop principal do menu para processamento de entrada e renderização.
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            mouse_pos = pygame.mouse.get_pos()

            # Desenha as opções do menu calculando dinamicamente
            for index, option in enumerate(self.options):
                pos_y = MENU_Y_START + (index * MENU_Y_SPACING)
                box_rect = pygame.Rect(0, 0, MENU_BOX_WIDTH, MENU_BOX_HEIGHT)
                box_rect.center = (WIN_WIDTH // 2, pos_y)

                # Verifica interatividade (mouse ou teclado)
                if box_rect.collidepoint(mouse_pos):
                    self.selected_index = index
                    is_active = True
                elif self.selected_index == index:
                    is_active = True
                else:
                    is_active = False

                # Define o estilo visual com base no estado de seleção
                if is_active:
                    current_box_color = C_BOX_HOVER
                    text_surf = self.font_selected.render(option, True, C_BLACK)
                else:
                    current_box_color = C_BOX_NORMAL
                    text_surf = self.font_normal.render(option, True, C_BLACK)

                # Renderiza caixa, borda e texto usando os parâmetros do const.py
                pygame.draw.rect(self.window, current_box_color, box_rect, border_radius=MENU_BOX_RADIUS)
                pygame.draw.rect(self.window, C_BORDER, box_rect, width=MENU_BORDER_WIDTH, border_radius=MENU_BOX_RADIUS)
                text_rect = text_surf.get_rect(center=box_rect.center)
                self.window.blit(source=text_surf, dest=text_rect)

            pygame.display.flip()

            # Processamento de eventos de entrada
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()

                # Navegação via teclado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected_index] == "NEW GAME":
                            pygame.mixer.music.stop()
                            return RETURN_START
                        elif self.options[self.selected_index] == "SCORE":
                            pygame.mixer.music.stop()
                            return RETURN_SCORE
                        elif self.options[self.selected_index] == "EXIT":
                            pygame.mixer.music.stop()
                            pygame.quit()
                            quit()

                # Seleção via clique do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == MOUSE_LEFT_BUTTON:  # Substituído o número mágico 1
                        for index, option in enumerate(self.options):
                            pos_y = MENU_Y_START + (index * MENU_Y_SPACING)
                            click_rect = pygame.Rect(0, 0, MENU_BOX_WIDTH, MENU_BOX_HEIGHT)
                            click_rect.center = (WIN_WIDTH // 2, pos_y)

                            if click_rect.collidepoint(mouse_pos):
                                if option == "NEW GAME":
                                    pygame.mixer.music.stop()
                                    return RETURN_START
                                elif option == "SCORE":
                                    pygame.mixer.music.stop()
                                    return RETURN_SCORE
                                elif option == "EXIT":
                                    pygame.mixer.music.stop()
                                    pygame.quit()
                                    quit()