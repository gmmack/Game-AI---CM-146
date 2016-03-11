#!/usr/bin/env python
#

"""
// The do_turn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist.
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


def setup_behavior_tree():
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')
    """
    spread_weakest_sequence = Sequence(name='Spread weakest neutral')
    spread_weakest_planet = Check(available)
    spread_weakest_action = Action(spread_to_weakest_neutral)
    spread_sequence.child_nodes = [spread_weakest_planet, spread_weakest_action]
    """

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_closest_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    defend_plan = Sequence(name='Defend Strategy')
    incoming_attack_check = Check(incoming_attack)
    defense = Action(d_fence)
    defend_plan.child_nodes = [incoming_attack_check, defense]

    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    atk_weakest_sequence = Sequence(name='Attack Weakest Strategy')
    n_planet_check = Check(if_neutral_planet_available)
    atk_weakest_action = Action(attack_weakest_planet)
    atk_weakest_sequence.child_nodes = [n_planet_check, atk_weakest_action]

    root.child_nodes = [atk_weakest_sequence, offensive_plan, spread_sequence, defend_plan, attack.copy()]

    logging.info('\n' + root.tree_to_string())
    return root


if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                behavior_tree.execute(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:

        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
