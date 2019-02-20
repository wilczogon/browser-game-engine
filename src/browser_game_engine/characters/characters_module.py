from browser_game_engine import EngineModule, app, db, error_handling, BadRequest, Unauthorized
from .models import CharacterStates
from flask import jsonify, request
import json
from functools import wraps


class CharactersModule(EngineModule):
    def __init__(self, character_class, create_character_func):
        self.character_class = character_class
        self.create_character_func = create_character_func

    def add_endpoints(self):
        @app.route(self.engine.root_path + "/characters")
        @error_handling
        @self.engine.users.auth
        def get_characters(user):
            db.session.commit()
            return jsonify({'characters': [character.get_public_json(self.engine) for character in self.character_class.query.all()]})

        @app.route(self.engine.root_path + "/characters/<character_id>")
        @error_handling
        @self.engine.users.auth
        def get_character(user, character_id):
            return jsonify(self.get_character_json(user, character_id))

        @app.route(self.engine.root_path + "/characters", methods=['POST'])
        @error_handling
        @self.engine.users.auth
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

            return jsonify(self.get_character_json(user, character.id))

        @app.route(self.engine.root_path + "/characters/<character_id>", methods=['PATCH'])
        @error_handling
        @self.engine.users.auth
        @self.get_and_validate_character
        def update_character(user, character):
            data = json.loads(request.get_data())

            if 'location' in data:
                self.engine.travelling.travel(character, data['location'])

            return jsonify(self.get_character_json(user, character.id))

    def get_character_json(self, user, character_id):
        db.session.commit()
        character = self.character_class.query.filter_by(id=character_id).first()

        if character.user_id == user.id:
            return character.get_protected_json(self.engine)
        else:
            return character.get_public_json(self.engine)

    def get_and_validate_character(self, func):
        @wraps(func)
        def call(user, character_id, *args, **kwargs):
            if user.last_character_id != character_id:
                raise Unauthorized('Cannot modify character.')

            character = self.character_class.query.filter_by(id=character_id).first()

            return func(user, character, *args, **kwargs)
        return call
