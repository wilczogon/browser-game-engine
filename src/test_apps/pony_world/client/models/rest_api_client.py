import requests
import base64


class RestApiClient:
    root_path = '/v1/pony_world'

    def __init__(self, url):
        self.url = url
        self.headers = {}
        self.character_id = None

    @staticmethod
    def handle_result(result):
        if result.status_code != 200:
            raise Exception(result.text)

    def login(self, email_address):
        encoded = base64.b64encode('{}:{}'.format(email_address, 'todo').encode('utf-8'))
        self.headers['Authorization'] = 'Basic {}'.format(encoded.decode("utf-8"))
        result = requests.post('{}{}/users/login'.format(self.url, self.root_path), headers=self.headers)
        self.handle_result(result)
        self.character_id = result.json()['last_character_id']
        return self.character_id

    def register(self, email_address):
        result = requests.post('{}{}/users'.format(self.url, self.root_path), json={'email_address': email_address})
        self.handle_result(result)
        self.login(email_address)

    def logout(self):
        result = requests.post('{}{}/users/logout'.format(self.url, self.root_path), headers=self.headers)
        self.handle_result(result)

    def connect(self, sid):
        result = requests.post(
            '{}{}/characters/{}/connect'.format(self.url, self.root_path, self.character_id),
            json={'sid': sid},
            headers=self.headers
        )
        self.handle_result(result)

    def create_character(self, name, species):
        result = requests.post('{}{}/characters'.format(self.url, self.root_path), json={'name': name, 'species': species}, headers=self.headers)
        self.handle_result(result)
        self.character_id = result.json()['id']

    def get_character_info(self):
        result = requests.get('{}{}/characters/{}'.format(self.url, self.root_path, self.character_id), headers=self.headers)
        self.handle_result(result)
        return result.json()

    def eat(self, item_id, amount):
        result = requests.post('{}{}/characters/{}/eat'.format(self.url, self.root_path, self.character_id), json={'item_id': item_id, 'amount': amount}, headers=self.headers)
        self.handle_result(result)
        return result.json()

    def explore(self, area_id):
        result = requests.post(
            '{}{}/characters/{}/explore/{}'.format(self.url, self.root_path, self.character_id, area_id),
            headers=self.headers
        )
        self.handle_result(result)
        return result.json()

    def travel(self, destination):
        result = requests.patch(
            '{}{}/characters/{}'.format(self.url, self.root_path, self.character_id),
            json={'location': destination},
            headers=self.headers
        )
        self.handle_result(result)
        return result