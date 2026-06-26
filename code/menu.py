import pygame
import sys
from code.const import (
    WIN_WIDTH, WIN_HEIGHT, ASSET_MENU_BG, ASSET_MENU_BGM,
    ASSET_HELP_BG, ASSET_HELP_BGM,
    C_BLACK, C_BOX_NORMAL, C_BOX_HOVER, C_BORDER,
    MENU_BOX_HEIGHT, MUSIC_VOLUME, FONT_NAME,
    FONT_SIZE_NORMAL, FONT_SIZE_SELECTED,
    MENU_BOX_RADIUS, MENU_BORDER_WIDTH, MOUSE_LEFT_BUTTON,
    RETURN_START, RETURN_SCORE, RETURN_HELP
)


class Menu:
    def __init__(self, window):
        self.window = window

        # Imagem de fundo do menu principal
        self.surf = pygame.image.load(ASSET_MENU_BG)
        self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect(left=0, top=0)

        # Fontes do sistema
        pygame.font.init()
        self.font_normal = pygame.font.SysFont(FONT_NAME, FONT_SIZE_NORMAL, bold=True)
        self.font_selected = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SELECTED, bold=True)
        self.font_instructions = pygame.font.SysFont(FONT_NAME, 20, bold=True)

        # Opcoes dispostas na grade 2x2
        self.options = ["NEW GAME", "SCORE", "HELP", "EXIT"]
        self.selected_index = 0

        # Audio do menu principal
        pygame.mixer.init()
        pygame.mixer.music.load(ASSET_MENU_BGM)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)

    def get_button_rects(self):
        # Grade 2x2 ajustada para a area visivel da tela
        rects = {}
        box_width = 240
        box_height = MENU_BOX_HEIGHT
        center_x = WIN_WIDTH // 2

        row1_y = 410  # Linha de cima (NEW GAME e SCORE)
        row2_y = 480  # Linha de baixo (HELP e EXIT)

        col_left_x = center_x - (box_width // 2) - 15
        col_right_x = center_x + (box_width // 2) + 15

        rects["NEW GAME"] = pygame.Rect(col_left_x - box_width // 2, row1_y - box_height // 2, box_width, box_height)
        rects["SCORE"] = pygame.Rect(col_right_x - box_width // 2, row1_y - box_height // 2, box_width, box_height)
        rects["HELP"] = pygame.Rect(col_left_x - box_width // 2, row2_y - box_height // 2, box_width, box_height)
        rects["EXIT"] = pygame.Rect(col_right_x - box_width // 2, row2_y - box_height // 2, box_width, box_height)

        return rects

    def show_how_to_play(self):
        # Carrega assets especificos do HELP
        help_surf = pygame.image.load(ASSET_HELP_BG)
        help_surf = pygame.transform.scale(help_surf, (WIN_WIDTH, WIN_HEIGHT))
        help_rect = help_surf.get_rect(left=0, top=0)

        pygame.mixer.music.load(ASSET_HELP_BGM)
        pygame.mixer.music.play(-1)

        # Cores escuras para dar contraste com o deserto claro
        COLOR_TITLE = (40, 40, 40)  # Cinza quase preto
        COLOR_KEY = (0, 51, 102)  # Azul escuro forte
        COLOR_TEXT = (20, 20, 20)  # Preto fosco
        COLOR_OBJ_LABEL = (139, 0, 0)  # Vermelho escuro para OBJETIVO:
        COLOR_OBJ_TEXT = (180, 0, 0)  # Vermelho para o texto do objetivo
        COLOR_FOOTER = (100, 100, 100)  # Cinza escuro para o rodape

        showing = True
        while showing:
            self.window.blit(source=help_surf, dest=help_rect)

            # Titulo principal escurecido
            title_surf = self.font_selected.render("HELP & INSTRUCTIONS", True, COLOR_TITLE)
            title_rect = title_surf.get_rect(center=(WIN_WIDTH // 2, 50))
            self.window.blit(title_surf, title_rect)

            # Lista de instrucoes e comandos exigidos pelo manual do trabalho
            instructions = [
                ("ESPAÇO", "Faz o dinossauro Pular os obstáculos."),
                ("SHIFT", "Faz o dinossauro acelerar e pular mais alto."),
                ("ENTER", "Inicia o jogo ou confirma ações."),
                ("SETAS", "Escolhe as opções do menu."),
                ("P", "Pausa o jogo a qualquer momento."),
                ("", ""),
                ("OBJETIVO:", "Sobreviva o maior TEMPO vivo para pegar a carne!"),
                ("", ""),
                ("ATIVIDADE PRÁTICA UNINTER:","" ),
                ("Everton Palhares - RU:524565", "")
            ]

            y_pos = 180
            for key, action in instructions:
                if key == "" and action == "":
                    y_pos += 15
                    continue

                # Define cores baseadas no tipo de texto para melhorar leitura
                if key == "OBJETIVO:":
                    key_color = COLOR_OBJ_LABEL
                    action_color = COLOR_OBJ_TEXT
                else:
                    key_color = COLOR_KEY
                    action_color = COLOR_TEXT

                k_surf = self.font_instructions.render(key, True, key_color)
                a_surf = self.font_instructions.render(action, True, action_color)

                self.window.blit(k_surf, (WIN_WIDTH // 2 - 240, y_pos))
                self.window.blit(a_surf, (WIN_WIDTH // 2 - 120, y_pos))
                y_pos += 35

            # Rodape informativo escurecido
            footer_surf = self.font_instructions.render("Pressione ESPAÇO ou ENTER para voltar", True, COLOR_FOOTER)
            footer_rect = footer_surf.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 60))
            self.window.blit(footer_surf, footer_rect)

            pygame.display.flip()

            # Captura eventos para retornar ao menu principal
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE]:
                        showing = False

        # Restaura a trilha sonora do menu principal ao retornar
        pygame.mixer.music.load(ASSET_MENU_BGM)
        pygame.mixer.music.play(-1)

    def run(self):
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            mouse_pos = pygame.mouse.get_pos()
            button_rects = self.get_button_rects()

            # Mapeamento de movimentacao da grade via setas do teclado
            nav_map = {
                0: (2, 2, 1, 1),  # NEW GAME
                1: (3, 3, 0, 0),  # SCORE
                2: (0, 0, 3, 3),  # HELP
                3: (1, 1, 2, 2)  # EXIT
            }

            for index, option in enumerate(self.options):
                box_rect = button_rects[option]

                if box_rect.collidepoint(mouse_pos):
                    self.selected_index = index
                    is_active = True
                elif self.selected_index == index:
                    is_active = True
                else:
                    is_active = False

                if is_active:
                    current_box_color = C_BOX_HOVER
                    text_surf = self.font_selected.render(option, True, C_BLACK)
                else:
                    current_box_color = C_BOX_NORMAL
                    text_surf = self.font_normal.render(option, True, C_BLACK)

                pygame.draw.rect(self.window, current_box_color, box_rect, border_radius=MENU_BOX_RADIUS)
                pygame.draw.rect(self.window, C_BORDER, box_rect, width=MENU_BORDER_WIDTH,
                                 border_radius=MENU_BOX_RADIUS)
                text_rect = text_surf.get_rect(center=box_rect.center)
                self.window.blit(source=text_surf, dest=text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    up_nav, down_nav, left_nav, right_nav = nav_map[self.selected_index]

                    if event.key == pygame.K_DOWN:
                        self.selected_index = down_nav
                    elif event.key == pygame.K_UP:
                        self.selected_index = up_nav
                    elif event.key == pygame.K_LEFT:
                        self.selected_index = left_nav
                    elif event.key == pygame.K_RIGHT:
                        self.selected_index = right_nav
                    elif event.key == pygame.K_RETURN:
                        chosen = self.options[self.selected_index]
                        if chosen == "NEW GAME":
                            pygame.mixer.music.stop()
                            return RETURN_START
                        elif chosen == "SCORE":
                            pygame.mixer.music.stop()
                            return RETURN_SCORE
                        elif chosen == "HELP":
                            self.show_how_to_play()
                        elif chosen == "EXIT":
                            pygame.mixer.music.stop()
                            pygame.quit()
                            sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == MOUSE_LEFT_BUTTON:
                        for option, box_rect in button_rects.items():
                            if box_rect.collidepoint(mouse_pos):
                                if option == "NEW GAME":
                                    pygame.mixer.music.stop()
                                    return RETURN_START
                                elif option == "SCORE":
                                    pygame.mixer.music.stop()
                                    return RETURN_SCORE
                                elif option == "HELP":
                                    self.show_how_to_play()
                                elif option == "EXIT":
                                    pygame.mixer.music.stop()
                                    pygame.quit()
                                    sys.exit()