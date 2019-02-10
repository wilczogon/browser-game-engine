from browser_game_engine import SystemModule, BadRequest, InternalServerError
import random


class ExplorationModule(SystemModule):
    def __init__(self, area_definitions, mappings):
        self.area_definitions = area_definitions
        self.mappings = mappings

    def add_endpoints(self):
        pass

    def explore(self, character, public_area_id):
        mappings = [m for m in self.mappings if m.location_id == character.location]
        if len(mappings) == 0:
            raise BadRequest('No areas to explore in this location.')
        elif len(mappings) > 1:
            raise InternalServerError('Multiple mappings for single location.')

        areas_ids = mappings[0].exploration_area_ids
        areas = [a for a in self.area_definitions if a.id in areas_ids and a.public_id == public_area_id]
        if len(areas) == 0:
            raise BadRequest('No area definition for this public_id in this location.')
        elif len(areas) > 1:
            raise BadRequest('Multiple area definitions with the same public_id in this location.')

        area = areas[0]
        area.cost.pay(self.system, character)

        for occurrance in area.item_occurrances:
            amount = 0
            for i in range(occurrance.max_amount_per_search):
                if random.random() <= occurrance.appearance_rate:
                    amount += 1

            if amount > 0:
                self.system.items.add_item(character, occurrance.item_id, amount)
