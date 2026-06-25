import pygame
from code.menu import Menu
from code.level import Level


def desenhar_texto_destacado(surface, text, font, color, pos):
    # Desenha texto com sombra para efeito de profundidade e legibilidade.
    sombra = font.render(text, True, (0, 0, 0))
    real = font.render(text, True, color)
    x, y = pos
    # Desenha a sombra levemente deslocada para dar o efeito de destaque
    surface.blit(sombra, (x - real.get_width() // 2 + 2, y - real.get_height() // 2 + 2))
    surface.blit(real, (x - real.get_width() // 2, y - real.get_height() // 2))


class Game:
    # Gerenciador principal do fluxo do jogo e persistência de pontuações.

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Hungry Run")
        self.window = pygame.display.set_mode(size=(800, 600))
        self.lista_scores = []

    def mostrar_tela_final(self, titulo, mensagem, cor_fundo):
        # Renderiza a tela de final de jogo com imagem de fundo e estilo elegante.

        # Define qual imagem carregar baseando-se no título da tela
        nome_img = "asset/TRexVitoria1.jpeg" if "VENCEU" in titulo else "asset/TRexDerrota1.jpeg"

        # Tenta carregar a imagem correspondente, caso não exista, usa cor sólida
        try:
            img_fim = pygame.image.load(nome_img).convert()
            img_fim = pygame.transform.scale(img_fim, (800, 600))
        except FileNotFoundError:
            img_fim = pygame.Surface((800, 600))
            img_fim.fill(cor_fundo)

        # Overlay escuro para garantir que o texto branco se destaque
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))

        font_titulo = pygame.font.SysFont("Arial", 60, bold=True)
        font_msg = pygame.font.SysFont("Arial", 30, bold=True)
        font_instr = pygame.font.SysFont("Arial", 24, italic=True)

        loop = True
        while loop:
            self.window.blit(img_fim, (0, 0))
            self.window.blit(overlay, (0, 0))

            # Desenha os textos usando o metodo de instância
            desenhar_texto_destacado(self.window, titulo, font_titulo, (255, 255, 255), (400, 150))
            desenhar_texto_destacado(self.window, mensagem, font_msg, (245, 222, 179), (400, 250))
            desenhar_texto_destacado(self.window, "Pressione ENTER para voltar ao Menu", font_instr,
                                          (255, 255, 255), (400, 500))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    loop = False

    def mostrar_tela_scores(self):
        # Exibe o ranking dos tempos mais rápidos registrados com fundo temático.
        font_titulo = pygame.font.SysFont("Arial", 46, bold=True)
        font_dados = pygame.font.SysFont("Arial", 32)

        # Cores claras para o texto (o destaque preto virá da sua função)
        cor_clara = (255, 255, 200)

        try:
            img_fundo = pygame.image.load("asset/deserto03.jpeg").convert()
            img_fundo = pygame.transform.scale(img_fundo, (800, 600))
        except FileNotFoundError:
            img_fundo = pygame.Surface((800, 600))
            img_fundo.fill((40, 40, 40))

        # Escurecimento mais forte para garantir contraste
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        loop = True
        while loop:
            self.window.blit(img_fundo, (0, 0))
            self.window.blit(overlay, (0, 0))

            # Desenha usando sua função que já coloca a sombra preta
            desenhar_texto_destacado(self.window, "ÚLTIMOS SCORES", font_titulo, cor_clara, (400, 80))

            if not self.lista_scores:
                desenhar_texto_destacado(self.window, "Nenhum recorde registrado ainda!", font_dados, cor_clara,
                                         (400, 250))
            else:
                for index, tempo in enumerate(self.lista_scores):
                    texto = f"{index + 1}º Lugar: {tempo:.2f} segundos"
                    desenhar_texto_destacado(self.window, texto, font_dados, cor_clara, (400, 200 + (index * 60)))

            desenhar_texto_destacado(self.window, "Pressione ENTER ou ESC para voltar", font_dados, (255, 255, 255),
                                     (400, 480))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    loop = False

    def adicionar_score(self, novo_tempo):
        # Adiciona novo score e limita a lista aos 4 melhores.
        self.lista_scores.append(novo_tempo)
        self.lista_scores.sort()
        if len(self.lista_scores) > 4:
            self.lista_scores = self.lista_scores[:4]

    def run(self):
        # Loop principal do jogo.
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == "Iniciar":
                melhor_tempo = min(self.lista_scores) if self.lista_scores else 0
                level = Level(self.window, recorde=melhor_tempo)
                resultado, tempo = level.run()

                if resultado == "Vitoria":
                    self.adicionar_score(tempo)
                    self.mostrar_tela_final("VOCÊ VENCEU!", f"Tempo total: {tempo:.2f} segundos", (34, 139, 34))
                elif resultado == "Game Over":
                    self.mostrar_tela_final("GAME OVER", "Suas vidas acabaram.", (139, 0, 0))

            elif menu_return == "Score":
                self.mostrar_tela_scores()