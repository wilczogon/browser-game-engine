class ItemOccurrence:
    def __init__(self, item_id, appearance_rate, max_amount_per_search=1):
        self.item_id = item_id
        self.appearance_rate = appearance_rate
        self.max_amount_per_search = max_amount_per_search


class ExplorationAreaDefinition:
    def __init__(self, id, name, item_occurances, cost):
        self.id = id
        self.name = name
        self.item_occurances = item_occurances
        self.cost = cost


class LocationsToExplorationAreasMapping:
    def __init__(self, location_id, exploration_area_ids):
        self.location_id = location_id
        self.exploration_area_ids = exploration_area_ids
