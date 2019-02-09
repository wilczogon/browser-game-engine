from browser_game_system import db, BadRequest


class Cost:
    def __init__(self, item_cost=None, **other_costs):
        self.item_cost = item_cost
        self.other_costs = other_costs

    def check(self, character):
        # TODO item cost

        for parameter_name in self.other_costs:
            if character.__dict__[parameter_name] < self.other_costs[parameter_name]:
                raise BadRequest('Cannot pay cost')

    def pay(self, character):
        self.check(character)

        # TODO item cost & time cost

        for parameter_name in self.other_costs:
            character.__setattr__(parameter_name, character.__class__.__dict__[parameter_name] - self.other_costs[parameter_name])

        db.session.commit()
