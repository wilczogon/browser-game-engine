from browser_game_engine import Engine, db, Unauthorized, BadRequest
from browser_game_engine.scheduler import Scheduler, Schedule, TaskDefinition
from browser_game_engine.users import UsersModule, User
from browser_game_engine.characters import CharactersModule, Character
from browser_game_engine.travelling import TravellingModule, LocationDefinition, PathDefinition
from browser_game_engine.exploration import ExplorationModule, ItemOccurrence, ExplorationAreaDefinition, LocationsToExplorationAreasMapping
from browser_game_engine.items import ItemsModule, ConsumableItemDefinition, Rarity
from browser_game_engine.crafting import CraftingModule, RecipeDescription
from browser_game_engine.supporting_models import Cost
from sqlalchemy import Column, Integer, String, Float, Boolean


class PonySpecies:
    PONY = 'pony'
    UNICORN_PONY = 'unicorn_pony'
    PEGASUS_PONY = 'pegasus_pony'


class PAUser(User):
    logged = Column(Boolean, default=False)


def register(email_address):
    users = PAUser.query.filter_by(email_address=email_address).all()
    if len(users) > 0:
        raise BadRequest('User with such email address already exists.')

    db.session.add(PAUser(email_address=email_address))
    db.session.commit()


def login(email_address, password):
    user = PAUser.query.filter_by(email_address=email_address).first()
    if user is None:
        raise Unauthorized()

    user.logged = True
    db.session.commit()
    character = Pony.query.filter_by(id=user.last_character_id).first()
    if character is not None:
        if character.energy < 0.1:
            character.location = 'ponyland_kindergarden'
            character.energy = 1
            # TODO set right event
            db.session.commit()
    return user


def logout(user): # TODO automatic log out
    user.logged = False
    db.session.commit()


def authenticate(username, password):
    user = PAUser.query.filter_by(email_address=username).first()
    if user is None:
        raise Unauthorized()

    if not user.logged:
        raise Unauthorized('User is not logged.')

    return user


class Pony(Character):
    _PROTECTED_FIELDS = Character._PROTECTED_FIELDS + ['species', 'strength', 'action_points', 'max_action_points', 'energy', 'max_energy']
    _PRIVATE_FIELDS = Character._PRIVATE_FIELDS + ['species', 'strength', 'action_points', 'max_action_points', 'energy', 'max_energy']

    species = Column(String(16))
    strength = Column(Integer, default=1)
    action_points = Column(Float, default=20)
    max_action_points = 20
    energy = Column(Float, default=20)
    max_energy = 20


def action_points_renewal():
    characters = Pony.query.filter(Pony.action_points < Pony.max_action_points).all()

    for character in characters:
        character.action_points = Pony.action_points + 0.1 # TODO min of this and max_action_points

    db.session.commit()


def action_losing_energy():
    characters = Pony.query.filter(Pony.energy > 0).all()

    for character in characters:
        character.energy = Pony.energy - 0.1 # TODO min of this and max_action_points

    db.session.commit()


def create_character_func(user, **kwargs):
    name = kwargs['name']
    species = kwargs['species']

    if species not in PonySpecies.__dict__.values():
        raise BadRequest('No such pony species: {}.'.format(species))

    return Pony(
        user_id=user.id,
        name=name,
        location='ponyland_kindergarden',
        species=species
    )


engine = Engine(
    'mysql://root:gurotyfi@127.0.0.1/pony_world',
    'secret_key',
    '/v1/pony_world',
    scheduler=Scheduler(
        task_definitions=[
            TaskDefinition('action_points_renewal', action_points_renewal),
            TaskDefinition('action_losing_energy', action_losing_energy)
        ],
        schedules=[
            Schedule('action_points_renewal', 0, interval=60),
            Schedule('action_losing_energy', 0, interval=600)
        ]
    ),
    users=UsersModule(
        user_class=PAUser,
        register=register,
        login=login,
        logout=logout,
        authenticate=authenticate
    ),
    characters=CharactersModule(
        character_class=Pony,
        create_character_func=create_character_func
    ),
    travelling=TravellingModule(
        locations_definitions=[
            LocationDefinition('ponyland_kindergarden', 'Ponyland Kindergarden'),
            LocationDefinition('ponyland_woods', 'Ponyland Woods')
        ],
        paths_definitions=[
            PathDefinition('ponyland_kindergarden', 'ponyland_woods', cost=Cost(action_points=10))
        ]
    ),
    exploration=ExplorationModule(
        area_definitions=[ExplorationAreaDefinition('normal_forest_area', 'forest', 'Forest', [
            ItemOccurrence('strawberry', 0.6, max_amount_per_search=3),
            ItemOccurrence('mushroom', 0.2, max_amount_per_search=2)
        ], Cost(action_points=2))],
        mappings=[
            LocationsToExplorationAreasMapping('ponyland_woods', ['normal_forest_area'])
        ]
    ),
    items=ItemsModule([
        ConsumableItemDefinition('apple', 'Apple', Rarity.COMMON, 2, energy=2),
        ConsumableItemDefinition('apple_juice', 'Apple Juice', Rarity.UNCOMMON, 6, energy=5),
        ConsumableItemDefinition('strawberry', 'Strawberry', Rarity.COMMON, 1, energy=1),
        ConsumableItemDefinition('mushroom', 'Mushroom', Rarity.COMMON, 2, energy=1)
    ]),
    crafting=CraftingModule([
        RecipeDescription(['apple', 'apple'], ['apple_juice'], 2, 0.99)
    ])
)

db.create_all()

engine.run()
