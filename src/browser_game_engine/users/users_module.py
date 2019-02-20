from browser_game_engine import EngineModule, app, Unauthorized, error_handling, ApiError, BadRequest
from .models import UserStates
from .models import UserRoles
import json
from flask import request, jsonify
from functools import wraps


class UsersModule(EngineModule):
    def __init__(self, user_class, register, login, logout, authenticate):
        self.user_class = user_class
        self.register = register
        self.login = login
        self.logout = logout

        def authenticate2(func):
            def call(username, password):
                user = func(username, password)
                if user.state != UserStates.ACTIVE:
                    raise Unauthorized('Inactive user.')
                return user
            return call

        self.authenticate = authenticate2(authenticate)

    def add_endpoints(self):
        def _get_user(user, user_id):
            if user.id != user_id:
                raise Unauthorized('You are not authorized to get other users info.')
            return jsonify(user.to_json())

        @app.route(self.engine.root_path + "/users/<int:user_id>")
        @error_handling
        @self.auth
        def get_user(user, user_id):
            return _get_user(user, user_id)

        @app.route(self.engine.root_path + "/users", methods=['POST'])
        @error_handling
        def register():
            data = json.loads(request.get_data())
            self.register(**data)

            return 'Successfully registered user.'

        @app.route(self.engine.root_path + "/users/login", methods=['POST']) # auth..?
        @error_handling
        def login():
            try:
                req_auth = request.authorization
            except Exception as e:
                raise Unauthorized('No authorization token provided.')

            if req_auth is None:
                raise Unauthorized('No authorization token provided')

            user = self.login(req_auth.username, req_auth.password)
            return _get_user(user, user.id)

        @app.route(self.engine.root_path + "/users/logout", methods=['POST'])
        @error_handling
        @self.auth
        def logout(user):
            self.logout(user)
            return 'Successfully logged out.'

    def auth(self, func):
        @wraps(func)
        def call(*args, **kwargs):
            try:
                req_auth = request.authorization
            except Exception as e:
                raise Unauthorized('No authorization token provided.')

            if req_auth is None:
                raise Unauthorized('No authorization token provided')

            return func(self.authenticate(req_auth.username, req_auth.password), *args, **kwargs)
        return call

    def admin_auth(self, func):
        @wraps(func)
        def call(*args, **kwargs):
            def prepared_func(user, *args, **kwargs):
                if user.role == UserRoles.REGULAR:
                    raise Unauthorized('Not for you, little guy.')

                return func(user, *args, **kwargs)

            return self.auth(prepared_func)(*args, **kwargs)
        return call
