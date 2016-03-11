import sys
sys.path.insert(0, '../')


def if_neutral_planet_available(state):
    return any(state.neutral_planets())

"""
def available(state):
    return any(state.neutral_planets())
"""


def closest_neutral_planet(state):
    #neutral
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_neutral = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)
    weakest_enemy = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)
    us_enemy_dist = weakest_enemy[5] * state.distance(strongest_planet[4], weakest_enemy[4])
    us_neutral_dist = state.distance(strongest_planet[0], weakest_neutral[0])
    #enemy
    state.distance(max(state.my_planets(), key=lambda p: p.num_ships, default=None), min(state.enemy_planets(), \
                                        key=lambda p: p.num_ships, default=None))
    pass


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


# Checks whether a enemy fleet is incoming towards a player planet
def incoming_attack(state):
    sort_enemy_fleet = sorted(state.enemy_fleets(), key=lambda p: p.num_ships)
    enemy_fleet_size = len(sort_enemy_fleet)
    iter_enemy_fleet = iter(sort_enemy_fleet)

    sort_my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    my_planets_size = len(sort_my_planets)
    iter_my_planets = iter(sort_my_planets)

    # enemy_fleet = next(iter_enemy_fleet)
    player_planet = next(iter_my_planets)
    try:
        while True:
            for i in range(enemy_fleet_size):
                enemy_fleet = next(iter_enemy_fleet)
                if enemy_fleet.destination_planet == player_planet:
                    return True
                for j in range(my_planets_size):
                    player_planet = next(iter_my_planets)
                    if enemy_fleet.destination_planet == player_planet:
                        return True
            return False

    except StopIteration:
        return False

    """
    if my_planets_size < 2 and enemy_fleet_size < 1:
        return False
    for i in range(enemy_fleet_size):
        enemy_fleet = next(iter_enemy_fleet)
        for j in range(my_planets_size):
            player_planet = next(iter_my_planets)
            if enemy_fleet.destination_planet == player_planet:
                return True

    return False
    """