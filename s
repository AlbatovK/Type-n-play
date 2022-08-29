pg.font.init()

        self.screen = pg.display.set_mode(self.wnd_size)
        self.clock = pg.time.Clock()
        self.running = False
        self.font = pg.font.SysFont("Comic Sans MS", 30, False, False)
        self.cur_text = ''
        self.text = random.choice(words)

          srf = self.font.render(self.text, True, Color.WHITE.value)
        new_srf = self.font.render(self.cur_text, True, Color.YELLOW.value)

        self.screen.blit(new_srf, (10, 100))
        self.screen.blit(srf, (10, 100))

         elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.cur_text = self.cur_text[:-1] if len(self.cur_text) else ''
                    break
                if len(self.cur_text) == len(self.text):
                    self.text, self.cur_text = random.choice(words), ''
                if event.unicode == self.text[len(self.cur_text)]:
                    self.cur_text += event.unicode