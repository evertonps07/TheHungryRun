# -*- coding: utf-8 -*-
from code.player import Player
from code.obstacle import Obstacle
from code.background import Background
from code.const import ENTITY_PLAYER, ENTITY_BACKGROUND, ENTITY_OBSTACULO

class EntityFactory:
    @staticmethod
    def create_entity(entity_type, window, extra=None):
        # Centraliza a criação e instanciação de todas as entidades do jogo (Pattern Factory)
        if entity_type == ENTITY_PLAYER:
            return Player(window)
        elif entity_type == ENTITY_BACKGROUND:
            return Background(window)
        elif entity_type == ENTITY_OBSTACULO:
            # Passa o dicionário 'extra' para configurar as propriedades específicas do obstáculo
            return Obstacle(window, extra)
        return None