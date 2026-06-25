#!/usr/bin/python
# -*- coding: utf-8 -*-

class Entity:
    def __init__(self):
        self.name = None # Identificador da entidade
        self.surf = None # Superfície (a imagem renderizada)
        self.rect = None # Retângulo de colisão e posição (x, y, largura, altura)

    def move(self):
        pass
