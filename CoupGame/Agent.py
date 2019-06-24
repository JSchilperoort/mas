import random

class Agent:
	def __init__(self, identifier, property_1, property_2, property_3):
		self.identifier = identifier
		self.prop1 = property_1
		self.prop2 = property_2
		self.prop3 = property_3
		self.cards = []
		self.dead_cards = []
		self.coins = 2
		self.actions_active = []
		self.actions_reactive = []
		self.alive = True

	def get_id(self):
		return self.identifier

	def add_card(self,card):
		self.cards.append(card)

	def remove_card(self):
		random.shuffle(self.cards)
		#print(self.alive)
		try:
			card = self.cards.pop()
			self.dead_cards.append(card)
		except:
			print("Failed removing card for agent:" + str(self.identifier))
			pass
		if len(self.cards) <= 0:
			self.alive = False
			print("-- player", self.identifier, "was killed")
		
	def get_cards(self):
		return self.cards

	def get_dead_cards(self):
		return self.dead_cards

	def get_coins(self):
		return self.coins

	def add_coins(self, amount):
		self.coins += amount

	def remove_coins(self, amount):
		self.coins -= amount
		if self.coins < 0:
			self.coins = 0

	def has_card(self, influence):
		for card in self.cards:
			if card.influence is influence:
				return True
		return False

	def is_alive(self):
		if self.alive == True:
			return True
		else:
			return False

	def get_identifier(self):
		return self.identifier