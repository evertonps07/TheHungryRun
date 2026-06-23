# THE HUNGRY RUN
import pygame

from code.menu import Menu


# !/usr/bin/python
# -*- coding: utf-8 -*-

class Game:
    def __init__(self):
        pygame.init()
        # Inicialização da janela gráfica e definição do título
        pygame.display.set_caption("The Hungry Run")
        self.window = pygame.display.set_mode(size=(800, 600))  # Definição das dimensões da tela

    def run(self):
        # Loop contínuo de execução do jogo
        while True:
            menu = Menu(self.window)
            menu.run()
            pass

            # # Captação e processamento da fila de eventos do sistema operacional
            # for event in pygame.event.get():
            #     # Interrupção do programa caso o botão de fechar a janela seja acionado
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         quit()



