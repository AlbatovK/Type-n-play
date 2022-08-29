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

    def update(self, meteors):
        super().update()
        if self.last is not None and not self.rect.centerx == self.last.rect.center:
            sign = -1 if self.rect.x > self.last.rect.x else 1
            self.rect = self.rect.move(sign * 1, 0)
        elif self.last is not None:
            self.last = None
        else:
            self.turn_to_last(meteors)

    def turn_to_last(self, meteors):
        def max_y(m: Meteor):
            return m.rect.y

        suits = list(filter(lambda x: x.rect.y < self.rect.y, meteors))
        if suits:
            self.last = max(suits, key=max_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
