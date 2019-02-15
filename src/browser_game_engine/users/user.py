from sqlalchemy import Column, Integer, String, DateTime
from browser_game_engine import db, generate_uuid
import datetime
from .user_states import UserStates
from .user_roles import UserRoles


class User(db.Model):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email_address = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    role = Column(String(16), default=UserRoles.REGULAR)
    state = Column(String(16), default=UserStates.ACTIVE)
    last_character_id = Column(String(36))

    def to_json(self):
        return {k: self.__dict__[k] for k in [key for key in self.__dict__ if not key.startswith('_')]}
