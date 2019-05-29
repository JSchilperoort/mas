
class Action():

	def choose_action(self, action, agent, target):
		if action == "tax":
			self.tax(agent)
		elif action == "forgein_aid":
			self.forgein_aid(agent)
		elif action == "assassinate":
			self.assassinate(agent, target)
		elif action == "income":
			self.income(agent)
		elif action == "coup":
			self.coup(agent, target)
		elif action == "steal":
			self.steal(agent, target)
		elif action == "swap_influence":
			self.swap_influence()
		elif action == "block_foreign_aid":
			self.block_foreign_aid()
		elif action == "block_assassination":
			self.block_assassination()
		elif action == "block_steal":
			self.block_steal()		
				
	def tax(self, agent):
		print("Action chosen: tax")
		agent.add_coins(3)

	def forgein_aid(self, agent):
		print("Action chosen: forgein aid")
		agent.add_coins(2)

	def assassinate(self, agent, target):
		print("Action chosen: assassinate. Target: agent",target.get_id())
		agent.remove_coins(3)
		target.remove_card()

	def income(self, agent):
		print("Action chosen: income")
		agent.add_coins(1)

	def coup(self, agent, target):
		print("Action chosen: coup. Target: agent",target.get_id())
		agent.remove_coins(7)
		target.remove_card()

	def steal(self, agent, target):
		print("Action chosen: steal. Target: agent",target.get_id())
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