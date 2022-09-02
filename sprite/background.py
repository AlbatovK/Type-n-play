import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from util.asset_manager import load_image


class Background(Sprite):

    image: pygame.Surface = load_image('game_back.png')

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int, velocity: int, group=pygame.sprite.Group()):
        self.rect: Rect = Rect(x_pos, y_pos, width, height)
        self.image: Surface = pygame.transform.scale(self.image, self.rect.size)

        self.velocity = velocity

        super().__init__(group)

    def update(self) -> None:
        self.rect = self.rect.move(0, self.velocity)
        if self.rect.y == self.rect.height:
            self.rect.y = -self.rect.height

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)
