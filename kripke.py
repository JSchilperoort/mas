import sys
from tqdm import tqdm
from itertools import product


class KripkeModel:
	def __init__(self, n_players):
		self.n_players = n_players
		self.worlds = list()

		self.set_worlds()

	def set_worlds(self):
		print("setting worlds...")
		cards = ['assassin', 'countessa', 'captain', 'duke']
		# all 'possible' distributions of cards
		possible_arrangements = product(cards, repeat=self.n_players*2)
		for pa in possible_arrangements:
			f = list()
			for i in range(self.n_players):
				f.append([pa[2*i], pa[2*i+1]])
			world = World(f, self.n_players)
			if world.feasible():
				# no more than 3 instances of each card exists in the game
				self.worlds.append(world)
		print(len(self.worlds))
		self.set_relations()

	def set_relations(self):
		print("\nsetting relations...")
		index = 0
		for player in tqdm(range(self.n_players)):
			for i_w, world in enumerate(self.worlds):
				w1_cards = world.get_cards(player)
				for world2 in self.worlds[i_w + 1:]:
					w2_cards = world2.get_cards(player)
					# if this player has the same cards in both worlds, add relation
					if w1_cards == w2_cards:
						index += 1
						world.set_relation(world2, player)
						world2.set_relation(world, player)
		print(index)


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


def main(argv):
	model = KripkeModel(n_players=3)
	# 2 players = 252 worlds, 3720 relations
	# 3 players = 3480 worlds, 1138068 relations
	# 4 players = 36120 worlds, 165544560 relations


if __name__ == "__main__":
	main(sys.argv)
