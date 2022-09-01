import pygame
from pygame import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from util.asset_manager import load_image


class Bullet(Sprite):

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int, velocity: int):
        super().__init__()

        self.rect: Rect = Rect(x_pos, y_pos, width, height)
        self.image: Surface = pygame.transform.scale(load_image('meteor.png'), self.rect.size)
        self.velocity: int = velocity

    def intersect(self, obj: Sprite) -> bool:
        return obj.rect.colliderect(self.rect)

    def update(self) -> None:
        self.rect = self.rect.move(0, self.velocity)
