import curses


class RegisterForm:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def get_register_data(self):
        self.stdscr.clear()
        curses.curs_set(True)
        curses.echo()

        self.stdscr.addstr(2, 2, 'Email address:')
        email_address = self.stdscr.getstr(3, 2, 16).decode('utf-8').strip()

        curses.noecho()
        return email_address