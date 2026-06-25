import pygame

class Menu:
    # Responsável por renderizar o menu principal e gerenciar a navegação do jogador.
    def __init__(self, window):
        self.window = window

        # Carrega e ajusta a imagem de fundo do menu
        self.surf = pygame.image.load("asset/imagemmenu.jpeg")
        self.surf = pygame.transform.scale(self.surf, (800, 600))
        self.rect = self.surf.get_rect(left=0, top=0)

        # Inicializa fontes para estados normal e selecionado
        pygame.font.init()
        self.font_normal = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_selected = pygame.font.SysFont("Arial", 42, bold=True)

        self.options = ["NEW GAME", "SCORE", "EXIT"]
        self.selected_index = 0

        # Paleta de cores da interface
        self.COLOR_TEXT = (0, 0, 0)
        self.COLOR_BOX_NORMAL = (210, 180, 140)
        self.COLOR_BOX_HOVER = (245, 222, 179)
        self.COLOR_BORDER = (100, 70, 40)

        # Configurações de áudio do menu
        pygame.mixer.init()
        pygame.mixer.music.load("asset/MenuDin.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def run(self):
        # Loop principal do menu para processamento de entrada e renderização.
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            mouse_pos = pygame.mouse.get_pos()

            # Desenha as opções do menu
            for index, option in enumerate(self.options):
                pos_y = 360 + (index * 75)
                box_rect = pygame.Rect(0, 0, 260, 55)
                box_rect.center = (400, pos_y)

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
                    current_box_color = self.COLOR_BOX_HOVER
                    text_surf = self.font_selected.render(option, True, self.COLOR_TEXT)
                else:
                    current_box_color = self.COLOR_BOX_NORMAL
                    text_surf = self.font_normal.render(option, True, self.COLOR_TEXT)

                # Renderiza caixa, borda e texto
                pygame.draw.rect(self.window, current_box_color, box_rect, border_radius=10)
                pygame.draw.rect(self.window, self.COLOR_BORDER, box_rect, width=3, border_radius=10)
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
                            return "Iniciar"
                        elif self.options[self.selected_index] == "SCORE":
                            pygame.mixer.music.stop()
                            return "Score"
                        elif self.options[self.selected_index] == "EXIT":
                            pygame.mixer.music.stop()
                            pygame.quit()
                            quit()

                # Seleção via clique do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for index, option in enumerate(self.options):
                            pos_y = 360 + (index * 75)
                            click_rect = pygame.Rect(0, 0, 260, 55)
                            click_rect.center = (400, pos_y)

                            # Metodo auxiliar para centralizar a lógica de saída do menu.
                            if click_rect.collidepoint(mouse_pos):
                                if option == "NEW GAME":
                                    pygame.mixer.music.stop()
                                    return "Iniciar"
                                elif option == "SCORE":
                                    pygame.mixer.music.stop()
                                    return "Score"
                                elif option == "EXIT":
                                    pygame.mixer.music.stop()
                                    pygame.quit()
                                    quit()