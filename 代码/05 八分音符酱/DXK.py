# -*- coding: utf-8 -*-
import pygame
class DXK(pygame.sprite.Sprite):
    def __init__(self, picture):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(picture).convert_alpha()
        self.width, self.height = self.image.get_size()
        self.can_jump = True
        self.can_fly = False
        self.speed_x = 0
        self.speed_y = 0
        self.g = 0.02

    def jump(self, speed):
        if self.can_jump:
            self.can_jump = False
            self.speed_y = speed

    def land(self):
        self.can_jump = True
        self.speed_y = 0

    def move(self):
        self.speed_x = -1.25

    def fly(self):
        self.can_fly = True
        self.g = 0.015

    def stop(self):
        self.speed_x = 0
        self.can_fly = True
        self.g = 0.02

class Block(pygame.sprite.Sprite):
    def __init__(self, picture):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(picture).convert_alpha()
        self.width, self.height = self.image.get_size()