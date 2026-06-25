import pygame
from code.fabricaEntidade import FabricaEntidade


class Level:
    # Gerencia o loop principal da fase com interface elegante.

    def __init__(self, window, game_ref=None, recorde=0):
        self.window = window
        self.game = game_ref
        self.recorde = recorde
        self.background = FabricaEntidade.criar_entidade("Background", self.window)
        self.player = FabricaEntidade.criar_entidade("Player", self.window)

        # Fila de obstáculos
        self.fila_obstaculos = [
            {"tipo": "pedra", "img": "pedra1.png"}, {"tipo": "pedra", "img": "pedra2.png"},
            {"tipo": "pterodatilo", "img": "pterodatilo1.png"}, {"tipo": "pedra", "img": "pedra3.png"},
            {"tipo": "pedra", "img": "pedra4.png"}, {"tipo": "estegossauro", "img": "estegossauro1.png"},
            {"tipo": "pedra", "img": "pedra5.png"}, {"tipo": "pedra", "img": "pedra6.png"},
            {"tipo": "carne", "img": "carne.png"}
        ]
        self.active_obstacles = []
        self.spawn_timer = 0
        self.distancia_entre_obstaculos = 130
        self.paused = False
        self.tempo_inicial = pygame.time.get_ticks()
        self.penalidade_tempo = 0  # Armazena milissegundos de penalidade
        self.tempo_decorrero = 0.0

        # Fontes e Cores Elegantes
        pygame.font.init()
        self.font_hud = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_pause = pygame.font.SysFont("Arial", 50, bold=True)

        self.COLOR_BG = (60, 50, 40)  # Marrom escuro elegante
        self.COLOR_TEXT = (255, 230, 200)  # Creme suave

        self.clock = pygame.time.Clock()

    def draw_hud_box(self, surface, rect):
        # Desenha caixa com transparência e borda sutil.
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((*self.COLOR_BG, 180))  # 180 é o nível de transparência
        pygame.draw.rect(s, (200, 180, 150, 100), s.get_rect(), border_radius=10, width=2)
        surface.blit(s, rect)

    def draw_text_with_shadow(self, surface, text, rect):
        # Desenha texto com sombra para efeito de profundidade.
        sombra = self.font_hud.render(text, True, (30, 30, 30))
        real = self.font_hud.render(text, True, self.COLOR_TEXT)
        surface.blit(sombra, (rect.centerx - real.get_width() // 2 + 1, rect.centery - real.get_height() // 2 + 1))
        surface.blit(real, (rect.centerx - real.get_width() // 2, rect.centery - real.get_height() // 2))

    def run(self):
        playing, vitoria, resultado_jogo = True, False, "Menu"
        while playing:
            self.clock.tick(60)

            caminho_da_vitoria = (len(self.fila_obstaculos) == 0 and not any(
                obs.tipo != "carne" for obs in self.active_obstacles))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.paused = not self.paused
                if not self.paused and not vitoria and not caminho_da_vitoria:
                    self.player.handle_event(event)

            if not self.paused and not vitoria:
                # O tempo final agora inclui a penalidade acumulada
                self.tempo_decorrero = (pygame.time.get_ticks() - self.tempo_inicial + self.penalidade_tempo) / 1000.0
                speed = 6 if caminho_da_vitoria else (11 if self.player.is_accelerating else 6)
                self.background.update(speed)
                self.player.update()

                self.spawn_timer += 1
                if self.spawn_timer > self.distancia_entre_obstaculos and len(self.fila_obstaculos) > 0:
                    info = self.fila_obstaculos.pop(0)
                    novo_obs = FabricaEntidade.criar_entidade("Obstaculo", self.window, info)
                    novo_obs.rect.y = 280 if info["tipo"] == "pterodatilo" else (
                        395 if info["tipo"] == "estegossauro" else 450)
                    self.active_obstacles.append(novo_obs)
                    self.spawn_timer = 0

                for obs in self.active_obstacles[:]:
                    obs.update(speed)
                    if obs.rect.right < 0:
                        self.active_obstacles.remove(obs)
                        continue
                    if self.player.rect.colliderect(obs.rect):
                        if hasattr(obs, 'tipo') and obs.tipo == "carne":
                            vitoria = True
                        elif hasattr(obs, 'tipo') and obs.tipo == "pterodatilo":
                            if self.player.is_jumping:
                                self.player.lives -= 1
                                self.penalidade_tempo += 2000  # Adiciona 2s (2000ms)
                                self.active_obstacles.remove(obs)
                        else:
                            self.player.lives -= 1
                            self.penalidade_tempo += 2000  # Adiciona 2s (2000ms)
                            self.active_obstacles.remove(obs)
                if self.player.lives <= 0:
                    resultado_jogo = "Game Over"
                    playing = False

            # Renderização
            self.background.draw()
            self.player.draw()
            for obs in self.active_obstacles:
                obs.draw()

            # --- HUD ---
            hud_info = [
                (f"VIDAS: {self.player.lives}", 20),
                (f"TEMPO: {int(self.tempo_decorrero)}s", 20),
                (f"REC: {self.recorde:.2f}" if self.recorde > 0 else "REC: 00.00", 70)
            ]

            for i, (texto, y) in enumerate(hud_info):
                x = 630 if i > 0 else 20
                if i == 2: x = 630
                rect = pygame.Rect(x, y, 150, 45)
                self.draw_hud_box(self.window, rect)
                self.draw_text_with_shadow(self.window, texto, rect)

            if self.paused:
                txt_pause = self.font_pause.render("PAUSADO", True, (255, 255, 255))
                self.window.blit(txt_pause, txt_pause.get_rect(center=(400, 300)))
            if vitoria:
                pygame.time.delay(1000)
                resultado_jogo = "Vitoria"
                playing = False

            pygame.display.flip()
        return resultado_jogo, self.tempo_decorrero