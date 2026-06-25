#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.player import Player
from code.obstaculo import Obstaculo
from code.background import Background

class FabricaEntidade:
    #Responsável por instanciar todas as entidades do jogo (Player, Obstáculos, etc).
    @staticmethod
    def criar_entidade(tipo, window, extra=None):
        if tipo == "Player":
            return Player(window)
        elif tipo == "Background":
            return Background(window)
        elif tipo == "Obstaculo":
            # extra contém {"tipo": str, "img": str} para inicializar a classe Obstaculo
            return Obstaculo(window, extra)

        # Caso o tipo não seja encontrado, retorna None (útil para debug)
        return None
