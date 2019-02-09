from browser_game_system import SystemModule, BadRequest
from browser_game_system.system_db import db


class TravellingModule(SystemModule):
    def __init__(self, locations_definitions, paths_definitions):
        self.locations_definitions = locations_definitions
        self.paths_definitions = paths_definitions

    def add_endpoints(self):
        pass
        # @app.route(self.system.root_path + "/locations")
        # def get_locations():
        #     return jsonify({'locations': [character.get_public_json() for character in self.character_class.query.all()]})
        #
        # @app.route(self.system.root_path + "/characters/<int:character_id>")
        # def get_location_info(location_id):
        #     return jsonify(self.character_class.query.filter_by(id=character_id).first().get_protected_json())

    def get_connection_ids(self, character):
        return [path_definition.location_id_2 for path_definition in self.paths_definitions if
         path_definition.location_id_1 == character.location] + \
        [path_definition.location_id_1 for path_definition in self.paths_definitions if
         path_definition.location_id_2 == character.location and path_definition.two_way_relation]

    def get_connections(self, character):
        ids = self.get_connection_ids(character)
        return [location_definition for location_definition in self.locations_definitions if location_definition.id in ids]

    def get_path_definition(self, source_id, destination_id):
        paths = list([path_definition for path_definition in self.paths_definitions if
         path_definition.location_id_1 == source_id and path_definition.location_id_2 == destination_id] + \
        [path_definition for path_definition in self.paths_definitions if
         path_definition.location_id_2 == source_id and path_definition.location_id_1 == destination_id
         and path_definition.two_way_relation])

        if len(paths) == 0:
            raise BadRequest('No such path.') # TODO additional conditions?
        elif len(paths) > 1:
            raise BadRequest('Multiple paths possible.')

        return paths[0]

    def travel(self, character, destination_id):
        path_definition = self.get_path_definition(character.location, destination_id)

        path_definition.cost.pay(character)
        character.location = destination_id
        db.session.commit()
