class LocationDefinition:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_json(self):
        return self.__dict__
