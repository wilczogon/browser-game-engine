from sqlalchemy import Column, Integer, String
from browser_game_engine.engine_imports import db


class CharacterToItem(db.Model):
    __tablename__ = 'characters_to_items'

    character_id = Column(String(36), primary_key=True)
    item_id = Column(String(32), primary_key=True)
    item_amount = Column(Integer)

    # def __repr__(self):
    #     return "<UserToItem(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)