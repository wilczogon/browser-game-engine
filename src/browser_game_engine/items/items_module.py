import json
from flask import request, jsonify
from browser_game_engine import SystemModule, BadRequest, db, error_handling, app
from .character_to_item import CharacterToItem
from .models import ItemCategory
from sqlalchemy import and_


class ItemsModule(SystemModule):
    def __init__(self, items_definitions):
        self.items_definitions = items_definitions
        self.items_definitions_lookup = {i.id: i for i in items_definitions}

    def add_endpoints(self):
        @app.route(self.system.root_path + "/characters/<character_id>/eat", methods=['POST'])
        @error_handling
        @self.system.users.auth
        @self.system.characters.get_and_validate_character
        def eat(user, character):
            data = json.loads(request.get_data())

            item_id = data['item_id']
            amount = data['amount']

            item_definition = self.items_definitions_lookup[item_id]
            if item_definition.category != ItemCategory.CONSUMABLE:
                raise BadRequest('Item is not consumable.')

            self.check_amount(character, item_id, amount)
            self.remove_item(character, item_id, amount)

            for stat in item_definition.modifications:
                character.__setattr__(stat, self.system.characters.character_class.__dict__[stat] + item_definition.modifications[stat])
                db.session.commit()
                character_cls = self.system.characters.character_class
                character_cls.query.filter(and_(character_cls.id == character.id, character_cls.__dict__[stat] > character_cls.__dict__["max_" + stat])).update({stat: character.__getattribute__("max_" + stat)})

            db.session.commit()

            return jsonify(self.system.characters.get_character_json(user, character.id))

    def get_items_json(self, character):
        items_recs = CharacterToItem.query.filter_by(character_id=character.id).all()
        return [{'amount': item_rec.item_amount, **self.items_definitions_lookup[item_rec.item_id].to_json()} for item_rec in items_recs]

    def add_item(self, character, item_id, amount):
        if amount <= 0:
            raise BadRequest('Amount of items cannot be less than 1.')

        character_to_item = CharacterToItem.query.filter_by(character_id=character.id, item_id=item_id).first()

        if character_to_item is None:
            db.session.add(CharacterToItem(character_id=character.id, item_id=item_id, item_amount=amount))
        else:
            character_to_item.item_amount = CharacterToItem.item_amount + amount

        db.session.commit()

    def remove_item(self, character, item_id, amount):
        if amount <= 0:
            raise BadRequest('Amount of items to remove cannot be less than 1.')

        character_to_item = CharacterToItem.query.filter_by(character_id=character.id, item_id=item_id).first()

        if character_to_item is None:
            raise BadRequest('No items found to remove.')
        elif character_to_item.item_amount < amount:
            raise BadRequest('Not enough items to remove all needed.')
        elif character_to_item.item_amount > amount:
            character_to_item.item_amount = CharacterToItem.item_amount - amount
            db.session.commit()
        else:
            db.session.delete(character_to_item)
            db.session.commit()

    def check_amount(self, character, item_id, amount):
        character_to_item = CharacterToItem.query.filter_by(character_id=character.id, item_id=item_id).first()

        if character_to_item is None:
            raise BadRequest('Not enough items.')
        else:
            if character_to_item.item_amount < amount:
                raise BadRequest('Not enough items.')
