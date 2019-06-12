from tqdm import tqdm
from itertools import product, combinations_with_replacement


class KripkeModel:
	def __init__(self, n_players):
		self.n_players = n_players
		self.worlds = list()

		self.set_worlds()

	def set_worlds(self):
		print("setting worlds...")
		cards = ['assassin', 'countessa', 'captain', 'duke']
		# all 'possible' distributions of cards
		player_hands = list(combinations_with_replacement(cards, 2))
		possible_arrangements = list(product(player_hands, repeat=self.n_players))

		for pa in possible_arrangements:
			f = list()
			for i in range(self.n_players):
				f.append(list(pa[i]))
			world = World(f, self.n_players)
			if world.feasible():
				# no more than 3 instances of each card exists in the game
				self.worlds.append(world)
		print("Number of worlds: {0}".format(len(self.worlds)))
		self.set_relations()

	def set_relations(self):
		print("\nsetting relations...")
		count = 0
		for player in tqdm(range(self.n_players)):
			for i_w, world in enumerate(self.worlds):
				w1_cards = world.get_cards(player)
				for world2 in self.worlds[i_w + 1:]:
					w2_cards = world2.get_cards(player)
					# if this player has the same cards in both worlds, add relation
					if w1_cards == w2_cards:
						count += 1
						world.set_relation(world2, player)
						world2.set_relation(world, player)
		print("Number of relations: {0}".format(count))


class World:
	def __init__(self, formulas, n_players):
		self.formulas = formulas
		self.n_players = n_players
		self.relations = [[self]] * n_players

	def feasible(self):
		if sum(x.count('assassin') for x in self.formulas) > 3:
			return False
		if sum(x.count('countessa') for x in self.formulas) > 3:
			return False
		if sum(x.count('captain') for x in self.formulas) > 3:
			return False
		if sum(x.count('duke') for x in self.formulas) > 3:
			return False
		return True

	def set_relation(self, world, player):
		self.relations[player].append(world)

	def get_cards(self, player):
		return self.formulas[player]


def main():
	model = KripkeModel(n_players=4)
	# 2 players = 96 worlds, 828 relations
	# 3 players = 780 worlds, 90900 relations
	# 4 players = 4674 worlds, 4433712 relations


if __name__ == "__main__":
	main()
