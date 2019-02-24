from sqlalchemy import Column, String, DateTime
from browser_game_engine import db
import datetime


class CharacterToConnection(db.Model):
    __tablename__ = 'characters_to_connections'

    character_id = Column(String(36), primary_key=True)
    sid = Column(String(32))
    connected_at = Column(DateTime, default=datetime.datetime.utcnow)