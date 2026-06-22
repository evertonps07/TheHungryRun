# THE HUNGRY RUN
import pygame

print("Setup Start")
pygame.init()

# Definição das dimensões da tela
LARGURA_TELA = 800
ALTURA_TELA = 600

# Inicialização da janela gráfica e definição do título
window = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("The Hungry Run")

print("Setup End")
print("Loop Start")

# Loop contínuo de execução do jogo
while True:
    # Captação e processamento da fila de eventos do sistema operacional
    for event in pygame.event.get():
        # Interrupção do programa caso o botão de fechar a janela seja acionado
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()