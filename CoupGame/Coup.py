
from Agent import Agent
from Action import Action
from Card import Card
import random

class Coup:
	def __init__(self, n_players):
		self.n_players = n_players
		self.alive_agents = n_players
		self.players = list()
		self.turn_counter = 0
		self.deck = []
		self.make_deck()
		#self.deck = ["ambassador", "ambassador", "ambassador", "assassin", "assassin","assassin", "captain", "captain","captain", "countessa","countessa","countessa", "duke", "duke", "duke"]
		self.set_players()
		self.all_actions_active = ["tax", "steal", "swap_influence"]
		self.all_actions_reactive = ["block_foreign_aid", "block_assassination", "block_steal"]
		self.actions = Action()
		self.finished = False

	def deal_card(self):
		random.shuffle(self.deck)
		card = self.deck.pop()
		return card

	def make_deck(self):
		# for i in range(3):
		# 	self.deck.append(Card("ambassador"))
		for i in range(3):
			self.deck.append(Card("assassin"))
		for i in range(3):
			self.deck.append(Card("captain"))
		for i in range(3):
			self.deck.append(Card("countessa"))
		for i in range(3):
			self.deck.append(Card("duke"))
					
	def set_players(self):
		for i in range(self.n_players):
			property1, property2, property3 = 1, 2, 3
			self.players.append(Agent(i, property1, property2, property3))
		for player in self.players:
			card = self.deal_card()
			player.add_card(card)
			card = self.deal_card()  
			player.add_card(card)
							
	def choose_action(self, agent):
		# Return Action, Target, IsBluff
		if agent.get_coins() >= 7:
			target = self.get_random_target(agent)
			# agent must coup if coins are >= 7
			action = "coup"
			self.actions.choose_action(action, agent, target)
		else:
			bluff = 0
			rand_int = random.randint(1, 4)
			if rand_int >= 2:
				bluff = 1

			cards = agent.get_cards()
			possible_actions_active = []
			possible_actions_reactive = []
			for card_actions in agent.get_possible_actions("active"):
				for action in card_actions:
					if action == "assassinate":
						if agent.get_coins() >= 3: 
							# only allow assasinate if agent has >= 3 coins
							possible_actions_active.append(action)
					else:
						possible_actions_active.append(action)

			for card_actions in agent.get_possible_actions("reactive"):
				for action in card_actions:
					possible_actions_reactive.append(action)

			possible_actions_active.append("income")
			possible_actions_active = set(possible_actions_active)
			possible_actions_reactive = set(possible_actions_reactive)
			possible_actions_active = list(filter(None, possible_actions_active))
			possible_actions_reactive = list(filter(None, possible_actions_reactive))
			#print(possible_actions_active)
			if bluff == 0:
				# No bluff: pick one of the available card actions
				print("Agent chooses: no bluff")

				action = random.choice(possible_actions_active)

				# TODO: prompt action, let other agents react to this prompt (call bluff for example)

				target = self.get_random_target(agent)
				print("Action chooses:", action)
				print("Target: Agent", target.get_id())
				if action == "tax":
					rand_int = random.randint(1, 4)
					if rand_int >= 4:
						# random agent wrongfully calls bluff
						caller = self.get_random_target(agent)
						caller.remove_card()

				elif action == "assassinate":
					if target.has_card("countessa"):
						# target calls block with countessa
						rand_int = random.randint(1, 4)
						if rand_int >= 4:
							# agent wrongfully calls bluff
							agent.remove_card()
					else:
						rand_int = random.randint(1, 4)
						if rand_int >= 4:
							# target bluffs that he has countessa
							rand_int = random.randint(1, 4)
							if rand_int >= 3:
								# agent believes the bluff: pay the 3 coins, nothing happens
								agent.remove_coins(3)
							else:
								# agent calls the bluff
								target.remove_card()


				elif action == "steal":
					if target.has_card("captain"):
						# target calls block with captain
						rand_int = random.randint(1, 4)
						if rand_int >= 4:
							# agent wrongfully calls bluff
							agent.remove_card()
					else:
						
						rand_int = random.randint(1, 4)
						if rand_int >= 4:
							# target bluffs that he has captain
							rand_int = random.randint(1, 4)
							if rand_int >= 3:
								# agent believes the bluff: nothing happens
								pass
							else:
								# agent calls the bluff
								target.remove_card()

				self.actions.choose_action(action, agent, target)

			else:
				# Bluff: pick a random action 
				all_actions_active = self.all_actions_active.copy()
				if agent.get_coins() >= 3:
					all_actions_active.append("assassinate")
				bluff_actions = []

				print("Agent chooses: bluff")
				actions = self.all_actions_active.copy()
				print(actions)
				if agent.get_coins() >= 3: 
					actions.append("assassinate")
				action = random.choice(actions)
				for action in all_actions_active:
					if action not in possible_actions_active:
						bluff_actions.append(action)
				#print(all_actions_active)
				#print(bluff_actions)
				action = random.choice(bluff_actions)
				print("Action chosen:", action)
		return action

	"""
	def get_next_agent(self):
		print(self.turn_counter)
		if self.turn_counter >= self.n_players:
			self.turn_counter = 0

		agent = self.players[self.turn_counter]
		self.turn_counter += 1

		return agent
	"""

	def get_next_agent(self):
		print(self.turn_counter)
		inf = 1
		while inf == 1:
			if self.turn_counter >= self.n_players:
				self.turn_counter = 0
			agent = self.players[self.turn_counter]
			if agent.is_alive() == True:
				self.turn_counter += 1	
				return agent	
			else:
				self.turn_counter += 1		


		

		#for i in range(self.turn_counter, self.n_players):


		#agent = self.players[self.turn_counter]
		

		#return agent


	def get_random_target(self, agent):
		target_ids = []
	#	target_ids_alive = []
		for i in range(self.n_players):
			if i != agent.get_id() and self.players[i].is_alive() == True:
				target_ids.append(i)

	#	for target_id in target_ids:
	#		if self.players[target_id].is_alive() == True:
	#			target_ids_alive.append(target_id)
		target_id = random.choice(target_ids)
		target = self.players[target_id]
		#target = random.choice(self.players)

		return target

	def is_finished(self):
		alive_agents = 0
		for agent in self.players:
			if agent.is_alive():
				alive_agents += 1
		if alive_agents <= 1:
			print("player {0} won the game!".format(self.players[0].identifier))
			self.finished = True


	"""
	def remove_dead_players(self):
		to_remove = list()
		for agent in self.players:
			if not agent.alive:
				to_remove.append(agent)
		self.players = [x for x in self.players if x not in to_remove]
		self.n_players = len(self.players)
		for agent in to_remove:
			print("-- player {0} was killed".format(agent.identifier))
		if self.n_players <= 1:
			print("player {0} won the game!".format(self.players[0].identifier))
			self.finished = True
	"""

	def get_players(self):
		return self.players