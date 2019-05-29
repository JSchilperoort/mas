import random

class Agent:
	def __init__(self, identifier, property_1, property_2, property_3):
		self.identifier = identifier
		self.prop1 = property_1
		self.prop2 = property_2
		self.prop3 = property_3
		self.cards = []
		self.coins = 2
		self.actions_active = []
		self.actions_reactive = []

	def get_id(self):
		return self.identifier

	def add_card(self,card):
		self.cards.append(card)

	def remove_card(self):
		random.shuffle(self.cards)
		self.cards.pop()		
		
	def get_cards(self):
		return self.cards

	def get_coins(self):
		return self.coins

	def add_coins(self, amount):

		self.coins += amount

	def remove_coins(self, amount):
		self.coins -= amount

	def get_possible_actions(self, action_type):
		actions = []
		for card in self.cards:
			action = card.get_action(action_type)
			actions.append(action)
		return actions

	def has_card(self, influence):
		if influence in self.cards:
			return True
		else:
			return False

	def get_identifier(self):
		return self.identifier