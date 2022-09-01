from enum import Enum


class GameState(Enum):
    ST_ENTER = 0
    ST_INPUT = 1
    ST_WAIT = 2
    ST_GAME = 3
    ST_INTRO = 4
    ST_GAME_OVER = 5
