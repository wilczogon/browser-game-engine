from browser_game_engine import EngineModule, socketio, error_handling, app, db
import logging
import json
from flask import request
from .character_to_connection import CharacterToConnection
from browser_game_engine.characters import Character
from flask_socketio import emit, join_room


class ChatModule(EngineModule):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def add_endpoints(self):
        for conn in CharacterToConnection.query.all():
            db.session.delete(conn)
        db.session.commit()

        @app.route(self.engine.root_path + "/characters/<character_id>/connect", methods=['POST'])
        @error_handling
        @self.engine.users.auth
        @self.engine.characters.get_and_validate_character
        def connect(user, character):
            data = json.loads(request.get_data())
            sid = data['sid'] # TODO what if incorrect data

            conn = CharacterToConnection(character_id=character.id, sid=sid)
            db.session.add(conn) # TODO what if already exists
            db.session.commit()

            return 'Connected.'

        @socketio.on_error_default  # handles all namespaces without an explicit error handler
        def default_error_handler(e):
            self._logger.error(e)

        @socketio.on('connect')
        def connect():
            join_room(request.sid)
            self._logger.info('Connected character with sid={}.'.format(request.sid))

        @socketio.on('disconnect')
        @self.get_character_for_connection
        def disconnect(character, conn):
            db.session.delete(conn)
            db.session.commit()
            self._logger.info('{} disconnected with sid={}.'.format(character.name, request.sid))

        @socketio.on('location_message')
        @self.get_character_for_connection
        def handle_message(character, conn, message):
            characters_in_location = Character.query.filter_by(location=character.location).all()
            conns = CharacterToConnection.query.filter(CharacterToConnection.character_id.in_([c.id for c in characters_in_location])).all()
            for conn in conns:
                emit('location_message', {'sender': character.name, 'message': message}, room=conn.sid)

    def get_character_for_connection(self, func):
        def call(*args, **kwargs):
            conn = CharacterToConnection.query.filter_by(sid=request.sid).first()  # TODO check if exists
            character = Character.query.filter_by(id=conn.character_id).first()
            return func(character, conn, *args, **kwargs)
        return call
