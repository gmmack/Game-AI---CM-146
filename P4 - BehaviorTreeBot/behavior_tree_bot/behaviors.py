import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def sort_player_planets(state):
    sort_player_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    iter_player_planets = iter(sort_player_planets)
    return iter_player_planets


def sort_enemy_planets(state):

    e_planets = [planet for planet in state.enemy_planets() if not any(fleet.destination_planet == planet.ID for fleet \
                                                                       in state.my_fleets())]
    e_planets.sort(key=lambda p: p.num_ships)
    return e_planets


def sort_neutral_planets(state):
    n_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    n_planets.sort(key=lambda p: p.num_ships)
    return n_planets


def sort_enemy_fleet(state):
    sort_enemy_fleet = sorted(state.enemy_fleets(), key=lambda p: p.num_ships)
    iter_enemy_fleet = iter(sort_enemy_fleet)
    return iter_enemy_fleet


def attack_weakest_enemy_planet(state):
    #Sort player and enemy planets
    my_planets = sort_player_planets(state)

    enemy_planets = sort_enemy_planets(state)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return False


def attack_weakest_planet(state):
    # Sort player and enemy planets
    my_planets = sort_player_planets(state)
    enemy_planets = sort_enemy_planets(state)
    neutral_planets = sort_neutral_planets(state)

    # Combine neutral and enemy lists
    neutral_and_enemy = neutral_planets + enemy_planets
    target_planets = iter(neutral_and_enemy)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return False


def spread_to_closest_planet(state):
    # Sort player and neutral planets
    my_planets = sort_player_planets(state)
    neutral_planets = sort_neutral_planets(state)

    target_planets = iter(neutral_planets)

    try:
        my_planet = next(my_planets)
        if len(neutral_planets) > 0:
            target_planet = find_closest_planet(state, neutral_planets, my_planet)
        else:
            target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                if len(neutral_planets) > 0:
                    target_planet = find_closest_planet(state, neutral_planets, my_planet)
                else:
                    target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return False


def d_fence(state):
    sort_enemy_fleet = sorted(state.enemy_fleets(), key=lambda p: p.num_ships)
    iter_enemy_fleet = iter(sort_enemy_fleet)

    sort_my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    iter_my_planets = iter(sort_my_planets)

    enemy_fleet = sort_enemy_fleet(state)
    my_planets = sort_player_planets(state)

    avg = sum(strength(planet) for planet in sort_my_planets) / len(sort_my_planets)
    strong_planets = [planet for planet in sort_my_planets if strength(planet) > avg]

    if not my_planets or not enemy_fleet:
        return

    strong_planets = iter(sorted(strong_planets, key=strength, reverse=True))

    try:
        player_planet = next(iter_my_planets)
        strong_planet = next(strong_planets)
        enemy_fleet = next(iter_enemy_fleet)
        while True:
            if enemy_fleet.destination_planet == player_planet:
                need = int(avg - strength(enemy_fleet.destination_planet))
                have = int(strength(strong_planet) - avg)
                if have >= need > 0:
                    issue_order(state, strong_planet.ID, enemy_fleet.destination_planet.ID, need)
                    enemy_fleet = next(iter_enemy_fleet)
                elif have > 0:
                    issue_order(state, strong_planet.ID, enemy_fleet.destination_planet.ID, have)
                    strong_planet = next(strong_planets)
                else:
                    strong_planet = next(strong_planets)

                #issue_order(state, strong_planet.ID, enemy_fleet.destination_planet.ID, need)

    except StopIteration:
        return False


def strength(p):
        return p.num_ships \
               + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == p.ID) \
               - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == p.ID)


def defend_my_planets(state):
    my_planets = [planet for planet in state.my_planets()]
    if not my_planets:
        return

    avg = sum(strength(planet) for planet in my_planets) / len(my_planets)

    weak_planets = [planet for planet in my_planets if strength(planet) < avg]
    strong_planets = [planet for planet in my_planets if strength(planet) > avg]

    if (not weak_planets) or (not strong_planets):
        return

    weak_planets = iter(sorted(weak_planets, key=strength))
    strong_planets = iter(sorted(strong_planets, key=strength, reverse=True))

    try:
        weak_planet = next(weak_planets)
        strong_planet = next(strong_planets)
        while True:
            need = int(avg - strength(weak_planet))
            have = int(strength(strong_planet) - avg)

            if have >= need > 0:
                issue_order(state, strong_planet.ID, weak_planet.ID, need)
                weak_planet = next(weak_planets)
            elif have > 0:
                issue_order(state, strong_planet.ID, weak_planet.ID, have)
                strong_planet = next(strong_planets)
            else:
                strong_planet = next(strong_planets)

    except StopIteration:
        return


def find_closest_planet(state, target_planets, my_planet):
    closest_distance = state.distance(target_planets[0].ID, my_planet.ID)
    closest_planet = target_planets[0]
    for planet in target_planets:
        temp = state.distance(planet.ID, my_planet.ID)
        curr_min = closest_distance
        if temp < curr_min:
            closest_distance = temp
            closest_planet = planet

    return closest_planet


def find_best_planet(state, target_planets, my_planet):

    d1 = state.distance(target_planets[0].ID, my_planet.ID)
    d2 = state.distance(target_planets[1].ID, my_planet.ID)
    d3 = state.distance(target_planets[2].ID, my_planet.ID)
    temp = d1
    if d2 > temp:
        temp = d1
        if d3 > temp:
            temp = d2
            if d2 > d3:
                temp = d3
    third_closest_distance = temp
    attack_planets = []
    for planet in target_planets:
        temp = state.distance(planet.ID, my_planet.ID)
        if len(attack_planets) < 6 or temp < third_closest_distance:
            attack_planets.append(planet)
            third_closest_distance = temp
    target = attack_planets[0]
    for planet in attack_planets:
        if state.distance(my_planet.ID, planet.ID) < state.distance(my_planet.ID, target.ID):
            target = planet
    return target
