import curses


def draw_on_center(win, lines, start_y=None):
    y, x = win.getmaxyx()

    if start_y is None:
        start_y = int((y - len(lines)) / 2)
    start_x = int((x - max([len(o) for o in lines])) / 2)

    for i in range(len(lines)):
        line = lines[i]

        win.addstr(start_y + i, start_x, line)


def draw_menu_2(win, options, choosen_option_no, start_y=None):
    draw_on_center(win, ["> " + o if i == choosen_option_no else "  " + o for i, o in enumerate(options)], start_y)


def draw_menu(win, options):
    y, x = win.getmaxyx()
    start_y = int((y - len(options))/2)
    start_x = int((x - max([len(o) for o in options]))/2)

    for i in range(len(options)):
        option = options[i]
        win.addstr(start_y + i, start_x, option)

    win.refresh()


def draw_window_with_input(y, x, start_y, start_x):
    win = curses.newwin(y, x, start_y, start_x)
    input = win.derwin(y-3, 0)
    win.box()
    input.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)

    return win, input