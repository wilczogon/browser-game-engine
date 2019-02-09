from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)


class System:
    def __init__(self, db_uri, root_path, scheduler, users, characters, travelling, exploration, items, crafting_system):
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        db.init_app(app)
        self.push_context()

        self.db_uri = db_uri
        self.root_path = root_path

        self.scheduler = scheduler
        self.scheduler.set_system(self)

        self.users = users
        self.users.set_system(self)

        self.characters = characters
        self.characters.set_system(self)

        self.travelling = travelling
        self.travelling.set_system(self)

        self.exploration = exploration
        self.exploration.set_system(self)

        self.items = items
        self.items.set_system(self)
        
        self.crafting_system = crafting_system
        self.crafting_system.set_system(self)

    def push_context(self):
        app.app_context().push()

    def run(self):
        app.run()
