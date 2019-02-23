from .utils import draw_menu_2
import curses


class GameMenu:
    def __init__(self, stdscr, menu_win, options, labels, chat):
        self.stdscr = stdscr
        self.menu_win = menu_win
        self.options = options
        self.labels = labels
        self.choosen_option = 0
        self.chat = chat

    def get_answer(self):
        while True:
            draw_menu_2(self.menu_win, [self.labels[o] for o in self.options], self.choosen_option)

            self.menu_win.refresh()

            result = self.stdscr.getch()

            if result == curses.KEY_UP:
                self.choosen_option = (self.choosen_option - 1 + len(self.options)) % len(self.options)
            elif result == curses.KEY_DOWN:
                self.choosen_option = (self.choosen_option + 1) % len(self.options)
            elif result in [curses.KEY_ENTER, 10, 13, 108, 109]:
                return self.options[self.choosen_option]
            elif result == ord('/'):
                self.chat.chat_input()