from browser_game_engine import SystemModule, BadRequest, InternalServerError, app, error_handling
from flask import jsonify
import random


class ExplorationModule(SystemModule):
    def __init__(self, area_definitions, mappings):
        self.area_definitions = area_definitions
        self.mappings = mappings

    def add_endpoints(self):
        @app.route(self.system.root_path + "/characters/<int:character_id>/explore/<area_public_id>", methods=['POST'])
        @error_handling
        @self.system.users.auth
        def explore(user, character_id, area_public_id): # TODO method for checking character in uri
            character = self.system.characters.character_class.query.filter_by(id=character_id).first()
            self.explore(character, area_public_id)
            return jsonify(self.system.characters.get_character_json(user, character_id))

    def get_areas_for_location(self, character):
        mappings = [m for m in self.mappings if m.location_id == character.location]
        if len(mappings) == 0:
            raise BadRequest('No areas to explore in this location.')
        elif len(mappings) > 1:
            raise InternalServerError('Multiple mappings for single location.')

        areas_ids = mappings[0].exploration_area_ids
        return [a for a in self.area_definitions if a.id in areas_ids]

    def get_exploration_areas_json(self, character):
        areas = self.get_areas_for_location(character)
        return [a.to_json() for a in areas]

    def explore(self, character, public_area_id):
        areas = self.get_areas_for_location(character)
        areas = [a for a in areas if a.public_id == public_area_id]
        if len(areas) == 0:
            raise BadRequest('No area definition for this public_id in this location.')
        elif len(areas) > 1:
            raise BadRequest('Multiple area definitions with the same public_id in this location.')

        area = areas[0]
        area.cost.pay(self.system, character)

        for occurrence in area.item_occurrences:
            amount = 0
            for i in range(occurrence.max_amount_per_search):
                if random.random() <= occurrence.appearance_rate:
                    amount += 1

            if amount > 0:
                self.system.items.add_item(character, occurrence.item_id, amount)
