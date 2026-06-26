# -*- coding: utf-8 -*-
import pygame
from code.menu import Menu
from code.level import Level
from code.score import ScoreManager
from code.const import WIN_WIDTH, WIN_HEIGHT, WIN_TITLE, RETURN_START, RETURN_SCORE


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(WIN_TITLE)
        self.score_manager = ScoreManager()
        # Carrega o menor tempo absoluto registrado para exibir dinamicamente na HUD da fase
        self.recorde = self.score_manager.get_melhor_tempo()

    def run(self):
        running = True
        # Gerencia o estado atual do fluxo de telas do jogo (Máquina de Estados)
        proxima_tela = "Menu"

        while running:
            if proxima_tela == "Menu":
                menu = Menu(self.window)
                escolha = menu.run()

                if escolha == RETURN_START:
                    proxima_tela = "Level"
                elif escolha == RETURN_SCORE:
                    proxima_tela = "Score"
                else:
                    running = False

            elif proxima_tela == "Score":
                self.score_manager.mostrar_tela_scores(self.window)
                proxima_tela = "Menu"

            elif proxima_tela == "Level":
                level = Level(self.window, game_ref=self, recorde=self.recorde)
                # Desempacota as informações retornadas ao encerrar a partida
                resultado, tempo = level.run()

                if resultado == "Vitoria":
                    # Grava o novo tempo no banco SQLite e atualiza o recorde local da HUD
                    self.score_manager.adicionar_score(tempo)
                    self.recorde = self.score_manager.get_melhor_tempo()

                    # Redireciona o jogador ao menu principal imediatamente após vencer
                    proxima_tela = "Menu"

                elif resultado == "Game Over":
                    proxima_tela = "Menu"
            else:
                running = False

        pygame.quit()