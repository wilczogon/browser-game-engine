from browser_game_engine import SystemModule


class ExplorationModule(SystemModule):
    def __init__(self, area_definitions, mappings):
        self.area_definitions = area_definitions
        self.mappings = mappings
