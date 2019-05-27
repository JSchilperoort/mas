
class Card:

	def __init__(self, influence):
		self.influence = influence

	def get_action(self, action_type):
		if self.influence == "ambassador":
			action_active = ["swap_influence"]
			action_reactive = ["block_stealing"]

		elif self.influence == "assassin":
			action_active = ["assassinate"]
			action_reactive = [""]

		elif self.influence == "captain":
			action_active = ["steal"]
			action_reactive = ["block_stealing"]

		elif self.influence == "countessa":
			action_active = [""]
			action_reactive = ["block_asssassination"]		

		elif self.influence == "duke":
			action_active = ["tax"]		
			action_reactive = ["block_forgein_aid"]

		if action_type == "active":	
			return action_active

		if action_type == "reactive":
			return action_reactive

	def get_influence(self):
		return self.influence
