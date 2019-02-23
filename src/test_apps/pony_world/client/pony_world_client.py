from curses import wrapper
from models import *

client = RestApiClient('http://127.0.0.1:5000')


def show_item_info(info_win, item_info):
    info_win.clear()
    info_win.box()
    info_lines = [
        ' Item name: {}'.format(item_info['name']),
        '  Category: {}'.format(item_info['category']),
        '    Amount: {}'.format(item_info['amount']),
        '    Rarity: {}'.format(item_info['rarity']),
        'Shop price: {}'.format(item_info['shop_price'])
    ]
    draw_on_center(info_win, info_lines)
    info_win.refresh()


def item_menu_loop(stdscr, menu_win, info_win, chat, item_info):
    while True:
        menu_win.clear()
        menu_win.box()
        menu = GameMenu(stdscr, menu_win, ['eat', 'back'],
                        {'eat': 'Eat', 'back': 'Back'}, chat)

        answer = menu.get_answer()

        if answer == 'eat':
            character_info = client.eat(item_info['id'], 1)
            item_info = [i for i in character_info['items'] if i['id'] == item_info['id']][0]
            show_item_info(info_win, item_info)
        elif answer == 'back':
            break


def inventory_menu_loop(stdscr, menu_win, info_win, chat):
    character_info = client.get_character_info()
    while True:
        menu_win.clear()
        menu_win.box()
        menu = GameMenu(stdscr, menu_win, [i['id'] for i in character_info['items']] + ['back'], {**{i['id']: '{} x{}'.format(i['name'], i['amount']) for i in character_info['items']}, 'back': 'Back'}, chat)

        answer = menu.get_answer()

        if answer == 'back':
            break
        else:
            item_info = [i for i in character_info['items'] if i['id'] == answer][0]
            show_item_info(info_win, item_info)
            item_menu_loop(stdscr, menu_win, info_win, chat, item_info)


def character_menu_loop(stdscr, menu_win, info_win, chat):
    while True:
        menu_win.clear()
        menu_win.box()
        menu = GameMenu(stdscr, menu_win, ['info', 'items', 'back'], {
            'info': 'Character Info',
            'items': 'Inventory',
            'back': 'Back'
        }, chat)

        answer = menu.get_answer()

        if answer == 'info':
            info_win.clear()
            info_win.box()
            info = client.get_character_info()
            info_lines = [
                'Character name: {}'.format(info['name']),
                '       Species: {}'.format(info['species']),
                '        Energy: {}'.format(info['energy']),
                ' Action points: {}'. format(info['action_points'])
            ]
            draw_on_center(info_win, info_lines)
            info_win.refresh()
        elif answer == 'items':
            inventory_menu_loop(stdscr, menu_win, info_win, chat)
        elif answer == 'back':
            break


def exploration_menu_loop(stdscr, menu_win, info_win, chat, character_info):
    while True:
        menu_win.clear()
        menu_win.box()
        menu = GameMenu(stdscr, menu_win, [a['id'] for a in character_info['location']['exploration_areas']] + ['back'],
                        {**{a['id']:a['name'] for a in character_info['location']['exploration_areas']}, 'back': 'Back'}, chat)

        answer = menu.get_answer()

        if answer == 'back':
            break
        else:
            result = client.explore(answer)
            info_win.clear()
            info_win.box()

            if len(result['found_items']) == 0:
                info_lines = ['Nothing found.']
            else:
                info_lines = [
                    'Found:',
                    *['    - {} x{}'.format(i['name'], i['amount']) for i in result['found_items']]
                ]
            draw_on_center(info_win, info_lines)
            info_win.refresh()


def show_location_info(info_win, character_info):
    info_win.clear()
    info_win.box()
    info_lines = [
        '      Location name: {}'.format(character_info['location']['name']),
        '',
        '  Exploration areas:',
        *['            - ' + p['name'] for p in character_info['location']['exploration_areas']],
        '',
        'Connected locations:',
        *['            - ' + p['location_name'] for p in character_info['connected_paths']]
    ]
    draw_on_center(info_win, info_lines)
    info_win.refresh()


def travelling_menu_loop(stdscr, menu_win, info_win, chat, character_info):
    while True:
        menu_win.clear()
        menu_win.box()
        menu = GameMenu(stdscr, menu_win, [p['location_id'] for p in character_info['connected_paths']] + ['back'],
                        {**{p['location_id']: p['location_name'] for p in character_info['connected_paths']}, 'back': 'Back'}, chat)

        answer = menu.get_answer()

        if answer == 'back':
            break
        else:
            result = client.travel(answer)
            show_location_info(info_win, result)


def location_menu_loop(stdscr, menu_win, info_win, chat):
    info = client.get_character_info()
    show_location_info(info_win, info)

    while True:
        menu_win.clear()
        menu_win.box()
        menu = GameMenu(stdscr, menu_win, ['explore', 'travel', 'back'], {
            'explore': 'Explore',
            'travel': 'Travel',
            'back': 'Back'
        }, chat)

        answer = menu.get_answer()

        if answer == 'explore':
            exploration_menu_loop(stdscr, menu_win, info_win, chat, info)
        elif answer == 'travel':
            travelling_menu_loop(stdscr, menu_win, info_win, chat, info)
        elif answer == 'back':
            break


def main_menu_loop(stdscr, menu_win, info_win, chat):
    while True:
        menu_win.clear()
        menu_win.box()
        menu = GameMenu(stdscr, menu_win, ['character', 'location', 'exit'], {
            'character': 'Character',
            'location': 'Location',
            'exit': 'Exit'
        }, chat)

        answer = menu.get_answer()

        if answer == 'character':
            character_menu_loop(stdscr, menu_win, info_win, chat)
        elif answer == 'location':
            location_menu_loop(stdscr, menu_win, info_win, chat)
        elif answer == 'exit':
            client.logout()
            break

def main(stdscr):
    # Clear screen
    intro = IntroMenu(stdscr, 'Pony World', 'standard')
    result = intro.get_answer()

    if result == 'login':
        form = LoginForm(stdscr)
        email_address = form.get_login_data()
        character_id = client.login(email_address)

        if character_id is None:
            pass # TODO character creation

    else:
        form = RegisterForm(stdscr)
        email_address = form.get_register_data()
        client.register(email_address)

        # TODO character creation

    curses.curs_set(False)
    menu_win, info_win, chat_win = GameLayout(stdscr).create_windows()
    chat = Chat(stdscr, chat_win)
    chat.draw()
    main_menu_loop(stdscr, menu_win, info_win, chat)

wrapper(main)


#   action_points: 16.7002
# connected_paths: [{'cost': {'action_points': 10}, 'location_id': 'ponyland_woods', 'location_name': 'Ponyland Woods'}]
#      created_at: Sat, 16 Feb 2019 12:06:51 GMT
#          energy: 18.0
#              id: e6e9c652-7b60-4aff-a6e7-85866b35be7e
#           items: [{'amount': 6, 'category': 'consumable', 'id': 'strawberry', 'modifications': {'energy': 1}, 'name': 'Strawberry', 'rarity': 0, 'shop_price': 1}]
#        location: {'exploration_areas': [], 'id': 'ponyland_kindergarden', 'name': 'Ponyland Kindergarden'}
#            name: Crafter
#         species: unicorn_pony
#           state: alive
#        strength: 1