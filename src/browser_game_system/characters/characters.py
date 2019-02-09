from browser_game_system import SystemModule, app, db, error_handling, BadRequest, Unauthorized
from .character_states import CharacterStates
from flask import jsonify, request
import json


class Characters(SystemModule):
    def __init__(self, character_class, create_character_func):
        self.character_class = character_class
        self.create_character_func = create_character_func

    def add_endpoints(self):
        @app.route(self.system.root_path + "/characters")
        @error_handling
        @self.system.users.auth
        def get_characters(user):
            db.session.commit()
            return jsonify({'characters': [character.get_public_json() for character in self.character_class.query.all()]})

        def _get_character(user, character_id):
            db.session.commit()
            character = self.character_class.query.filter_by(id=character_id).first()

            if character.user_id == user.id:
                return jsonify(character.get_protected_json())
            else:
                return jsonify(character.get_public_json())

        @app.route(self.system.root_path + "/characters/<int:character_id>")
        @error_handling
        @self.system.users.auth
        def get_character(user, character_id):
            return _get_character(user, character_id)

        @app.route(self.system.root_path + "/characters", methods=['POST'])
        @error_handling
        @self.system.users.auth
        def create_character(user):
            data = json.loads(request.get_data())

            last_character = self.character_class.query.filter_by(id=user.last_character_id).first()
            if last_character is not None and last_character.state == CharacterStates.ALIVE:
                raise BadRequest('Character for this user is still alive.')

            characters = self.character_class.query.filter_by(name=data['name'], state=CharacterStates.ALIVE).all()
            if len(characters) > 0:
                raise BadRequest('Character with name \'{}\' already exists.'.format(data['name']))

            character = self.create_character_func(user, **data)
            db.session.add(character)
            db.session.commit()
            user.last_character_id = character.id
            db.session.commit()

            return _get_character(user, character.id)

        @app.route(self.system.root_path + "/characters/<int:character_id>", methods=['PATCH'])
        @error_handling
        @self.system.users.auth
        def update_character(user, character_id):
            if user.last_character_id != character_id:
                raise Unauthorized('Cannot modify character.')

            character = self.character_class.query.filter_by(id=character_id).first()

            data = json.loads(request.get_data())

            if 'location' in data:
                self.system.travelling.travel(character, data['location'])

            return _get_character(user, character_id)
