class PathDefinition:
    def __init__(self, location_id_1, location_id_2, cost, two_way_relation=True, visibility_condition=None):
        self.location_id_1 = location_id_1
        self.location_id_2 = location_id_2
        self.cost = cost
        self.two_way_relation = two_way_relation
        self.visibility_condition = visibility_condition


class LocationDefinition:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_json(self, engine, character):
        obj = dict(self.__dict__.items())
        obj['exploration_areas'] = engine.exploration.get_exploration_areas_json(character)

        return obj
