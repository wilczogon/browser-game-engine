from browser_game_engine.engine_module import EngineModule


class CraftingModule(EngineModule):
    def __init__(self, recipe_descriptions):
        self.recipe_descriptions = recipe_descriptions

    def craft(self, ingredients):
        pass