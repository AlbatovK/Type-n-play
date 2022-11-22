import pygame
from pygame import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from util.asset_manager import load_image


class Meteor(Sprite):
    velocity = 3

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int, velocity: int, group=pygame.sprite.Group()):
        self.from_last_frame = 0
        self.rect: Rect = Rect(x_pos, y_pos, width, height)
        self.animate = True
        self.images = [
            pygame.transform.scale(load_image('meteor.png'), self.rect.size),
            pygame.transform.scale(load_image('meteor_fly.png'), self.rect.size)
        ]
        self.image: Surface = self.images[0]
        self.last_frame = 0
        self.velocity = velocity

        super().__init__(group)

    def blow(self):
        self.velocity = 0
        self.animate = False
        self.image = pygame.transform.scale(load_image('explosion.png'), self.rect.size)

    def intersect(self, obj: Sprite) -> bool:
        return obj.rect.colliderect(self.rect)

    def update(self, ms) -> None:
        self.from_last_frame += ms

        if self.from_last_frame > 300 and self.animate:
            self.last_frame = (self.last_frame + 1) % len(self.images)
            self.image = self.images[self.last_frame]
            self.from_last_frame = 0

        self.rect = self.rect.move(0, self.velocity)

    def draw(self, screen, ms) -> None:
        screen.blit(self.image, self.rect)
