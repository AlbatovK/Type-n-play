from threading import Thread
from typing import Any

import pygame.sprite
from pygame import Rect

from util.api_service import get_random_words
from util.asset_manager import play_sound, load_image


class TypingEngine(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, width, height) -> None:
        super().__init__()
        self.rect = Rect(x_pos, y_pos, width, height)
        self.words = ""
        self.written = ""
        self.image = pygame.transform.scale(load_image("text_back.png"), self.rect.size)
        self.load_words()

    def load_words(self):
        def load():
            self.words = get_random_words(10)

        Thread(target=load, daemon=True).start()

    def update(self, events: Any) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if len(self.written) == len(self.words):
                    self.words, self.written = get_random_words(10), ""
                if event.unicode == self.words[len(self.written)]:
                    self.written += event.unicode
                else:
                    play_sound("error.wav")
                if self.written == self.words:
                    text_done_event = pygame.event.Event(pygame.USEREVENT)
                    pygame.event.post(text_done_event)

    def draw(self, screen: pygame.Surface, font, color, written_color):

        screen.blit(self.image, (self.rect.x, self.rect.y))

        def blit_text(surface, text, pos, _color):

            words = [word.split(' ') for word in text.splitlines()]
            space = font.size(' ')[0]
            max_width, max_height = surface.get_size()
            max_width -= 40
            max_height -= 40
            x, y = pos
            x += 50
            y += 40
            word_height = 0
            for line in words:
                for word in line:
                    word_surface = font.render(word, 0, _color)
                    word_width, word_height = word_surface.get_size()
                    word_height += 10
                    if x + word_width >= max_width:
                        x = pos[0] + 50
                        y += word_height
                    surface.blit(word_surface, (x, y))
                    x += word_width + space
                x = pos[0] + 50
                y += word_height

        blit_text(screen, self.words, (self.rect.x, self.rect.y), color)
        blit_text(screen, self.written, (self.rect.x, self.rect.y), written_color)
