import curses


class GameLayout:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def create_windows(self):
        self.stdscr.clear()

        row_1_lines = int(curses.LINES * 0.7)
        col_1_cols = int(curses.COLS * 0.6)
        menu_win = self.stdscr.subwin(row_1_lines, col_1_cols, 0, 0)
        info_win = self.stdscr.subwin(row_1_lines, curses.COLS - col_1_cols, 0, col_1_cols)
        chat_win = self.stdscr.subwin(curses.LINES - row_1_lines, curses.COLS, row_1_lines, 0)

        return menu_win, info_win, chat_win