from sqlalchemy import Column, Integer, String
from browser_game_system.system_db import db


class UserToItem(db.Model):
    __tablename__ = 'users_to_items'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    item_id = Column(String(32))
    item_amount = Column(Integer)

    # def __repr__(self):
    #     return "<UserToItem(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)