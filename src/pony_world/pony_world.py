import requests
import sys
import base64

url = 'http://127.0.0.1:5000'
root_path = '/v1/pony_world'
headers = {}
character_id = None


def handle_result(result):
    if result.status_code != 200:
        raise Exception(result.text)


def login(email_address):
    encoded = base64.b64encode('{}:{}'.format(email_address, 'todo').encode('utf-8'))
    headers['Authorization'] = 'Basic {}'.format(encoded.decode("utf-8"))
    result = requests.post('{}{}/users/login'.format(url, root_path), headers=headers)
    handle_result(result)
    global character_id
    character_id = result.json()['last_character_id']


def register(email_address):
    result = requests.post('{}{}/users'.format(url, root_path), json={'email_address': email_address})
    handle_result(result)
    login(email_address)


def logout():
    result = requests.post('{}{}/users/logout'.format(url, root_path), headers=headers)
    handle_result(result)


def create_character(name, species):
    result = requests.post('{}{}/characters'.format(url, root_path), json={'name': name, 'species': species}, headers=headers)
    handle_result(result)
    global character_id
    character_id = result.json()['id']


def get_character_info():
    result = requests.get('{}{}/characters/{}'.format(url, root_path, character_id), headers=headers)
    handle_result(result)
    return result.json()


def explore():
    result = requests.post(
        '{}{}/characters/{}/explore/forest'.format(url, root_path, character_id),
        headers=headers
    )
    handle_result(result)


def travel(destination):
    result = requests.patch(
        '{}{}/characters/{}'.format(url, root_path, character_id),
        json={'location': destination},
        headers=headers
    )
    handle_result(result)


def game_loop():
    while True:
        print('')
        print('1) Character info')
        print('2) Location info')
        print('3) Explore')
        print('4) Travel')
        print('5) Logout')
        choice = int(input('>> '))

        try:
            if choice == 1:
                character_info = get_character_info()
                longest_key = max([len(key) for key in character_info])
                print('\nCharacter Info')
                print('--------------')
                for info in character_info.items():
                    print('{}{}: {}'.format(' '*(longest_key - len(info[0])), info[0], info[1]))
            elif choice == 2:
                pass
            elif choice == 3:
                explore()
            elif choice == 4:
                character_info = get_character_info()
                print('Destination:')
                c = 1
                for conn in character_info['connected_paths']:
                    print('{}) {}'.format(c, conn['location_name']))
                    c += 1
                choice = int(input('>> '))
                conn = character_info['connected_paths'][choice-1]
                destination = conn['location_id']
                travel(destination)
            elif choice == 5:
                logout()
                sys.exit()
        except Exception as e:
            print("Error occured: ", e)


print('Welcome to')
print('''  ____                    __        __         _     _ 
 |  _ \ ___  _ __  _   _  \ \      / /__  _ __| | __| |
 | |_) / _ \| '_ \| | | |  \ \ /\ / / _ \| '__| |/ _` |
 |  __/ (_) | | | | |_| |   \ V  V / (_) | |  | | (_| |
 |_|   \___/|_| |_|\__, |    \_/\_/ \___/|_|  |_|\__,_|
                   |___/                              
''')

print('1) login')
print('2) register')

choice = int(input(">> "))

if choice == 1:
    email_address = input('Email address: ')
    login(email_address)
elif choice == 2:
    email_address = input('Email address: ')
    register(email_address)
    print('Great, you were successfully registered.')
    print('Let\'s prepare you ingame character now.')
    character_name = input('Character name: ')
    print('Character species:')
    print('1) Pony')
    print('2) Unicorn Pony')
    print('3) Pegasus Pony')
    choice = int(input(">> "))
    species = {
        1: 'pony',
        2: 'unicorn_pony',
        3: 'pegasus_pony'
    }[choice]
    create_character(character_name, species)
    print('You\'re character was successfully created.')
else:
    print('Invalid command.')
    sys.exit()

game_loop()
