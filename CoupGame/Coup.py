
from Agent import Agent
from Action import Action
from Card import Card
import random
from Kripke import KripkeModel
from Enums import Influence, Actions
from BluffSequence import BluffSequence
from ActionSequence import ActionSequence
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
		self.all_actions_active = [Actions.Tax, Actions.Steal, Actions.Assasinate]
		self.all_actions_reactive = [Actions.Block_Assasinate, Actions.Block_Foreign_Aid, Actions.Block_Steal]
		self.actions = Action()
		self.finished = False
		self.model = KripkeModel(n_players, [Influence.Ambassador, Influence.Contessa, Influence.Captain, Influence.Duke])

	def deal_card(self):
		if not self.deck:
			return None
		return self.deck.pop()

	def make_deck(self):
		for influence in Influence:
			if influence == Influence.Ambassador:
				continue
			for i in range(3):
				self.deck.append(Card(influence))
		random.shuffle(self.deck)
					
	def set_players(self):
		for i in range(self.n_players):
			property1, property2, property3 = 1, 2, 3
			agent = Agent(i, property1, property2, property3)
			agent.add_card(self.deal_card())
			agent.add_card(self.deal_card())
			self.players.append(agent)
						
	def choose_action(self, agent):
		action_sequence = []
		bluff_sequence = []

		# If agent has enough coins to coup it will
		if agent.coins >= 7:
			action = Actions.Coup
			target =  self.get_random_target(agent)
			action_sequence.append(ActionSequence(action, agent, target))
			self.actions.perform_action(action, agent, target)
			return action_sequence, bluff_sequence
		
		# Determine the possible active and reactive actions for the agent
		possible_actions_active = []
		possible_actions_active.append(Actions.Income)
		possible_actions_active.append(Actions.Foreign_Aid)
		possible_actions_reactive = []
		for card in agent.cards:
			action_active = card.get_action_active()
			action_reactive = card.get_action_reactive()
			# only allow assasinate if agent has >= 3 coin
			if action_active == Actions.Assasinate and agent.coins <= 3:
				continue
			# Keep list unique and without None values
			if action_active is not None and action_active not in possible_actions_active:
				possible_actions_active.append(action_active)
			if action_reactive is not None and action_reactive not in possible_actions_reactive:
				possible_actions_reactive.append(action_reactive)	

	
		# Income cant be blocked 
		# 25% chance to bluff
		bluff = random.randint(0, 3)
		
		if bluff > 0:
			# Player will not bluff
			action = random.choice(possible_actions_active)
			if action == Actions.Income:
				action_sequence.append(ActionSequence(action, agent, None))
				self.actions.perform_action(action, agent)

			elif action == Actions.Foreign_Aid:
				# Random target will bluff having duke if he doesn't have it
				if  random.randint(0, 3) == 0:
					target = self.get_random_target(agent)
				else:
					target = None
					for player in self.players:
						if player.has_card(Influence.Duke):
							target = player
							break
							
					if target is None:
						# No target can block
							action_sequence.append(ActionSequence(action, agent, None))
							self.actions.perform_action(action, agent)
							return action_sequence, bluff_sequence

					if  random.randint(0, 3) > 1:
						# Agent believes target
						#TODO Fix believes in bluff
						bluff_sequence.append(BluffSequence(Actions.Block_Foreign_Aid, target, agent, False))
					else:
						# Agent doesn't believe target
						if target.has_card(Influence.Duke):
							# Wrongly called bluff
							bluff_sequence.append(BluffSequence(Actions.Block_Foreign_Aid, target, agent, False))
							agent.remove_card()
						else:
							# Correctly called bluff on target
							bluff_sequence.append(BluffSequence(Actions.Block_Foreign_Aid, target, agent, True))
							target.remove_card()
							action_sequence.append(ActionSequence(action, agent, None))
							self.actions.perform_action(action, agent)
			
						
			elif action == Actions.Tax:
				if random.randint(0, 3) == 0:
					# Random player wrongfully called bluff
					bluff_caller = self.get_random_target(agent)
					bluff_caller.remove_card()
					action_sequence.append(ActionSequence(action, agent, None))
					bluff_sequence.append(BluffSequence(action, agent, bluff_caller, False))
					self.actions.perform_action(action, agent)
				else:
					# No bluff was called
					action_sequence.append(ActionSequence(action, agent, None))
					self.actions.perform_action(action, agent)

			elif action == Actions.Assasinate:
				target = self.get_random_target(agent)
				if target.has_card(Influence.Contessa):
					# target calls block with countessa
					if random.randint(0, 3) == 0:
						# agent wrongfully calls bluff
						bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, False))
						agent.remove_card()
					# Action is blocked
					action_sequence.append((ActionSequence(Actions.Block_Assasinate, target, agent)))
				else:
					# Target cant't block card
					if  random.randint(0, 3) == 0:
						# target bluffs that he has contessa
						if random.randint(0, 3) > 1:
							# Agent believes the bluff; loses coins and performs no action
							#TODO Check of het klopt dat je coins verliest
							agent.remove_coins(3)
							#TODO Fix bluffsequence zodat je kan believen/niet believen
							action_sequence.append((ActionSequence(Actions.Block_Assasinate, target, agent)))
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, False))
						else:
							# Correctly called bluff so remove card of target
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True))
							target.remove_card()
							action_sequence.append(ActionSequence(action, agent, target))
							self.actions.perform_action(action, agent, target)
					else:						
						# Contessa wasn't bluffed
						action_sequence.append(ActionSequence(action, agent, target))
						self.actions.perform_action(action, agent, target)

			
			elif action == Actions.Steal:
				target = self.get_random_target(agent)
				if target.has_card(Influence.Captain):
					# target calls block with Captain
					if random.randint(0, 3) == 0:
						# agent wrongfully calls bluff
						bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, False))
						agent.remove_card()
					# Action is blocked
					action_sequence.append(ActionSequence(Actions.Block_Steal, target, agent))
				else:
					# Target cant't block card
					if  random.randint(0, 3) == 0:
						# target bluffs that he has Captain
						if random.randint(0, 3) > 1:
							# Agent believes the bluff and performs no action
							action_sequence.append(ActionSequence(Actions.Block_Steal, target, agent))
							bluff_sequence.append(BluffSequence(Actions.v, target, agent, False))
						else:
							# Correctly called bluff so remove card of target
							bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, True))
							target.remove_card()
							action_sequence.append(ActionSequence(action, agent, target))
							self.actions.perform_action(action, agent, target)
					else:						
						# Captain wasn't bluffed
						action_sequence.append(ActionSequence(action, agent, target))
						self.actions.perform_action(action, agent, target)

				if target.has_card(Influence.Captain):
					# target calls block with captain
					if random.randint(0, 3) == 0:
						bluff_sequence.append(BluffSequence(Actions.Steal, target, agent, False))
						agent.remove_card()
					# Action is blocked
				else:
					if random.randint(0, 3) == 0:
						# target bluffs that he has captain
						rand_int = random.randint(1, 4)
						if  random.randint(0, 3) > 1:
							# agent believes the bluff action happens
							action_sequence.append(ActionSequence(action, agent, target))
							self.actions.perform_action(action, agent, target)
						else:
							# agent calls the bluff
							target.remove_card()

		
		else:
			pass
			# Agent will possibly bluff a card

		return action_sequence, bluff_sequence
		'''
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
			'''
		'''
			if bluff == 0:
				# No bluff: pick one of the available card actions
				print("Agent chooses: no bluff")

				# Choose a random action for the available actions
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
		'''

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
		#print(self.turn_counter)
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
			for agent in self.players:
				if agent.is_alive():
					winner_id = agent.get_id()
			print("player {0} won the game!".format(winner_id))
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
	
	def reset_game(self):
		self.alive_agents = self.n_players
		self.players = list()
		self.turn_counter = 0
		self.deck = []
		self.make_deck()
		self.set_players()
		self.all_actions_active = ["tax", "steal", "swap_influence"]
		self.all_actions_reactive = ["block_foreign_aid", "block_assassination", "block_steal"]
		self.actions = Action()
		self.finished = False

