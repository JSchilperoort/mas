# from tqdm import tqdm
from itertools import product, combinations_with_replacement
from copy import deepcopy

class KripkeModel:
	def __init__(self, n_players, cards):
		self.n_players = n_players  # number of players
		self.worlds = list()  # all worlds in the model
		self.cards = cards  # types of cards
		self.set_worlds()  # initialize worlds

	# set worlds given the parameters
	def set_worlds(self):
		print("setting worlds...")
		# all 'possible' distributions of cards
		player_hands = list(combinations_with_replacement(self.cards, 2))
		possible_arrangements = list(product(player_hands, repeat=self.n_players))

		for pa in possible_arrangements:
			f = list()
			visible_cards = list()
			for i in range(self.n_players):
				f.append(list(pa[i]))  # add hand to formulas
				visible_cards.append([False, False])  # initially, all cards are not visible, hence [false, false]
			world = World(f, visible_cards, self.n_players, self.cards)  # set world with the parameters
			if world.feasible():
				# no more than 3 instances of each card exists in the game
				self.worlds.append(world)
		# set the relations between the worlds
		self.set_relations()

	# set the relations between the worlds in the model
	def set_relations(self):
		print("\nsetting relations...")
		count = 0
		for player in range(self.n_players):
			for i_w, world1 in enumerate(self.worlds):
				w1_cards = world1.get_cards(player, visible_cards=True)
				# this loop can start after world i_w since all relations are reflexive
				for world2 in self.worlds[i_w + 1:]:

					w2_cards = world2.get_cards(player, visible_cards=True)
					# if this player has the same cards in both worlds, add relation
					if w1_cards == w2_cards:
						count += 1
						# print('before::')
						# print(self.count_relations())
						world1.set_relation(world2, player)
						world2.set_relation(world1, player)
						# print('after:::')
						# print(self.count_relations())
		print("Number of worlds: {0}".format(len(self.worlds)))
		print("Number of relations: {0}".format(self.count_relations()))

	# remove all relations between worlds
	def remove_relations(self):
		for world in self.worlds:
			world.remove_relations()

	# remove all relations between worlds
	def remove_relations_dead_players(self):
		for player in range(self.n_players):
			for world in self.worlds:
				if len(world.get_cards(player, visible_cards=False)) == 0:
					world.remove_relations_player(player)

	# count and return the number of relations in the model
	def count_relations(self):
		count = 0
		for world in self.worlds:
			count += world.count_relations()

			#print(count)
		#print(" Added relations:", count)
		return count

	# return the world with formulas 'f'
	def get_world(self, f):
		for world in self.worlds:
			if world.same_formulas(f):
				return world

	# in 'world', does 'player' know that 'opponent' has 'boolean' 'card'
	def query(self, cards_player, player, opponent, boolean, card):
		for world in self.worlds:
			other_hand = world.get_cards(player, visible_cards=True)
			if self.same_hand(cards_player, other_hand):
				if boolean:
					if not world.has_card_in_all_worlds(player, opponent, card):
						return False
				else:
					if not world.does_not_have_card_in_any_world(player, opponent, card):
						return False
		return True

	def same_hand(self, cards1, cards2):
		if len(cards1) == len(cards2):
			if (cards1[0] == cards2[0] and cards1[1] == cards2[1]) or (cards1[0] == cards2[1] and cards1[1] == cards2[0]):
				return True
		return False

	# make a card of a given player visible
	def flip_card(self, player, card):
		new_worlds = list()
		for world in self.worlds:
			if world.can_flip(player, card):
				world.set_visible(player, card)
				new_worlds.append(world)
		self.worlds = new_worlds
		self.remove_relations()
		print(self.count_relations())
		self.set_relations()
		self.remove_relations_dead_players()


class World:
	def __init__(self, formulas, visible_cards, n_players, cards):
		self.formulas = formulas  # distribution of cards
		self.visible_cards = visible_cards  # boolean list of whether certain cards are flipped
		self.n_players = n_players  # number of players in the game
		self.relations_player0 = [self]
		self.relations_player1 = [self]

		self.cards = cards  # all cards

	# check whether the distribution of cards is possible (no more than three instances of each card)
	def feasible(self):
		for card in self.cards:
			if sum(x.count(card) for x in self.formulas) > 3:
				return False
		return True

	# set a relation between two worlds (exists as a list of pointers from this world to those worlds)
	def set_relation(self, world, player):
		# print()
		# print(self.relations_player0)
		# print(self.relations_player1)
		if player == 0:
			self.relations_player0.append(world)
		if player == 1:
			self.relations_player1.append(world)
		#
		# print(self.relations_player0)
		# print(self.relations_player1)

	# check if an opponent has a certain card in all worlds accessible from this world by the player
	def has_card_in_all_worlds(self, player, opponent, card):
		for relation in self.relations[player]:
			# there exists an accessible world in which the opponent does not have 'card'
			if not card in relation.get_cards(opponent, visible_cards=False):
				return False
		return True

	# check whether the player can be certain that the opponent does not have a specific cart
	def does_not_have_card_in_any_world(self, player, opponent, card):
		for relation in self.relations[player]:
			if card in relation.get_cards(opponent, visible_cards=True):
				return False
		return True

	# check whether the formulas in the argument are the same as the ones in this world
	def same_formulas(self, formulas_other):
		for i, own_hand in enumerate(self.formulas):
			other_hand = formulas_other[i]
			if not(own_hand[0] == other_hand[0] and own_hand[1] == other_hand[1]) and \
					not(own_hand[0] == other_hand[1] and own_hand[1] == other_hand[0]):
				return False
		return True

	# return the hand of a player
	def get_cards(self, player, visible_cards):
		return_cards = list()
		for i, c in enumerate(self.formulas[player]):
			if visible_cards:
				return_cards.append(self.formulas[player][i])
			else:
				if not self.visible_cards[player][i]:
					return_cards.append(self.formulas[player][i])
		return return_cards

	# check whether it is possible to flip a given card for a given player
	def can_flip(self, player, flip_card):
		for i, card in enumerate(self.formulas[player]):
			# does player have card? + Was card not already flipped?
			if card == flip_card and not self.visible_cards[player][i]:
				return True

	# flip card
	def set_visible(self, player, flipped_card):
		for i, card in enumerate(self.formulas[player]):
			if card == flipped_card and not self.visible_cards[player][i]:
				self.visible_cards[player][i] = True
				break

	# remove all relations (except the reflexive relation) from this world
	def remove_relations(self):
		self.relations = [[self]] * self.n_players

	def remove_relations_player(self, player):
		self.relations[player] = []

	# count the number of relations from this world to itself and other worlds
	def count_relations(self):
		count = 0
		count += len(self.relations_player0)
		count += len(self.relations_player1)

		return count


def main():
	cards = ['assassin', 'countessa', 'captain', 'duke']
	model = KripkeModel(n_players=2, cards=cards)
	model.flip_card(1, 'assassin')
	model.flip_card(1, 'assassin')

	other_card = 'countessa'
	own_hand = ['countessa', 'duke']
	player = 0
	other_player = 1
	worlds = model.worlds

	# for world in worlds:
	# 	this_cards = world.formulas
	# 	print()
	# 	print(this_cards)
	# 	for i, w in enumerate(world.relations_player0):
	# 		print(w.formulas)


	if model.query(own_hand, player, other_player, True, other_card):
		print("Player {0} knows that player {1} has card {2}".format(player, other_player, other_card))
	else:
		print("Player {0} does not know whether player {1} has card {2}".format(player, other_player, other_card))

	if model.query(own_hand, player,  other_player, False, other_card):
		print("Player {0} knows that player {1} does not have card {2}".format(player, other_player, other_card))
	else:
		print("Player {0} does not know whether player {1} does not have card {2}".format(player, other_player, other_card))

	# 2 players = 96 worlds, 828 relations   ~0 seconds
	# 3 players = 780 worlds, 90900 relations   ~0 seconds
	# 4 players = 4674 worlds, 4433712 relations   ~12 seconds
	# 5 players = 16260 worlds, 67616850 relations   ~5 minutes


if __name__ == "__main__":
	main()