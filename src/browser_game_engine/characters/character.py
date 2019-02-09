from sqlalchemy import Column, Integer, String, DateTime
from browser_game_engine.system_db import db
import datetime
from .character_states import CharacterStates


class Character(db.Model):
    __tablename__ = 'characters'

    _PUBLIC_FIELDS = ['id', 'name', 'created_at', 'state']
    _PROTECTED_FIELDS = ['id', 'name', 'created_at', 'state', 'location', 'connected_paths']
    _PRIVATE_FIELDS = ['id', 'user_id', 'name', 'created_at', 'state', 'location', 'connected_paths']

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    state = Column(String(16), default=CharacterStates.ALIVE)
    location = Column(String(32), nullable=False)

    def _get_json(self, system, fields):  # TODO items?
        cloned = {key: self.__dict__[key] for key in self.__dict__ if not key.startswith('_') and key != 'location'}
        cloned['location'] = system.travelling.location_lookup[self.location].to_json()
        els = list(cloned.items())
        els.append(('connected_paths', system.travelling.get_connected_paths_json(self)))
        return dict(list(filter(lambda x: x[0] in fields, els)))

    def get_public_json(self, system):
        return self._get_json(system, self._PUBLIC_FIELDS)

    def get_protected_json(self, system):
        return self._get_json(system, self._PROTECTED_FIELDS)

    def get_private_json(self, system):
        return self._get_json(system, self._PRIVATE_FIELDS)

    # def __repr__(self):
    #     return "<UserToItem(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)