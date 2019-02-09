from browser_game_system.system_module import SystemModule


class CraftingSystem(SystemModule):
    def __init__(self, recipe_descriptions):
        self.recipe_descriptions = recipe_descriptions

    def craft(self, ingredients):
        pass