
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 10000
explore_faction = 2.0

def traverse_nodes(node, state, identity):
	""" Traverses the tree until the end criterion are met.

	Args:
		node:		A tree node from which the search is traversing.
		state:		The state of the game.
		identity:	The bot's identity, either 'red' or 'blue'.

	Returns:		A node from which the next stage of the search can proceed.

	"""
	#no tried actions but child nodes exist
	leaf_node = node
	myList = node.child_nodes.values()
	while leaf_node.untried_actions == [] and len(myList) != 0:
		if identity == state.player_turn:
			leaf_node = max(myList, key = lambda c: (c.wins/c.visits) + (explore_faction)*sqrt(2*log(c.parent.visits)/c.visits))
		else:
			leaf_node = max(myList, key = lambda c: (1 - c.wins/c.visits) + (explore_faction)*sqrt(2*log(c.parent.visits)/c.visits))
		myList = leaf_node.child_nodes.values()
		state.apply_move(leaf_node.parent_action)
	return leaf_node
	# Hint: return leaf_node


def expand_leaf(node, state):
	""" Adds a new leaf to the tree by creating a new child node for the given node.

	Args:
		node:	The node for which a child will be added.
		state:	The state of the game.

	Returns:	The added child node.

	"""
	new_node = node
	if len(node.untried_actions) != 0:
		next_move = choice(node.untried_actions)
		state.apply_move(next_move)
		new_node = MCTSNode(parent=node, parent_action=next_move, action_list=state.legal_moves)
		node.untried_actions.remove(next_move)
		node.child_nodes[next_move] = new_node
	return new_node
	# Hint: return new_node


def rollout(state):
	""" Given the state of the game, the rollout plays out the remainder randomly.

	Args:
		state:	The state of the game.

	"""
	while not state.is_terminal:
		state.apply_move(choice(state.legal_moves))


def backpropagate(node, won):
	""" Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

	Args:
		node:	A leaf node.
		won:	An indicator of whether the bot won or lost the game.

	"""
	while node != None:
		node.wins += won
		node.visits += 1
		node = node.parent


def incFactor():
	#explore_faction = explore_faction * 0.8
	tmp = explore_faction
	#tmp *= 1.2
	tmp += .1
	return tmp
def decFactor():
	tmp = explore_faction
	#tmp *= 0.8
	if tmp > .1:
		tmp -= .1
	return tmp
	#explore_faction = explore_faction * 1.3

def think(state):
	""" Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

	Args:
		state:	The state of the game.

	Returns:	The action to be taken.

	"""
	identity_of_bot = state.player_turn
	root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)

	for step in range(num_nodes):
		# Copy the game for sampling a playthrough
		sampled_game = state.copy()

		# Start at root
		node = root_node

		# Do MCTS - This is all you!
		leaf_node = traverse_nodes(node, sampled_game, identity_of_bot)
		new_node = expand_leaf(leaf_node, sampled_game)
		rollout(sampled_game)
		turnVal = 999# dummy values
		if sampled_game.winner == identity_of_bot:
			turnVal = 1
			#if doing well exploit more
			explore_faction = decFactor()
		elif sampled_game.winner == 'tie':
			turnVal = 0
		else:
			#if doing badly explore more
			turnVal = -1
			explore_faction = incFactor()
		backpropagate(new_node, turnVal)
	# Return an action, typically the most frequently used action (from the root) or the action with the best
	# estimated win rate.
	return max(root_node.child_nodes.values(), key = lambda c: c.visits).parent_action
