from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

db = SQLAlchemy()
app = Flask(__name__)
socketio = SocketIO(app)


class Engine:
    def __init__(self, db_uri, websocket_secret, root_path, scheduler, users, characters, travelling, exploration, items, crafting):
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SECRET_KEY'] = 'websocket_secret'
        db.init_app(app)
        self.push_context()

        self.db_uri = db_uri
        self.root_path = root_path

        self.scheduler = scheduler
        self.scheduler.set_engine(self)

        self.users = users
        self.users.set_engine(self)

        self.characters = characters
        self.characters.set_engine(self)

        self.travelling = travelling
        self.travelling.set_engine(self)

        self.exploration = exploration
        self.exploration.set_engine(self)

        self.items = items
        self.items.set_engine(self)
        
        self.crafting = crafting
        self.crafting.set_engine(self)

    def push_context(self):
        app.app_context().push()

    def run(self):
        socketio.run(app)  # TODO prod run: host='0.0.0.0'
