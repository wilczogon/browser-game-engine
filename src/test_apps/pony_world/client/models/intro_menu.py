from pyfiglet import figlet_format
import curses
from .utils import draw_on_center, draw_menu_2


class IntroMenu:
    options = ['login', 'register']

    labels = {
        'login': 'Login',
        'register': 'Register'
    }

    def __init__(self, stdscr, title, font):
        self.stdscr = stdscr
        self.title = title
        self.font = font
        self.choosen_option = 0

    def get_answer(self):
        self.stdscr.clear()
        curses.curs_set(False)

        logo = figlet_format(self.title, font=self.font)
        lines = logo.split('\n')

        logo_win = self.stdscr.subwin(len(lines) + 2, curses.COLS, 0, 0)

        draw_on_center(logo_win, lines, 2)

        logo_y, logo_x = logo_win.getmaxyx()

        menu_win = self.stdscr.subwin(curses.LINES - logo_y, curses.COLS, logo_y, 0)

        logo_win.refresh()

        while True:
            draw_menu_2(menu_win, [self.labels[o] for o in self.options], self.choosen_option, start_y=2)

            menu_win.refresh()

            result = self.stdscr.getch()

            if result == curses.KEY_UP:
                self.choosen_option = (self.choosen_option - 1 + 2) % 2
            elif result == curses.KEY_DOWN:
                self.choosen_option = (self.choosen_option + 1) % 2
            elif result in [curses.KEY_ENTER, 10, 13, 108, 109]:
                return self.options[self.choosen_option]