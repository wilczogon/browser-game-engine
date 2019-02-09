from sqlalchemy import Column, Integer, String, DateTime
from browser_game_system.system_db import db
import datetime
from .user_states import UserStates
from .user_roles import UserRoles


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email_address = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    role = Column(String(16), default=UserRoles.REGULAR)
    state = Column(String(16), default=UserStates.ACTIVE)
    last_character_id = Column(Integer)

    def to_json(self):
        return {k: self.__dict__[k] for k in [key for key in self.__dict__ if not key.startswith('_')]}
