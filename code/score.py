# -*- coding: utf-8 -*-
import pygame
import os
import sqlite3
from datetime import datetime
from code.const import (
    WIN_WIDTH, WIN_HEIGHT, FPS, C_BLACK, C_WHITE, C_HUD_TEXT,
    FONT_NAME, DATE_FORMAT, SCORE_ROUND_PRECISION, SHADOW_OFFSET,
    ASSET_SCORE_BG, ASSET_SCORE_BGM, MUSIC_VOLUME, DB_NAME, DEFAULT_PLAYER_NAME
)


def desenhar_texto_destacado(surface, texto, fonte, cor, pos):
    # Desenha o texto duplicado com um pequeno deslocamento (offset) para criar efeito de sombra e leitura estável
    sombra = fonte.render(texto, True, C_BLACK)
    real = fonte.render(texto, True, cor)
    x, y = pos

    offset_x = x - real.get_width() // 2
    offset_y = y - real.get_height() // 2

    surface.blit(sombra, (offset_x + SHADOW_OFFSET, offset_y + SHADOW_OFFSET))
    surface.blit(real, (offset_x, offset_y))


class ScoreManager:
    def __init__(self):
        self.db_path = DB_NAME
        self._inicializar_banco_nativo()

    def _inicializar_banco_nativo(self):
        # Garante de forma nativa e segura que a tabela de scores existe no banco SQLite
        try:
            conexao = sqlite3.connect(self.db_path)
            cursor = conexao.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tabela_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    score REAL NOT NULL,
                    date TEXT NOT NULL
                )
            ''')
            conexao.commit()
            conexao.close()
        except Exception as e:
            print(f"Erro ao verificar/criar banco de dados: {e}")

    def adicionar_score(self, novo_tempo):
        # Grava o tempo final da corrida arredondado com base na precisão definida nas constantes
        try:
            conexao = sqlite3.connect(self.db_path)
            cursor = conexao.cursor()
            data_atual = datetime.now().strftime(DATE_FORMAT)
            tempo_salvar = round(float(novo_tempo), SCORE_ROUND_PRECISION)

            cursor.execute('''
                INSERT INTO tabela_scores (name, score, date)
                VALUES (?, ?, ?)
            ''', (DEFAULT_PLAYER_NAME, tempo_salvar, data_atual))

            conexao.commit()
            conexao.close()
            print(f"Sucesso: Pontuação de {tempo_salvar}s guardada!")
        except Exception as e:
            print(f"Erro ao adicionar score no banco: {e}")

    def get_melhor_tempo(self):
        # Busca o menor valor de tempo registrado para alimentar o recorde dinâmico na HUD da fase
        try:
            conexao = sqlite3.connect(self.db_path)
            cursor = conexao.cursor()
            cursor.execute('SELECT score FROM tabela_scores ORDER BY score ASC LIMIT 1')
            resultado = cursor.fetchone()
            conexao.close()

            if resultado:
                return float(resultado[0])
        except Exception as e:
            print(f"Erro ao buscar melhor tempo: {e}")
        return 0.0

    def mostrar_tela_scores(self, window):
        # Gerencia o loop da tela de ranking carregando e organizando o TOP 5 de tempos mais baixos
        clock = pygame.time.Clock()
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(ASSET_SCORE_BGM)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("Erro ao carregar a trilha sonora da tela de Scores.")

        try:
            surf_bg = pygame.image.load(ASSET_SCORE_BG)
            surf_bg = pygame.transform.scale(surf_bg, (WIN_WIDTH, WIN_HEIGHT))
        except pygame.error:
            surf_bg = None

        font_titulo = pygame.font.SysFont(FONT_NAME, 46, bold=True)
        font_registro = pygame.font.SysFont(FONT_NAME, 24, bold=True)
        font_aviso = pygame.font.SysFont(FONT_NAME, 20, bold=True)

        registros = []
        try:
            conexao = sqlite3.connect(self.db_path)
            cursor = conexao.cursor()
            cursor.execute('SELECT name, score, date FROM tabela_scores ORDER BY score ASC LIMIT 5')
            registros = cursor.fetchall()
            conexao.close()
        except Exception as e:
            print(f"Erro ao buscar TOP 5 do banco: {e}")

        exibindo = True
        while exibindo:
            if surf_bg:
                window.blit(surf_bg, (0, 0))
            else:
                window.fill((40, 35, 35))

            desenhar_texto_destacado(
                window, "TOP 5 - MELHORES TEMPOS", font_titulo, C_HUD_TEXT, (WIN_WIDTH // 2, 70)
            )

            if registros:
                for idx, reg in enumerate(registros):
                    nome = reg[0]
                    tempo = reg[1]
                    data = reg[2]
                    # Formata o alinhamento das colunas de texto para manter a tabela do ranking simétrica
                    texto_linha = f"{idx + 1}º  {nome:<6} --- {tempo:>6}.s --- ({data})"
                    desenhar_texto_destacado(window, texto_linha, font_registro, C_WHITE,
                                             (WIN_WIDTH // 2, 180 + idx * 50))
            else:
                desenhar_texto_destacado(
                    window, "NENHUM RECORDE GRAVADO AINDA", font_registro, C_WHITE, (WIN_WIDTH // 2, 260)
                )

            desenhar_texto_destacado(
                window, "Pressione ENTER ou ESC para voltar", font_aviso, (200, 180, 150), (WIN_WIDTH // 2, 500)
            )

            pygame.display.flip()
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        pygame.mixer.music.stop()
                        exibindo = False