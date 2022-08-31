import pygame
from pygame import Rect
from pygame.sprite import Sprite

from util.asset_manager import load_image


class Bullet(Sprite):

    def __init__(self, x_pos, y_pos, width, height, velocity):
        super().__init__()
        rect = Rect(x_pos, y_pos, width, height)
        self.rect = rect
        self.image = pygame.transform.scale(load_image('meteor.png'), self.rect.size)
        self.velocity = velocity

    def intersect(self, obj: Sprite):
        return obj.rect.colliderect(self.rect)

    def update(self):
        super().update()
        self.rect = self.rect.move(0, self.velocity)
