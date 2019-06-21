from tqdm import tqdm
from itertools import product, combinations_with_replacement


class KripkeModel:
	def __init__(self, n_players, cards):
		self.n_players = n_players
		self.worlds = list()
		self.cards = cards

		self.set_worlds()

	def set_worlds(self):
		print("setting worlds...")
		# all 'possible' distributions of cards
		player_hands = list(combinations_with_replacement(self.cards, 2))
		possible_arrangements = list(product(player_hands, repeat=self.n_players))

		for pa in possible_arrangements:
			f = list()
			for i in range(self.n_players):
				f.append(list(pa[i]))
			world = World(f, self.n_players, self.cards)
			if world.feasible():
				# no more than 3 instances of each card exists in the game
				self.worlds.append(world)
		print("Number of worlds: {0}".format(len(self.worlds)))
		self.set_relations()

	def set_relations(self):
		print("\nsetting relations...")
		count = 0
		for player in range(self.n_players):
			for i_w, world in enumerate(tqdm(self.worlds)):
				w1_cards = world.get_cards(player)
				for world2 in self.worlds[i_w + 1:]:
					w2_cards = world2.get_cards(player)
					# if this player has the same cards in both worlds, add relation
					if w1_cards == w2_cards:
						count += 1
						world.set_relation(world2, player)
						world2.set_relation(world, player)
		print("Number of relations: {0}".format(count))

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


class World:
	def __init__(self, formulas, n_players, cards):
		self.formulas = formulas
		self.n_players = n_players
		self.relations = [[self]] * n_players
		self.cards = cards

	def feasible(self):
		for card in self.cards:
			if sum(x.count(card) for x in self.formulas) > 3:
				return False
		return True

	def set_relation(self, world, player):
		self.relations[player].append(world)

	def has_card_in_all_worlds(self, player, opponent, card):
		for relation in self.relations[player]:
			if not card in relation.get_cards(opponent):
				return False
		return True

	def does_not_have_card_in_any_world(self, player, opponent, card):
		for relation in self.relations[player]:
			if card in relation.get_cards(opponent):
				return False
		return True

	def same_formulas(self, formulas_other):
		for i, own_hand in enumerate(self.formulas):
			# print(own_hand)
			other_hand = formulas_other[i]
			if not(own_hand[0] == other_hand[0] and own_hand[1] == other_hand[1]) and \
					not(own_hand[0] == other_hand[1] and own_hand[1] == other_hand[0]):
				return False
		return True

	def get_cards(self, player):
		return self.formulas[player]


def main():
	cards = ['assassin', 'countessa', 'captain', 'duke']
	model = KripkeModel(n_players=3, cards=cards)
	if model.query(['duke', 'assassin'], 1, 2, True, 'captain'):
		print("Player {0} knows that player {1} has card {2}".format(1, 2, 'captain'))
	else:
		print("Player {0} does not know whether player {1} has card {2}".format(1, 2, 'captain'))

	if model.query(['duke', 'assassin'], 1, 2, False, 'captain'):
		print("Player {0} knows that player {1} does not have card {2}".format(1, 2, 'captain'))
	else:
		print("Player {0} does not know whether player {1} does not have card {2}".format(1, 2, 'captain'))

	# 2 players = 96 worlds, 828 relations   ~0 seconds
	# 3 players = 780 worlds, 90900 relations   ~0 seconds
	# 4 players = 4674 worlds, 4433712 relations   ~12 seconds
	# 5 players = 16260 worlds, 67616850 relations   ~5 minutes


if __name__ == "__main__":
	main()
