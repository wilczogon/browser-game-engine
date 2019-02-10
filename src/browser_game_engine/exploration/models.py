class ItemOccurrence:
    def __init__(self, item_id, appearance_rate, max_amount_per_search=1):
        self.item_id = item_id
        self.appearance_rate = appearance_rate
        self.max_amount_per_search = max_amount_per_search


class ExplorationAreaDefinition:
    def __init__(self, id, public_id, name, item_occurrences, cost):
        self.id = id
        self.public_id = public_id
        self.name = name
        self.item_occurrences = item_occurrences
        self.cost = cost

    def to_json(self):
        return {
            'id': self.public_id,
            'name': self.name,
            'cost': self.cost.to_json()
        }


class LocationsToExplorationAreasMapping:
    def __init__(self, location_id, exploration_area_ids):
        self.location_id = location_id
        self.exploration_area_ids = exploration_area_ids
