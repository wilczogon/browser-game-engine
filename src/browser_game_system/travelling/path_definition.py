class PathDefinition:
    def __init__(self, location_id_1, location_id_2, cost, two_way_relation=True, visibility_condition=None):
        self.location_id_1 = location_id_1
        self.location_id_2 = location_id_2
        self.cost = cost
        self.two_way_relation = two_way_relation
        self.visibility_condition = visibility_condition
