import sys
import time
from enum import Enum
from threading import Thread

import pygame as pg
import pygame_widgets
from pygame.font import Font
from pygame.rect import Rect
from pygame_textinput import pygame_textinput, TextInputManager
from pygame_widgets.button import ButtonArray, Button

from util.api_service import enter_session, create_session, get_last_event
from util.asset_manager import load_image, load_font, play_sound


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)


class GameState(Enum):
    ST_ENTER = 0
    ST_INPUT = 1
    ST_WAIT = 2
    ST_GAME = 3


def validate(string):
    play_sound("select.wav")
    return (string.isdigit() and len(string) <= 6) or not string


class GameCycle:
    running = False
    wnd_size, fps = (720, 640), 60
    cur_state = GameState.ST_ENTER
    session_id = None

    font: Font = load_font("GangSmallYuxian.ttf", 40)
    medium_font: Font = load_font("GangSmallYuxian.ttf", 55)
    title_font: Font = load_font("GangSmallYuxian.ttf", 80)

    textinput = pygame_textinput.TextInputVisualizer(
        font_object=font,
        manager=TextInputManager(validator=lambda x: validate(x)),
        font_color=Color.WHITE.value,
        cursor_color=Color.WHITE.value
    )

    text_position = [50, 270]

    def __init__(self):
        pg.init()
        pg.font.init()
        pg.mixer.init()

        pg.display.set_caption("Type'n'play")
        pg.display.set_icon(load_image("icon.jpg"))
        self.screen = pg.display.set_mode(self.wnd_size)
        self.clock = pg.time.Clock()

        def enter_input_state():
            self.cur_state = GameState.ST_INPUT

        def enter_wait_state():
            def enter_threaded():
                self.session_id = create_session()
                self.cur_state = GameState.ST_WAIT

            Thread(target=enter_threaded).start()

        def game_exit():
            self.running = False

        self.buttons = ButtonArray(
            self.screen, 0, 340, 500, 200, (1, 3),
            border=0, separationThickness=20,
            hoverColours=[Color.BLACK.value] * 3, colour=Color.BLACK.value,
            inactiveColours=[Color.BLACK.value] * 3,
            textColours=[Color.GRAY.value] + [Color.WHITE.value] * 2,
            fonts=[self.font] * 3, texts=['Create Game', 'Enter Game', 'Exit'],
            onClicks=(enter_wait_state, enter_input_state, game_exit)
        )

        self.cur_btn = 0

    def start_game_cycle(self):
        self.running = True

        def event_pool():
            while self.running:
                if self.cur_state == GameState.ST_WAIT or self.cur_state == GameState.ST_INPUT:
                    if self.session_id is not None:
                        try:
                            event = get_last_event(self.session_id)
                            print(event)
                            if event['eventCode'] == 1:
                                play_sound("alert.wav")
                                self.cur_state = GameState.ST_GAME
                            time.sleep(1)
                        except Exception as e:
                            print(e)

        Thread(target=event_pool, daemon=True).start()

        while self.running:
            self.process_events()
            self.pre_render()
            self.render()

        pg.quit()
        sys.exit()

    def pre_render(self):
        self.clock.tick(self.fps)

    def render(self):
        if self.cur_state == GameState.ST_ENTER:
            self.screen.blit(load_image("enter_background.png"), (0, 0))
            self.buttons.draw()
            title_size_x = self.title_font.size("Type'n'play")[0]
            text_surface = self.title_font.render("Type'n'play", True, Color.WHITE.value, Color.BLACK.value)
            self.screen.blit(text_surface, ((500 - title_size_x) // 2, 190))

        elif self.cur_state == GameState.ST_INPUT:
            self.screen.blit(load_image("enter_background.png"), (0, 0))
            self.screen.blit(self.textinput.surface, self.text_position)
            title_size_x = self.medium_font.size("Enter session id")[0]
            text_surface = self.medium_font.render("Enter session id", True, Color.WHITE.value, Color.BLACK.value)
            self.screen.blit(text_surface, ((500 - title_size_x) // 2, 190))

        elif self.cur_state == GameState.ST_WAIT:
            self.screen.blit(load_image("enter_background.png"), (0, 0))
            title_size_x = self.medium_font.size('Your session id')[0]
            text_surface = self.medium_font.render("Your session id", True, Color.WHITE.value, Color.BLACK.value)
            self.screen.blit(text_surface, ((500 - title_size_x) // 2, 190))
            id_size_x = self.medium_font.size(str(self.session_id))[0]
            id_surface = self.medium_font.render(str(self.session_id), True, Color.WHITE.value, Color.BLACK.value)
            self.screen.blit(id_surface, ((500 - id_size_x) // 2, 300))

        elif self.cur_state == GameState.ST_GAME:
            self.screen.blit(load_image("enter_background.png"), (0, 0))

        pg.display.update()

    def process_events(self):

        events = pg.event.get()
        if self.cur_state == GameState.ST_ENTER:
            pygame_widgets.update(events)
        elif self.cur_state == GameState.ST_INPUT:
            self.textinput.update(events)

        for event in events:

            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False

            if self.cur_state == GameState.ST_ENTER:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        play_sound('select.wav')
                        self.buttons.getButtons()[self.cur_btn].onClick()
                    elif event.key in [pg.K_UP, pg.K_DOWN]:
                        play_sound('select.wav')

                        if event.key == pg.K_UP:
                            self.cur_btn = (self.cur_btn - 1) % 3
                        elif event.key == pg.K_DOWN:
                            self.cur_btn = (self.cur_btn + 1) % 3

                        for button in self.buttons.getButtons():
                            button.textColour = Color.WHITE.value
                            button.text = self.font.render(button.string, True, button.textColour)

                        btn: Button = self.buttons.getButtons()[self.cur_btn]
                        btn.textColour = Color.GRAY.value
                        btn.text = self.font.render(btn.string, True, btn.textColour)

            elif self.cur_state == GameState.ST_INPUT:

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:

                        def enter_session_by_id():
                            try:
                                sid = int(self.textinput.value)
                                enter_session(sid)
                                self.session_id = sid
                            except Exception as e:
                                print(e)

                        Thread(target=enter_session_by_id).start()

            elif self.cur_state == GameState.ST_GAME:
                pass
