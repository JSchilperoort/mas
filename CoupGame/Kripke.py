# from tqdm import tqdm
from itertools import product, combinations_with_replacement


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
		for player in range(self.n_players):
			for i_w, world in enumerate(self.worlds):
				w1_cards = world.get_cards(player)
				# this loop can start after world i_w since all relations are reflexive
				for world2 in self.worlds[i_w + 1:]:
					w2_cards = world2.get_cards(player)
					# if this player has the same cards in both worlds, add relation
					if w1_cards == w2_cards:
						# set relation in both directions
						world.set_relation(world2, player)
						world2.set_relation(world, player)
		print("Number of worlds: {0}".format(len(self.worlds)))
		print("Number of relations: {0}".format(self.count_relations()))

	# remove all relations between worlds
	def remove_relations(self):
		for world in self.worlds:
			world.remove_relations()

	# count and return the number of relations in the model
	def count_relations(self):
		count = 0
		for world in self.worlds:
			count += world.count_relations()
		return count

	# return the world with formulas 'f'
	def get_world(self, f):
		for world in self.worlds:
			if world.same_formulas(f):
				return world

	# in 'world', does 'player' know that 'opponent' has 'boolean' 'card'
	def query(self, cards_player, player, opponent, boolean, card):
		for world in self.worlds:
			if cards_player[0] == world.get_cards(player)[0] and cards_player[1] == world.get_cards(player)[1] or cards_player[0] == world.get_cards(player)[1] and cards_player[1] == world.get_cards(player)[0]:
				if boolean:
					if not world.has_card_in_all_worlds(player, opponent, card):
						return False
				else:
					if not world.does_not_have_card_in_any_world(player, opponent, card):
						return False
		return True

	# make a card of a given player visible
	def flip_card(self, player, card):
		new_worlds = list()
		for world in self.worlds:
			if world.can_flip(player, card):
				world.set_visible(player, card)
				new_worlds.append(world)
		self.worlds = new_worlds
		self.remove_relations()
		self.set_relations()


class World:
	def __init__(self, formulas, visible_cards, n_players, cards):
		self.formulas = formulas  # distribution of cards
		self.visible_cards = visible_cards  # boolean list of whether certain cards are flipped
		self.n_players = n_players  # number of players in the game
		self.relations = [[self]] * n_players  # initialize world with only reflexive relations to itself
		self.belief_relations = [[self]] * n_players  # initialize world with only reflexive beliefs
		self.cards = cards  # all cards

	# check whether the distribution of cards is possible (no more than three instances of each card)
	def feasible(self):
		for card in self.cards:
			if sum(x.count(card) for x in self.formulas) > 3:
				return False
		return True

	# set a relation between two worlds (exists as a list of pointers from this world to those worlds)
	def set_relation(self, world, player):
		self.relations[player].append(world)

	# check if an opponent has a certain card in all worlds accessible from this world by the player
	def has_card_in_all_worlds(self, player, opponent, card):
		for relation in self.relations[player]:
			if not card in relation.get_cards(opponent):
				return False
		return True

	# check whether the player can be certain that the opponent does not have a specific cart
	def does_not_have_card_in_any_world(self, player, opponent, card):
		for relation in self.relations[player]:
			if card in relation.get_cards(opponent):
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
	def get_cards(self, player):
		return self.formulas[player]

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

	# count the number of relations from this world to itself and other worlds
	def count_relations(self):
		count = 0
		for relation in self.relations:
			count += len(relation)
		return count


def main():
	cards = ['assassin', 'countessa', 'captain', 'duke']
	model = KripkeModel(n_players=4, cards=cards)
	model.flip_card(2, 'assassin')
	model.flip_card(2, 'assassin')
	model.flip_card(1, 'assassin')
	model.flip_card(1, 'countessa')
	model.flip_card(0, 'countessa')
	model.flip_card(0, 'countessa')
	# if model.query(['duke', 'assassin'], 1, 2, True, 'captain'):
	# 	print("Player {0} knows that player {1} has card {2}".format(1, 2, 'captain'))
	# else:
	# 	print("Player {0} does not know whether player {1} has card {2}".format(1, 2, 'captain'))
	#
	# if model.query(['duke', 'assassin'], 1, 2, False, 'captain'):
	# 	print("Player {0} knows that player {1} does not have card {2}".format(1, 2, 'captain'))
	# else:
	# 	print("Player {0} does not know whether player {1} does not have card {2}".format(1, 2, 'captain'))

	# 2 players = 96 worlds, 828 relations   ~0 seconds
	# 3 players = 780 worlds, 90900 relations   ~0 seconds
	# 4 players = 4674 worlds, 4433712 relations   ~12 seconds
	# 5 players = 16260 worlds, 67616850 relations   ~5 minutes


if __name__ == "__main__":
	main()