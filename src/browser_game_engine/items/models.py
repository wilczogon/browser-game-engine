class ItemCategory:
    CONSUMABLE = 'consumable'
    WEARABLE = 'wearable'
    COLLECTABLE = 'collectable'


class Rarity:
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    VERY_RARE = 3
    MYSTIC_RARE = 4


class ItemDefinition:
    def __init__(self, id, name, category, rarity, shop_price):
        self.id = id
        self.name = name
        self.category = category
        self.rarity = rarity
        self.shop_price = shop_price

    def to_json(self):
        return dict(self.__dict__.items()) # TODO better copying


class ConsumableItemDefinition(ItemDefinition):
    def __init__(self, id, name, rarity, shop_price, **modifications):
        ItemDefinition.__init__(self, id, name, ItemCategory.CONSUMABLE, rarity, shop_price)
        self.modifications = modifications


class WearableItemDefinition(ItemDefinition):
    def __init__(self, id, name, rarity, shop_price, **modifications):
        ItemDefinition.__init__(self, id, name, ItemCategory.WEARABLE, rarity, shop_price)
        self.modifications = modifications


class CollectableItemDefinition(ItemDefinition):
    def __init__(self, id, name, rarity, shop_price):
        ItemDefinition.__init__(self, id, name, ItemCategory.COLLECTABLE, rarity, shop_price)


class ItemWithAmount:
    def __init__(self, item_definition, amount):
        self.item_definition = item_definition
        self.amount = amount

    def to_json(self):
        return {'amount': self.amount, **self.item_definition.__dict__}