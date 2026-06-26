# -*- coding: utf-8 -*-

# CONFIGURAÇÕES GERAIS DO JOGO (CONSTANTES)

# A - Caminhos de Assets
ASSET_FOLDER = "asset/"
ASSET_BG_LAYER1 = "asset/deserto01.jpeg"
ASSET_BG_LAYER2 = "asset/deserto02.jpeg"
ASSET_MENU_BG = "asset/imagemmenu.jpeg"
ASSET_SCORE_BG = "asset/deserto03.jpeg"
ASSET_HELP_BG = "asset/deserto03.jpeg"
ASSET_MENU_BGM = "asset/MenuDin.mp3"
ASSET_SCORE_BGM = "asset/MenuDin.mp3"
ASSET_HELP_BGM = "asset/MenuDin.mp3"
ASSET_WIN_BG = "asset/TRexVitoria1.jpeg"
ASSET_LOSE_BG = "asset/TRexDerrota1.jpeg"
ASSET_STAGE_BGM = "asset/fase1.mp3"
ASSET_PLAYER = "asset/TRex1.png"

# B - Banco de Dados e Persistência
DB_NAME = 'the_hungry_run.db'
DEFAULT_PLAYER_NAME = "TREX"
SCORE_ROUND_PRECISION = 2
DATE_FORMAT = "%d/%m/%Y"

# C - Cores (RGB / RGBA)
C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)
C_YELLOW = (255, 255, 0)
C_LIGHT_YELLOW = (255, 255, 200)
C_DARK_GRAY = (40, 40, 40)
C_BOX_NORMAL = (210, 180, 140)
C_BOX_HOVER = (245, 222, 179)
C_BORDER = (100, 70, 40)
C_GREEN_WIN = (34, 139, 34)
C_RED_LOSE = (139, 0, 0)
C_HUD_BG = (60, 50, 40)
C_HUD_TEXT = (255, 230, 200)
C_HUD_BORDER = (200, 180, 150, 100)

# D - Dimensões e Tamanhos das Entidades (Largura, Altura)
SIZE_PLAYER = (130, 150)
SIZE_PTERODATILO = (180, 130)
SIZE_CARNE = (100, 100)
SIZE_ESTEGOSSAURO = (200, 140)
SIZE_PEDRA = (120, 120)

# E - Tipos de Entidades e Obstáculos
ENTITY_BACKGROUND = "Background"
ENTITY_OBSTACULO = "Obstaculo"
ENTITY_PLAYER = "Player"

OBS_PTERODATILO = "pterodatilo"
OBS_ESTEGOSSAURO = "estegossauro"
OBS_PEDRA = "pedra"
OBS_CARNE = "carne"

# F - Fontes e Efeitos Visuais
FONT_NAME = "Arial"
FONT_SIZE_NORMAL = 36
FONT_SIZE_SELECTED = 42
SHADOW_OFFSET = 2

# I - Inputs (Controles e Dispositivos)
MOUSE_LEFT_BUTTON = 1

# J - Balanço de Jogabilidade (Gameplay Tuning)
FPS = 60
SPEED_NORMAL = 6
SPEED_FAST = 11
# Intervalo de frames mínimo para o nascimento de um novo obstáculo
SPAWN_COOLDOWN = 130
# Tempo em milissegundos adicionado ao cronômetro como punição ao tomar dano
PENALTY_TIME_MS = 2000
DELAY_VICTORY_MS = 1000
PLAYER_INITIAL_LIVES = 3
# Força da gravidade que puxa o T-Rex para baixo a cada frame após o pulo
PLAYER_GRAVITY = 0.9
# Impulso vertical inicial aplicado ao eixo Y do T-Rex para realizar o pulo
PLAYER_JUMP_SPEED = -22

# M - Menus e Dimensões de Interface
MENU_OPTION = ["NEW GAME", "SCORE", "EXIT"]
MENU_BOX_WIDTH = 260
MENU_BOX_HEIGHT = 55
MENU_Y_START = 360
MENU_Y_SPACING = 75
MENU_BOX_RADIUS = 10
MENU_BORDER_WIDTH = 3
HUD_BOX_WIDTH = 150
HUD_BOX_HEIGHT = 45

# O - Posições de Altura (Y) e Inicialização (X)
# Define as alturas fixas de spawn para cada tipo de obstáculo alinhar com o chão ou ar
Y_POS_PTERODATILO = 270
Y_POS_ESTEGOSSAURO = 395
Y_POS_PEDRA = 450
PLAYER_START_X = 100
PLAYER_FLOOR_Y = 400

# R - Retornos de Fluxo (Estados do Jogo)
RETURN_START = "Iniciar"
RETURN_SCORE = "Score"
RETURN_START = "START"
RETURN_SCORE = "SCORE"
RETURN_HELP = "HELP"
RETURN_EXIT = "EXIT"

# T - Dimensões da Tela e Configurações Globais
WIN_TITLE = "The Hungry Run"
WIN_WIDTH = 800
WIN_HEIGHT = 600
MUSIC_VOLUME = 0.5

