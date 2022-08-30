import pygame
from pygame import Rect
from pygame.sprite import Sprite

from sprite.meteor import Meteor
from util.asset_manager import load_image


class Rocket(Sprite):
    last = None

    def __init__(self, x_pos, y_pos, width, height, velocity):
        super().__init__()
        self.rect = Rect(x_pos, y_pos, width, height)
        self.original = load_image('rocket.png')
        self.image = pygame.transform.scale(self.original, self.rect.size)
        self.velocity = velocity

    def intersect(self, obj: Sprite):
        return obj.rect.colliderect(self.rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
