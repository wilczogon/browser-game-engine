from browser_game_engine import SystemModule, BadRequest
from browser_game_engine.system_db import db


class TravellingModule(SystemModule):
    def __init__(self, locations_definitions, paths_definitions):
        self.locations_definitions = locations_definitions
        self.location_lookup = {location.id: location for location in locations_definitions}
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

    def get_connected_paths(self, character):
        source_id = character.location

        return list([path_definition for path_definition in self.paths_definitions if
         path_definition.location_id_1 == source_id and
                      (path_definition.visibility_condition is None or path_definition.visibility_condition(character))] +
        [path_definition for path_definition in self.paths_definitions if
         path_definition.location_id_2 == source_id and path_definition.two_way_relation and
         (path_definition.visibility_condition is None or path_definition.visibility_condition(character))])

    def get_connected_paths_json(self, character):
        paths = self.get_connected_paths(character)

        def get_connected_path_json(path):
            if path.location_id_1 == character.location:
                location_id = path.location_id_2
            elif path.location_id_2 == character.location and path.two_way_relation:
                location_id = path.location_id_1
            else:
                raise Exception('Failure during getting connected location for path: {}.'.format(path))

            location = self.location_lookup[location_id]
            return {'location_id': location.id, 'location_name': location.name, 'cost': path.cost.to_json()}

        return [get_connected_path_json(path) for path in paths]

    def get_path_definition(self, character, destination_id):
        source_id = character.location

        paths = list([path_definition for path_definition in self.paths_definitions if
         path_definition.location_id_1 == source_id and path_definition.location_id_2 == destination_id and
                      (path_definition.visibility_condition is None or path_definition.visibility_condition(character))] +
        [path_definition for path_definition in self.paths_definitions if
         path_definition.location_id_2 == source_id and path_definition.location_id_1 == destination_id
         and path_definition.two_way_relation and
         (path_definition.visibility_condition is None or path_definition.visibility_condition(character))])

        if len(paths) == 0:
            raise BadRequest('No such path.')
        elif len(paths) > 1:
            raise BadRequest('Multiple paths possible.')

        return paths[0]

    def travel(self, character, destination_id):
        path_definition = self.get_path_definition(character, destination_id)

        path_definition.cost.pay(character)
        character.location = destination_id
        db.session.commit()
