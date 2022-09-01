import os
from os import path

import pygame as pg
from pygame.font import Font
from pygame.surface import Surface


def play_sound(filename: str) -> None:
    file_path: bytes = os.path.join("sound", filename)
    if not path.isfile(file_path):
        raise Exception(f"No such sound found: {file_path}")

    pg.mixer.music.load(file_path)
    pg.mixer.music.play()


def load_font(filename: str, size: int) -> Font:
    file_path: bytes = os.path.join("font", filename)
    if not path.isfile(file_path):
        raise Exception(f"No such font found: {file_path}")

    return pg.font.Font(file_path, size)


def load_image(filename: str) -> Surface:
    file_path: bytes = os.path.join('image', filename)
    if not path.isfile(file_path):
        raise Exception(f"No such image found: {file_path}")

    return pg.image.load(file_path)
