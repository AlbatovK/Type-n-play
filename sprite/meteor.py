from typing import List

import pygame
from pygame import Rect
from pygame.sprite import Sprite

from util.asset_manager import load_image


class Meteor(Sprite):

    def __init__(self, x_pos, y_pos, width, height, velocity):
        super().__init__()
        rect = Rect(x_pos, y_pos, width, height)
        self.rect = rect
        self.original = load_image('rocket.png')
        self.image = pygame.transform.scale(self.original, self.rect.size)
        self.image = pygame.transform.rotate(self.image, 180.0)
        self.velocity = velocity

    def intersect(self, obj: Sprite):
        return obj.rect.colliderect(self.rect)

    def update(self):
        super().update()
        self.rect = self.rect.move(0, self.velocity)
