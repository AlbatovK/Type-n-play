from typing import List

import pygame.sprite
from pygame import Rect
from pygame.event import Event
from pygame.font import Font
from pygame.surface import Surface

from util.api_service import get_random_words
from util.asset_manager import play_sound, load_image
from util.threaded import threaded


class TypingEngine(pygame.sprite.Sprite):

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int, word_count: int):
        super().__init__()

        self.rect: Rect = Rect(x_pos, y_pos, width, height)
        self.from_last_frame = 0
        self.images = [
            pygame.transform.scale(load_image("text_back.png"), self.rect.size),
            pygame.transform.scale(load_image("text_back_active.png"), self.rect.size)
        ]
        self.image: Surface = self.images[0]
        self.last_frame = 0

        self.word_count = word_count
        self.words, self.written = "", ""
        self.load_words()

    @threaded
    def load_words(self) -> None:
        self.words = get_random_words(self.word_count)
        self.written = ""

    def update(self, events: List[Event]) -> None:

        for event in events:
            if event.type == pygame.KEYDOWN:

                if len(self.written) < len(self.words) and event.unicode == self.words[len(self.written)]:
                    self.written += event.unicode

                    if self.written == self.words:
                        text_done_event = pygame.event.Event(pygame.USEREVENT)
                        pygame.event.post(text_done_event)
                        self.load_words()

                else:
                    play_sound("error.wav")

    def draw(self, ms, screen: Surface, font: Font, color, written_color) -> None:

        self.from_last_frame += ms

        if self.from_last_frame > 800:
            self.last_frame = (self.last_frame + 1) % len(self.images)
            self.image = self.images[self.last_frame]
            self.from_last_frame = 0

        screen.blit(self.image, self.rect.topleft)

        def blit_multiline_text(surface: Surface, text: str, pos, _color) -> None:

            words = [word.split(' ') for word in text.splitlines()]
            space = font.size(' ')[0]

            (max_width, max_height), word_height = surface.get_size(), 0
            max_width -= 40
            max_height -= 40

            offset_x, offset_y = 60, 70
            x, y = pos
            x += offset_x
            y += offset_y

            for line in words:
                for word in line:

                    word_surface = font.render(word, 0, _color)
                    word_width, word_height = word_surface.get_size()[0], 50

                    if x + word_width >= max_width:
                        x = pos[0] + offset_x
                        y += word_height

                    surface.blit(word_surface, (x, y))
                    x += word_width + space

                x = pos[0] + offset_x
                y += word_height

        blit_multiline_text(screen, self.words, (self.rect.x, self.rect.y), color)
        blit_multiline_text(screen, self.written, (self.rect.x, self.rect.y), written_color)
