class LocationDefinition:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_json(self, system, character):
        obj = dict(self.__dict__.items())
        obj['exploration_areas'] = system.exploration.get_exploration_areas_json(character)

        return obj
