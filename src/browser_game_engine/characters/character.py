from sqlalchemy import Column, Integer, String, DateTime
from browser_game_engine import db, generate_uuid
import datetime
from .models import CharacterStates


class Character(db.Model):
    __tablename__ = 'characters'

    _PUBLIC_FIELDS = ['id', 'name', 'created_at', 'state']
    _PROTECTED_FIELDS = ['id', 'name', 'created_at', 'state', 'location', 'connected_paths', 'items']
    _PRIVATE_FIELDS = ['id', 'user_id', 'name', 'created_at', 'state', 'location', 'connected_paths', 'items']

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), nullable=False)
    name = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    state = Column(String(16), default=CharacterStates.ALIVE)
    location = Column(String(32), nullable=False)

    def get_json_attr(self, item):
        return self.__getattribute__(item)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def _get_json(self, engine, fields):
        cloned = {key: self.get_json_attr(key) for key in dir(self) if not key.startswith('_') and key != 'location'}
        cloned['location'] = engine.travelling.location_lookup[self.location].to_json(engine, self)
        els = list(cloned.items())
        els.append(('connected_paths', engine.travelling.get_connected_paths_json(self)))
        els.append(('items', engine.items.get_items_json(self)))
        return dict(list(filter(lambda x: x[0] in fields, els)))

    def get_public_json(self, engine):
        return self._get_json(engine, self._PUBLIC_FIELDS)

    def get_protected_json(self, engine):
        return self._get_json(engine, self._PROTECTED_FIELDS)

    def get_private_json(self, engine):
        return self._get_json(engine, self._PRIVATE_FIELDS)

    # def __repr__(self):
    #     return "<UserToItem(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)