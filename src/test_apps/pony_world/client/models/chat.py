import curses


class Chat:
    def __init__(self, stdscr, chat_win):
        self.stdscr = stdscr
        chat_win_y, chat_win_x = chat_win.getmaxyx()
        self.chat_win = chat_win.derwin(chat_win_y - 2, chat_win_x, 0, 0)
        self.input_win = chat_win.derwin(3, chat_win_x, chat_win_y - 3, 0)
        self.message = ''
        self.chat_content = []

    def draw(self):
        self.chat_win.border(0, 0, 0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE)
        self.input_win.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)
        self.input_win.addstr(1, 2, "Click '/' to switch between menus and chat")

    def chat_input(self):
        curses.curs_set(True)
        self.input_win.clear()
        self.input_win.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)
        self.input_win.addstr(1, 2, self.message)
        self.input_win.refresh()

        while True:
            y, x = self.input_win.getbegyx()
            self.stdscr.move(y+1, x+2+len(self.message))

            key = self.stdscr.getch()

            if key == ord('/'):
                curses.curs_set(False)
                break
            elif key in [curses.KEY_ENTER, 10, 13]:
                # TODO send message
                self.message = ''
                self.input_win.addstr(1, 2, "Click '/' to switch between menus and chat")
                self.input_win.refresh()
                curses.curs_set(False)
                break
            elif key >= 0 and key < 256:
                self.message += chr(key)
                self.input_win.clear()
                self.input_win.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)
                self.input_win.addstr(1, 2, self.message)
                self.input_win.refresh()

    def add_message(self, msg):
        self.chat_content.append(msg)

        elements_to_show = self.chat_content
        y, x = self.chat_win.getmaxyx()
        if len(elements_to_show) > y-2:
            elements_to_show = elements_to_show[len(elements_to_show) + 2 - y:]
        self.chat_win.clear()
        self.chat_win.border(0, 0, 0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE)
        for i, el in enumerate(elements_to_show):
            self.chat_win.addstr(i + 1, 2, el)

        self.chat_win.refresh()
