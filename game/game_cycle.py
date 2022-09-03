import sys
import time

import pygame as pg
import pygame_widgets
from pygame.font import Font
from pygame_textinput import pygame_textinput, TextInputManager
from pygame_widgets.button import ButtonArray, Button

from game.color import Color
from game.event_code import EventCode
from game.game_state import GameState
from game.player import PlayerEnum
from sprite.background import Background
from sprite.bullet import Bullet
from sprite.meteor import Meteor
from sprite.rocket import Rocket
from sprite.typing_engine import TypingEngine
from util import threaded
from util.api_service import enter_session, create_session, get_last_event, post_event
from util.asset_manager import load_image, load_font
from util.text import *


class GameCycle:
    running = False
    wnd_size, fps = (720, 640), 60
    cur_state = GameState.ST_ENTER
    word_count = 5
    intro_dlt = 10

    session_id = None
    last_event_id = None
    player = None
    won = None
    count = None
    buttons = None
    cur_btn = 0

    small_font: Font = load_font("GangSmallYuxian.ttf", 35)
    font: Font = load_font("GangSmallYuxian.ttf", 40)
    medium_font: Font = load_font("GangSmallYuxian.ttf", 55)
    title_font: Font = load_font("GangSmallYuxian.ttf", 80)

    rocket = Rocket(110, 450, 100, 150)
    bullet_group = pg.sprite.Group()
    meteors = pg.sprite.Group()
    game_bgs = pg.sprite.Group()
    typing_engine = TypingEngine(320, 0, 400, 640, word_count)

    textinput = pygame_textinput.TextInputVisualizer(
        font_object=font,
        manager=TextInputManager(validator=validate),
        font_color=Color.WHITE.value,
        cursor_color=Color.WHITE.value
    )

    def init_buttons(self):

        @threaded.threaded
        def enter_wait_state():
            try:
                self.session_id = create_session()
                self.cur_state, self.player = GameState.ST_WAIT, PlayerEnum.FIRST
            except Exception as e:
                play_sound("error.wav")
                print(e)

        def enter_input_state():
            self.cur_state = GameState.ST_INPUT

        def exit_game():
            self.running = False

        self.buttons = ButtonArray(
            self.screen, 0, 340, 500, 200, (1, 3),
            border=0, separationThickness=20,
            hoverColours=[Color.BLACK.value] * 3,
            colour=Color.BLACK.value,
            inactiveColours=[Color.BLACK.value] * 3,
            textColours=[Color.GRAY.value] + [Color.WHITE.value] * 2,
            fonts=[self.font] * 3, texts=['Create Game', 'Enter Game', 'Exit'],
            onClicks=(enter_wait_state, enter_input_state, exit_game)
        )

        back_last = Background(0, -640, 320, 640, 2)
        back_first = Background(0, 0, 320, 640, 2)
        self.game_bgs.add(back_first, back_last)

    def __init__(self):
        pg.init()
        pg.font.init()
        pg.mixer.init()

        pg.display.set_caption("Type'n'play")
        pg.display.set_icon(load_image("icon.png"))
        self.screen = pg.display.set_mode(self.wnd_size)
        self.clock = pg.time.Clock()

        self.init_buttons()

    @threaded.threaded
    def play_intro(self):

        @threaded.threaded
        def start_countdown():
            self.count = 120
            while self.count > 0 and self.cur_state == GameState.ST_GAME:
                time.sleep(1)
                self.count -= 1
                if self.count < 10:
                    play_sound("blip.wav")

            if self.count == 0:
                self.won = PlayerEnum.SECOND
            post_event(self.session_id, EventCode.EVT_GMOVER.value)

        time.sleep(self.intro_dlt)
        self.cur_state = GameState.ST_GAME
        play_sound("blip.wav")
        start_countdown()

    def process_event_pool(self):

        if self.session_id is None:
            return

        try:
            event = get_last_event(self.session_id)
            print(event)
            if event['posId'] == self.last_event_id:
                return
            self.last_event_id = event['posId']

            if self.cur_state == GameState.ST_GAME:

                if event['eventCode'] == EventCode.EVT_METSPWN.value:
                    Meteor(x_pos=110, y_pos=-100, width=100, height=100, velocity=2, group=self.meteors)
                elif event['eventCode'] == EventCode.EVT_METDESTR.value:
                    Bullet(x_pos=145, y_pos=500, width=30, height=60, velocity=-5, group=self.bullet_group)
                    play_sound("laser.wav")
                elif event['eventCode'] == EventCode.EVT_GMOVER.value:
                    play_sound("blip.wav")
                    self.cur_state = GameState.ST_GAME_OVER

            elif self.cur_state == GameState.ST_WAIT or self.cur_state == GameState.ST_INPUT:

                if event['eventCode'] == EventCode.EVT_START.value:
                    self.last_event_id = event['posId']
                    self.cur_state = GameState.ST_INTRO
                    self.play_intro()
                    play_sound("alert.wav")

        except Exception as e:
            print(e)

    def start_game_cycle(self):

        self.running = True

        @threaded.cycled_factory(0.1, self)
        def event_pool():
            self.process_event_pool()

        event_pool()

        while self.running:
            self.clock.tick(self.fps)
            self.render()
            self.process_events()

        pg.quit()
        sys.exit()

    def render_game_over_state(self):
        self.screen.fill(Color.BLACK.value)
        text = ""
        if self.player == PlayerEnum.FIRST:
            text = outro_player_one_won if self.won == self.player else outro_player_one_lost
        elif self.player == PlayerEnum.SECOND:
            text = outro_player_two_won if self.won == self.player else outro_player_two_lost

        line_size = self.small_font.size(text.split("\n")[0])[1] + 10
        y = line_size
        for line in (text.split("\n") + ["Press any button to go to main screen"]):
            text_surface = self.small_font.render(line, True, Color.WHITE.value, Color.BLACK.value)
            self.screen.blit(text_surface, (30, y))
            y += line_size

    def render_enter_state(self):
        self.screen.blit(load_image("enter_background.png"), (0, 0))
        self.buttons.draw()
        title_size_x = self.title_font.size("Type'n'play")[0]
        text_surface = self.title_font.render("Type'n'play", True, Color.WHITE.value, Color.BLACK.value)
        self.screen.blit(text_surface, ((500 - title_size_x) // 2, 190))

    def render_input_state(self):
        self.screen.blit(load_image("enter_background.png"), (0, 0))
        self.screen.blit(self.textinput.surface, (50, 270))
        title_size_x = self.medium_font.size("Enter session id")[0]
        text_surface = self.medium_font.render("Enter session id", True, Color.WHITE.value, Color.BLACK.value)
        self.screen.blit(text_surface, ((500 - title_size_x) // 2, 190))

    def render_wait_state(self):
        self.screen.blit(load_image("enter_background.png"), (0, 0))
        title_size_x = self.medium_font.size('Your session id')[0]
        text_surface = self.medium_font.render("Your session id", True, Color.WHITE.value, Color.BLACK.value)
        self.screen.blit(text_surface, ((500 - title_size_x) // 2, 190))
        id_size_x = self.medium_font.size(str(self.session_id))[0]
        id_surface = self.medium_font.render(str(self.session_id), True, Color.WHITE.value, Color.BLACK.value)
        self.screen.blit(id_surface, ((500 - id_size_x) // 2, 300))

    def render_intro_state(self):
        self.screen.fill(Color.BLACK.value)
        text = intro_player_one if self.player == PlayerEnum.FIRST else intro_player_two
        line_size = self.small_font.size(text.split("\n")[0])[1] + 10
        y = line_size
        for line in text.split("\n"):
            text_surface = self.small_font.render(line, True, Color.WHITE.value, Color.BLACK.value)
            self.screen.blit(text_surface, (30, y))
            y += line_size

    def render_game_state(self):
        self.screen.fill(Color.BLACK.value)
        self.game_bgs.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.rocket.draw(self.screen)
        self.meteors.draw(self.screen)
        self.typing_engine.draw(self.screen, self.small_font, Color.WHITE.value, Color.BLACK.value)
        countdown_x, countdown_y = self.medium_font.size(str(self.count))
        text_surface = self.medium_font.render(str(self.count), True, Color.WHITE.value)
        self.screen.blit(text_surface, (520 - countdown_x // 2, 640 - countdown_y - 90))

    def render(self):
        if self.cur_state == GameState.ST_ENTER:
            self.render_enter_state()

        elif self.cur_state == GameState.ST_INPUT:
            self.render_input_state()

        elif self.cur_state == GameState.ST_WAIT:
            self.render_wait_state()

        elif self.cur_state == GameState.ST_INTRO:
            self.render_intro_state()

        elif self.cur_state == GameState.ST_GAME:
            self.render_game_state()

        elif self.cur_state == GameState.ST_GAME_OVER:
            self.render_game_over_state()

        pg.display.update()

    def process_game_over_events(self, events):

        for event in events:
            if event.type == pg.KEYDOWN:
                self.bullet_group = pg.sprite.Group()
                self.meteors = pg.sprite.Group()
                self.cur_state = pg.sprite.Group()
                self.rocket = Rocket(110, 450, 100, 150)
                self.typing_engine.load_words()

                self.cur_state = GameState.ST_ENTER

                self.session_id = None
                self.player = None
                self.count = None

                play_sound("select.wav")

    def process_input_events(self, events):
        self.textinput.update(events)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:

                    @threaded.threaded
                    def enter_session_by_id():
                        try:
                            sid = int(self.textinput.value)
                            enter_session(sid)
                            self.session_id = sid
                            self.player = PlayerEnum.SECOND
                        except Exception as e:
                            play_sound("error.wav")
                            print(e)

                    enter_session_by_id()

    def process_game_events(self, events):
        self.rocket.update(events)
        self.meteors.update()
        self.bullet_group.update()
        self.typing_engine.update(events)
        self.game_bgs.update()

        for event in events:
            if event.type == pg.USEREVENT:

                @threaded.threaded
                def post_events():
                    code = EventCode.EVT_METSPWN if self.player == PlayerEnum.FIRST else EventCode.EVT_METDESTR
                    post_event(self.session_id, code.value)

                post_events()

        delete_m = []
        delete_b = []
        for meteor in self.meteors.sprites():
            if self.rocket.intersect(meteor):
                self.won = PlayerEnum.FIRST
                play_sound("explosion.wav")
                self.meteors.remove(meteor)
                self.rocket.blow()

                @threaded.threaded
                def end_game():
                    time.sleep(1)
                    post_event(self.session_id, EventCode.EVT_GMOVER.value)

                end_game()

            for bullet in self.bullet_group.sprites():
                if isinstance(bullet, Bullet) and bullet.intersect(meteor):
                    delete_m.append(meteor)
                    delete_b.append(bullet)
                    if isinstance(meteor, Meteor):
                        meteor.blow()
                    play_sound("explosion.wav")

        self.bullet_group.remove(delete_b)

        @threaded.threaded
        def delete_meteor():
            time.sleep(1)
            self.meteors.remove(delete_m)

        if len(delete_m):
            delete_meteor()

    def process_enter_events(self, events):
        pygame_widgets.update(events)

        for event in events:
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_RETURN:
                    self.buttons.getButtons()[self.cur_btn].onClick()
                    play_sound('select.wav')

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

    def process_events(self):

        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False

        if self.cur_state == GameState.ST_ENTER:
            self.process_enter_events(events)
        elif self.cur_state == GameState.ST_INPUT:
            self.process_input_events(events)
        elif self.cur_state == GameState.ST_GAME:
            self.process_game_events(events)
        elif self.cur_state == GameState.ST_GAME_OVER:
            self.process_game_over_events(events)
