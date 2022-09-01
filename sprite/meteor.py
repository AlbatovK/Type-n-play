import pygame
from pygame import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from util.asset_manager import load_image


class Meteor(Sprite):

    image: pygame.Surface = load_image('meteor.png')
    velocity = 2

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int, velocity: int, group=pygame.sprite.Group()):

        self.rect: Rect = Rect(x_pos, y_pos, width, height)
        self.image: Surface = pygame.transform.scale(self.image, self.rect.size)

        self.velocity = velocity

        super().__init__(group)

    def blow(self):
        self.velocity = 0
        self.image = pygame.transform.scale(load_image('explosion.png'), self.rect.size)

    def intersect(self, obj: Sprite) -> bool:
        return obj.rect.colliderect(self.rect)

    def update(self) -> None:
        self.rect = self.rect.move(0, self.velocity)

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)
