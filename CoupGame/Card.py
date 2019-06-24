from Enums import Influence, Actions
class Card:

	def __init__(self, influence):
		self.influence = influence

	def get_action_active(self):
		if self.influence == Influence.Ambassador:
			return Actions.Swap_Influence

		elif self.influence == Influence.Assassin:
			return Actions.Assasinate

		elif self.influence == Influence.Captain:
			return Actions.Steal

		elif self.influence == Influence.Contessa:
			return None	

		elif self.influence == Influence.Duke:
			return Actions.Tax

	def get_action_reactive(self):
		if self.influence == Influence.Ambassador:
			return Actions.Block_Steal

		elif self.influence == Influence.Assassin:
			return None

		elif self.influence == Influence.Captain:
			return Actions.Steal

		elif self.influence == Influence.Contessa:
			return Actions.Block_Assasinate

		elif self.influence == Influence.Duke:
			return Actions.Block_Foreign_Aid

	def get_influence(self):
		return self.influence
