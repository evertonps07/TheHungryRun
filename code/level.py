# -*- coding: utf-8 -*-
import pygame
from code.entity_factory import EntityFactory
from code.score import desenhar_texto_destacado
from code.const import (
    WIN_WIDTH, WIN_HEIGHT, ASSET_STAGE_BGM, MUSIC_VOLUME, FPS,
    C_HUD_BG, C_HUD_TEXT, C_HUD_BORDER, C_WHITE,
    ENTITY_BACKGROUND, ENTITY_PLAYER, ENTITY_OBSTACULO,
    OBS_PTERODATILO, OBS_ESTEGOSSAURO, OBS_PEDRA, OBS_CARNE,
    SPEED_NORMAL, SPEED_FAST, SPAWN_COOLDOWN, PENALTY_TIME_MS,
    Y_POS_PTERODATILO, Y_POS_ESTEGOSSAURO, Y_POS_PEDRA,
    HUD_BOX_WIDTH, HUD_BOX_HEIGHT,
    ASSET_WIN_BG, ASSET_LOSE_BG
)

class Level:
    def __init__(self, window, game_ref=None, recorde=0):
        self.window = window
        self.game = game_ref
        self.recorde = recorde

        self.background = EntityFactory.create_entity(ENTITY_BACKGROUND, self.window)
        self.player = EntityFactory.create_entity(ENTITY_PLAYER, self.window)

        # Fila pré-definida de obstáculos que dita o ritmo e o fim da fase
        self.fila_obstaculos = [
            {"tipo": OBS_PEDRA, "img": "pedra1.png"}, {"tipo": OBS_PEDRA, "img": "pedra2.png"},
            {"tipo": OBS_PTERODATILO, "img": "pterodatilo1.png"}, {"tipo": OBS_PEDRA, "img": "pedra3.png"},
            {"tipo": OBS_PEDRA, "img": "pedra4.png"}, {"tipo": OBS_ESTEGOSSAURO, "img": "estegossauro1.png"},
            {"tipo": OBS_PEDRA, "img": "pedra5.png"}, {"tipo": OBS_PEDRA, "img": "pedra6.png"},
            {"tipo": OBS_CARNE, "img": "carne.png"}
        ]
        self.active_obstacles = []
        self.spawn_timer = 0
        self.distancia_entre_obstaculos = SPAWN_COOLDOWN
        self.paused = False
        self.tempo_inicial = pygame.time.get_ticks()
        self.penalidade_tempo = 0
        self.tempo_decorrero = 0.0

        pygame.font.init()
        self.font_hud = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_pause = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_fim = pygame.font.SysFont("Arial", 32, bold=True)

        self.COLOR_BG = C_HUD_BG
        self.COLOR_TEXT = C_HUD_TEXT
        self.clock = pygame.time.Clock()

        try:
            pygame.mixer.music.load(ASSET_STAGE_BGM)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print(f"Aviso: Falha ao carregar a música '{ASSET_STAGE_BGM}'.")

    def draw_hud_box(self, surface, rect):
        # Cria uma superfície separada para aplicar transparência (Alpha) no fundo das caixas da HUD
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((*self.COLOR_BG, 180))
        pygame.draw.rect(s, C_HUD_BORDER, s.get_rect(), border_radius=10, width=2)
        surface.blit(s, rect)

    def mostrar_tela_final(self, caminho_imagem, texto_principal):
        # Renderiza a imagem de fundo de fim de jogo e espera ENTER ou ESC para sair
        try:
            bg_fim = pygame.image.load(caminho_imagem).convert()
            bg_fim = pygame.transform.scale(bg_fim, (WIN_WIDTH, WIN_HEIGHT))
        except pygame.error:
            bg_fim = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            bg_fim.fill((20, 20, 20))

        aguardando = True
        while aguardando:
            self.window.blit(bg_fim, (0, 0))

            desenhar_texto_destacado(self.window, texto_principal, self.font_pause, (255, 215, 0),
                                     (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
            desenhar_texto_destacado(self.window, "Pressione ENTER ou ESC para continuar", self.font_fim, C_WHITE,
                                     (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50))

            pygame.display.flip()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        aguardando = False

        # A música do estágio para apenas aqui, quando o jogador sai da tela de vitória/derrota
        pygame.mixer.music.stop()

    def run(self):
        playing = True
        vitoria = False
        resultado_jogo = "Menu"

        while playing:
            self.clock.tick(FPS)

            # Verifica se a fila acabou e se não restam obstáculos perigosos na tela antes de liberar a carne
            caminho_da_vitoria = (len(self.fila_obstaculos) == 0 and not any(
                obs.type != OBS_CARNE for obs in self.active_obstacles))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.paused = not self.paused
                    if self.paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                if not self.paused and not vitoria and not caminho_da_vitoria:
                    self.player.handle_event(event)

            if not self.paused and not vitoria:
                # Calcula o tempo total de corrida somando os milissegundos de penalidade por colisões
                self.tempo_decorrero = (pygame.time.get_ticks() - self.tempo_inicial + self.penalidade_tempo) / 1000.0
                speed = SPEED_NORMAL if caminho_da_vitoria else (
                    SPEED_FAST if self.player.is_accelerating else SPEED_NORMAL)
                self.background.update(speed)
                self.player.update()

                # Controla o tempo de surgimento e posicionamento vertical de cada tipo de obstáculo
                self.spawn_timer += 1
                if self.spawn_timer > self.distancia_entre_obstaculos and len(self.fila_obstaculos) > 0:
                    info = self.fila_obstaculos.pop(0)
                    novo_obs = EntityFactory.create_entity(ENTITY_OBSTACULO, self.window, info)

                    novo_obs.rect.x = WIN_WIDTH + 50
                    if info["tipo"] == OBS_PTERODATILO:
                        novo_obs.rect.y = Y_POS_PTERODATILO
                    elif info["tipo"] == OBS_ESTEGOSSAURO:
                        novo_obs.rect.y = Y_POS_ESTEGOSSAURO
                    else:
                        novo_obs.rect.y = Y_POS_PEDRA

                    self.active_obstacles.append(novo_obs)
                    self.spawn_timer = 0

                # Varre a lista de obstáculos ativos para detecção de colisões e fim da fase
                for obs in self.active_obstacles[:]:
                    obs.update(speed)
                    if obs.rect.right < 0:
                        self.active_obstacles.remove(obs)
                        continue
                    if self.player.rect.colliderect(obs.rect):
                        if hasattr(obs, 'type') and obs.type == OBS_CARNE:
                            vitoria = True
                        else:
                            self.player.lives -= 1
                            self.penalidade_tempo += PENALTY_TIME_MS
                            self.active_obstacles.remove(obs)

                if self.player.lives <= 0:
                    resultado_jogo = "Game Over"
                    playing = False

            self.background.draw()
            self.player.draw()
            for obs in self.active_obstacles: obs.draw()

            hud_info = [
                (f"VIDAS: {self.player.lives}", 20),
                (f"TEMPO: {int(self.tempo_decorrero)}s", 20),
                (f"REC: {self.recorde:.2f}" if self.recorde > 0 else "REC: 00.00", 70)
            ]

            for i, (texto, y) in enumerate(hud_info):
                x = (WIN_WIDTH - HUD_BOX_WIDTH - 20) if i > 0 else 20
                if i == 2: x = (WIN_WIDTH - HUD_BOX_WIDTH - 20)
                rect = pygame.Rect(x, y, HUD_BOX_WIDTH, HUD_BOX_HEIGHT)
                self.draw_hud_box(self.window, rect)
                desenhar_texto_destacado(self.window, texto, self.font_hud, self.COLOR_TEXT, rect.center)

            if self.paused:
                txt_pause = self.font_pause.render("PAUSADO", True, C_WHITE)
                self.window.blit(txt_pause, txt_pause.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2)))

            if vitoria:
                resultado_jogo = "Vitoria"
                playing = False

            pygame.display.flip()

        if resultado_jogo == "Game Over":
            self.mostrar_tela_final(ASSET_LOSE_BG, "GAME OVER")
        elif resultado_jogo == "Vitoria":
            self.mostrar_tela_final(ASSET_WIN_BG, "VITÓRIA!")

        return resultado_jogo, self.tempo_decorrero