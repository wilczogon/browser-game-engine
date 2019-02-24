from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

db = SQLAlchemy()
app = Flask(__name__)
socketio = SocketIO(app)


class Engine:
    def __init__(self, db_uri, websocket_secret, root_path, scheduler, chat, users, characters, travelling, exploration, items, crafting):
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SECRET_KEY'] = websocket_secret
        db.init_app(app)
        self.push_context()

        self.db_uri = db_uri
        self.root_path = root_path

        self.scheduler = scheduler
        self.chat = chat
        self.users = users
        self.characters = characters
        self.travelling = travelling
        self.exploration = exploration
        self.items = items
        self.crafting = crafting

        self.scheduler.set_engine(self)
        self.chat.set_engine(self)
        self.users.set_engine(self)
        self.characters.set_engine(self)
        self.travelling.set_engine(self)
        self.exploration.set_engine(self)
        self.items.set_engine(self)
        self.crafting.set_engine(self)

    def push_context(self):
        app.app_context().push()

    def run(self):
        socketio.run(app)  # TODO prod run: host='0.0.0.0'
