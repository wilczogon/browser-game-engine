class ItemWithAmount:
    def __init__(self, item_definition, amount):
        self.item_definition = item_definition
        self.amount = amount

    def to_json(self):
        return {'amount': self.amount, **self.item_definition.__dict__}