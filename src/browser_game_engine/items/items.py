from browser_game_engine import SystemModule, BadRequest, db
from .character_to_item import CharacterToItem


class Items(SystemModule):
    def __init__(self, items_definitions):
        self.items_definitions = items_definitions
        self.items_definitions_lookup = {i.id: i for i in items_definitions}

    def get_items_json(self, character):
        items_recs = CharacterToItem.query.filter_by(character_id=character.id).all()
        return [{'amount': item_rec.amount, **self.items_definitions_lookup[item_rec.id].to_json()} for item_rec in items_recs]

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
        else:
            if character_to_item.item_amount < amount:
                raise BadRequest('Not enough items to remove all needed.')

            character_to_item.item_amount = CharacterToItem.item_amount - amount
            db.session.commit()

    def check_amount(self, character, item_id, amount):
        character_to_item = CharacterToItem.query.filter_by(character_id=character.id, item_id=item_id).first()

        if character_to_item is None:
            raise BadRequest('Not enough items.')
        else:
            if character_to_item.item_amount < amount:
                raise BadRequest('Not enough items.')
