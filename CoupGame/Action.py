from Enums import Actions
class Action():
	def perform_action(self, action, agent, target=None):
		if action == Actions.Tax:
			self.tax(agent)
		elif action == Actions.Foreign_Aid:
			self.forgein_aid(agent)
		elif action == Actions.Assasinate:
			card = self.assassinate(agent, target)
			return card
		elif action == Actions.Income:
			self.income(agent)
		elif action == Actions.Coup:
			card = self.coup(agent, target)
			return card
		elif action == Actions.Steal:
			self.steal(agent, target)
		elif action == Actions.Swap_Influence:
			self.swap_influence()
		elif action == Actions.Swap_Influence:
			self.block_foreign_aid()
		elif action == Actions.Block_Assasinate:
			self.block_assassination()
		elif action == Actions.Block_Steal:
			self.block_steal()		
				
	def tax(self, agent):
		agent.add_coins(3)

	def forgein_aid(self, agent):
		agent.add_coins(2)

	def assassinate(self, agent, target):
		agent.remove_coins(3)
		card = target.remove_card()
		return card

	def income(self, agent):
		agent.add_coins(1)

	def coup(self, agent, target):
		agent.remove_coins(7)
		card = target.remove_card()
		return card

	def steal(self, agent, target):
		if target.get_coins() == 0:
			agent.add_coins(0)
			target.remove_coins(0)
		elif target.get_coins() == 1:
			agent.add_coins(1)
			target.remove_coins(1)
		else:
			agent.add_coins(2)
			target.remove_coins(2)
	# TODO these still have to be implemented
	def swap_influence(self):
		return None

	def block_foreign_aid(self):
		return None

	def block_assassination(self):
		return None

	def block_steal(self):
		return None