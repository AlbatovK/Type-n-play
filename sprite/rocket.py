import pygame
from pygame import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from util.asset_manager import load_image


class Rocket(Sprite):

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int):
        super().__init__()

        self.rect: Rect = Rect(x_pos, y_pos, width, height)
        self.image: Surface = pygame.transform.scale(load_image('rocket.png'), self.rect.size)

    def blow(self):
        self.image = pygame.transform.scale(load_image('explosion.png'), self.rect.size)

    def intersect(self, obj: Sprite) -> bool:
        return obj.rect.colliderect(self.rect)

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)
