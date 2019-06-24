
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
		self.all_actions_active = [Actions.Tax, Actions.Steal, Actions.Assasinate, Actions.Income, Actions.Tax, Actions.Foreign_Aid]
		self.all_actions_reactive = [Actions.Block_Assasinate, Actions.Block_Foreign_Aid, Actions.Block_Steal]
		self.actions = Action()
		self.finished = False
		self.model = KripkeModel(n_players, [Influence.Assassin, Influence.Contessa, Influence.Captain, Influence.Duke])
	#	self.model = KripkeModel(n, ['assassin', 'countessa', 'captain', 'duke'])

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

	def remove_card_and_update_model(self, player):
		card = player.remove_card()
		self.model.flip_card(player.identifier, card.influence)

	def perform_action_and_update_model(self, action, agent, target):
		if action == Actions.Assasinate or action == Actions.Coup:
			card = self.actions.perform_action(action, agent, target)	
			self.model.flip_card(target.identifier, card.influence)
		else:
			self.actions.perform_action(action, agent, target)	
		

	"""
	def get_influencecards(self, agent):
		all_
		alive_cards = agent.cards 
		dead_cards = agent.dead_cards 
	"""
						
	def choose_action(self, agent):
		action_sequence = []
		bluff_sequence = []
		cards = [x.influence for x in agent.cards]

		# If agent has enough coins to coup it will
		if agent.coins >= 7:
			action = Actions.Coup
			target =  self.get_random_target(agent)
			action_sequence.append(ActionSequence(action, agent, target))
			#self.actions.perform_action(action, agent, target)
			self.perform_action_and_update_model(action, agent, target)
			return action_sequence, bluff_sequence
		
		# Determine the possible active and reactive actions for the agent
		possible_actions_active = []
		possible_actions_active.append(Actions.Income)
		#possible_actions_active.append(Actions.Foreign_Aid)
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
			#action = Actions.Tax
			if action == Actions.Income:
				action_sequence.append(ActionSequence(action, agent, None))
				self.actions.perform_action(action, agent)

			elif action == Actions.Foreign_Aid:
				# Random target will bluff having duke if he doesn't have it
				if  random.randint(0, 3) == 0:
					caller = self.get_random_target(agent)
				else:
					caller = None
					for player in self.players:
						if player.identifier == agent.identifier or not player.is_alive():
							continue
						if player.has_card(Influence.Duke):
							caller = player
							break
							
				if caller is None:
					# No target can block
						action_sequence.append(ActionSequence(action, agent, None))
						self.actions.perform_action(action, agent)
						return action_sequence, bluff_sequence

				if  random.randint(0, 3) > 1:
					# Agent believes target
					action_sequence.append(ActionSequence(action, agent, caller, Actions.Block_Foreign_Aid))
					bluff_sequence.append(BluffSequence(Actions.Block_Foreign_Aid, caller, agent, False, True))
				else:
					# Agent doesn't believe target
					if caller.has_card(Influence.Duke):
						# Wrongly called bluff
						action_sequence.append(ActionSequence(action, agent, caller, Actions.Block_Foreign_Aid))
						bluff_sequence.append(BluffSequence(Actions.Block_Foreign_Aid, caller, agent, False, False))
						agent.remove_card()
					else:
						# Correctly called bluff on target
						bluff_sequence.append(BluffSequence(Actions.Block_Foreign_Aid, caller, agent, True, False))
						caller.remove_card()
						action_sequence.append(ActionSequence(action, agent, caller, Actions.Block_Foreign_Aid))
						self.actions.perform_action(action, agent)
			
						
			elif action == Actions.Tax:
				for player in self.players:
					if player.identifier != agent.identifier:
						#self.model = KripkeModel(n_players, [Influence.Assassin, Influence.Contessa, Influence.Captain, Influence.Duke])
						
						#cards = [x.influence for x in player.cards]
						call = self.model.query(cards, player.identifier, agent.identifier, True, Influence.Duke)
						if call == True:
							#player.remove_card()
							self.remove_card_and_update_model(player)
							action_sequence.append(ActionSequence(action, agent, None))
							bluff_sequence.append(BluffSequence(action, agent, player, False, False))
							self.actions.perform_action(action, agent)
							#print("True")
						else:
							action_sequence.append(ActionSequence(action, agent, None))
							continue
							#print("False")
						#def query(self, cards_player, player, opponent, boolean, card):
				"""
				if random.randint(0, 3) == 0:
					# Random player wrongfully called bluff


					bluff_caller = self.get_random_target(agent)
					bluff_caller.remove_card()
					action_sequence.append(ActionSequence(action, agent, None))
					bluff_sequence.append(BluffSequence(action, agent, bluff_caller, False, False))
					self.actions.perform_action(action, agent)
				else:
					# No bluff was called
					action_sequence.append(ActionSequence(action, agent, None))
					self.actions.perform_action(action, agent)
				"""


			elif action == Actions.Assasinate:

				target = self.get_random_target(agent)
				if target.has_card(Influence.Contessa):
					# target calls block with countessa
					"""
					if random.randint(0, 3) == 0:
						# agent wrongfully calls bluff
						bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, False, False))
						agent.remove_card()

					"""
					#cards = [x.influence for x in agent.cards]
					call = self.model.query(cards, agent.identifier, target.identifier, True, Influence.Contessa)
					if call == True:
						# Agent knows that target has a contessa
						bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, False, True))

					else:
						# Agent doesn't know that the target has a contessa
						# TODO: HERE WE HAVE TO ADD BELIEF TO MAKE THE GAME BETTER
						bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, False, False))
						self.remove_card_and_update_model(agent)
					
					action_sequence.append((ActionSequence(action, agent, target, Actions.Block_Assasinate)))
				else:
					# Target cant't block card: has to choose something else to do

					"""
					rand_int = random.randint(1, 3)
					if   rand_int == 1:
						# target bluffs that he has contessa
						if random.randint(0, 3) > 1:
							# Agent believes the bluff; loses coins and performs no action
							agent.remove_coins(3)
							action_sequence.append((ActionSequence(action, agent, target, Actions.Block_Assasinate)))
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, True))
						else:
							# Correctly called bluff so remove card of target
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, False))
							target.remove_card()
							action_sequence.append(ActionSequence(action, agent, target, Actions.Block_Assasinate))
							self.actions.perform_action(action, agent, target)
					"""	
					call = self.model.query(cards, target.identifier, agent.identifier, True, Influence.Assassin)
					# Target checks if he knows that agent has an Assassin
					if call == True:
						# Target knows that agent has an assassin: let's the assassinate happen
						action_sequence.append(ActionSequence(action, agent, target))
						bluff_sequence.append(BluffSequence(action, agent, target, False, True))
						self.actions.perform_action(action, agent, target)	
					if call == False:
						# Target doesn't know that agent has an assassin:
						rand_int = random.randint(1, 2)
						if rand_int == 1:
							# Target bluffs that he has contessa
							call = self.model.query(cards, agent.identifier, target.identifier, True, Influence.Contessa)
							# Agent checks to see whether he knows that target has a Contessa
							if call == True:
								# Agent knows that target has Contessa: 
								agent.remove_coins(3)
								action_sequence.append((ActionSequence(action, agent, target, Actions.Block_Assasinate)))
								bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, True))
							else:
								# Agent doesn't know that target has Contessa: rightfully calls the bluff
								bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, False))
								#target.remove_card()
								self.remove_card_and_update_model(target)
								action_sequence.append(ActionSequence(action, agent, target, Actions.Block_Assasinate))
								#self.actions.perform_action(action, agent, target)		
								self.perform_action_and_update_model(action, agent, target)		

						if rand_int == 2:
							# Target wrongly calls bluff on assassin

							bluff_sequence.append(BluffSequence(action, agent, target, False, False))
							#target.remove_card()
							self.remove_card_and_update_model(target)
							action_sequence.append(ActionSequence(action, agent, target))
						#	self.actions.perform_action(action, agent, target)
							self.perform_action_and_update_model(action, agent, target)


					"""
					rand_int = random.randint(1, 3)
					if rand_int == 1:
						# Target bluffs that he has contessa
						call = self.model.query(cards, agent.identifier, target.identifier, True, Influence.Contessa)
						if call == True:
							# Agent knows that target has a contessa: believes the bluff
							agent.remove_coins(3)
							action_sequence.append((ActionSequence(action, agent, target, Actions.Block_Assasinate)))
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, True))
						else:
							# Agent doesn't know that target has contessa
							# Correctly calls it
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, False))
							#target.remove_card()
							self.remove_card_and_update_model(target)
							action_sequence.append(ActionSequence(action, agent, target, Actions.Block_Assasinate))
							self.actions.perform_action(action, agent, target)							

					elif rand_int == 2:
						# Target wrongly calls bluff on assinate

						bluff_sequence.append(BluffSequence(action, agent, target, False, False))
						target.remove_card()
						action_sequence.append(ActionSequence(action, agent, target))
						self.actions.perform_action(action, agent, target)

					elif rand_int == 3:
						# Call no bluff; let action through
						action_sequence.append(ActionSequence(action, agent, target))
						bluff_sequence.append(BluffSequence(action, agent, target, False, True))
						self.actions.perform_action(action, agent, target)
					"""

			elif action == Actions.Steal:
		#	elif action == Actions.Assasinate:

				target = self.get_random_target(agent)
				if target.has_card(Influence.Captain):
					# target calls block with captain
					"""
					if random.randint(0, 3) == 0:
						# agent wrongfully calls bluff
						bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, False, False))
						agent.remove_card()

					"""
					#cards = [x.influence for x in agent.cards]
					call = self.model.query(cards, agent.identifier, target.identifier, True, Influence.Captain)
					if call == True:
						# Agent knows that target has a captain
						bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, False, True))

					else:
						# Agent doesn't know that the target has a captain
						# TODO: HERE WE HAVE TO ADD BELIEF TO MAKE THE GAME BETTER
						bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, False, False))
						self.remove_card_and_update_model(agent)
					
					action_sequence.append((ActionSequence(action, agent, target, Actions.Block_Steal)))
				else:
					# Target cant't block card: has to choose something else to do

					"""
					rand_int = random.randint(1, 3)
					if   rand_int == 1:
						# target bluffs that he has contessa
						if random.randint(0, 3) > 1:
							# Agent believes the bluff; loses coins and performs no action
							agent.remove_coins(3)
							action_sequence.append((ActionSequence(action, agent, target, Actions.Block_Assasinate)))
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, True))
						else:
							# Correctly called bluff so remove card of target
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, False))
							target.remove_card()
							action_sequence.append(ActionSequence(action, agent, target, Actions.Block_Assasinate))
							self.actions.perform_action(action, agent, target)
					"""	
					call = self.model.query(cards, target.identifier, agent.identifier, True, Influence.Captain)
					# Target checks if he knows that agent has an Captain
					if call == True:
						# Target knows that agent has an assassin: let's the assassinate happen
						action_sequence.append(ActionSequence(action, agent, target))
						bluff_sequence.append(BluffSequence(action, agent, target, False, True))
						self.actions.perform_action(action, agent, target)	
					if call == False:
						# Target doesn't know that agent has an assassin:
						rand_int = random.randint(1, 2)
						if rand_int == 1:
							# Target bluffs that he has captain
							call = self.model.query(cards, agent.identifier, target.identifier, True, Influence.Captain)
							# Agent checks to see whether he knows that target has a Contessa
							if call == True:
								# Agent knows that target has Captain: 
								action_sequence.append((ActionSequence(action, agent, target, Actions.Block_Steal)))
								bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, True, True))
							else:
								# Agent doesn't know that target has Captain: rightfully calls the bluff
								bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, True, False))
								#target.remove_card()
								self.remove_card_and_update_model(target)
								action_sequence.append(ActionSequence(action, agent, target, Actions.Block_Steal))
								#self.actions.perform_action(action, agent, target)		
								self.perform_action_and_update_model(action, agent, target)		

						if rand_int == 2:
							# Target wrongly calls bluff on Captain

							bluff_sequence.append(BluffSequence(action, agent, target, False, False))
							#target.remove_card()
							self.remove_card_and_update_model(target)
							action_sequence.append(ActionSequence(action, agent, target))
						#	self.actions.perform_action(action, agent, target)
							self.perform_action_and_update_model(action, agent, target)
						




		
		else:
			# Possibly bluff an action
			all_actions_active = self.all_actions_active.copy()
			agent.coins = 0
			if agent.coins < 3:
				all_actions_active.remove(Actions.Assasinate)
			action = random.choice(all_actions_active)

			if action in possible_actions_active:
				valid_action = True
			else:
				valid_action = False

			if action == Actions.Income:
				action_sequence.append(ActionSequence(action, agent, None))
				self.actions.perform_action(action, agent)

			elif action == Actions.Foreign_Aid:
				# Random target will bluff having duke if he doesn't have it
				if  random.randint(0, 3) == 0:
					caller = self.get_random_target(agent)
				else:
					caller = None
					for player in self.players:
						if player.identifier == agent.identifier or not player.is_alive():
							continue
						if player.has_card(Influence.Duke):
							caller = player
							break
							
				if caller is None:
					# No target can block
						action_sequence.append(ActionSequence(action, agent, None))
						self.actions.perform_action(action, agent)
						return action_sequence, bluff_sequence

				if  random.randint(0, 3) > 1:
					# Agent believes target
					action_sequence.append(ActionSequence(action, agent, caller, Actions.Block_Foreign_Aid))
					bluff_sequence.append(BluffSequence(Actions.Block_Foreign_Aid, caller, agent, False, True))
				else:
					# Agent doesn't believe target
					if caller.has_card(Influence.Duke):
						# Wrongly called bluff
						action_sequence.append(ActionSequence(action, agent, caller, Actions.Block_Foreign_Aid))
						bluff_sequence.append(BluffSequence(Actions.Block_Foreign_Aid, caller, agent, False, False))
						agent.remove_card()
					else:
						# Correctly called bluff on target
						bluff_sequence.append(BluffSequence(Actions.Block_Foreign_Aid, caller, agent, True, False))
						caller.remove_card()
						action_sequence.append(ActionSequence(action, agent, caller, Actions.Block_Foreign_Aid))
						self.actions.perform_action(action, agent)
			
			elif action == Actions.Tax:
				action_sequence.append(ActionSequence(action, agent, None))
				if random.randint(0, 3) == 0:
					# Random player calls bluff
					bluff_caller = self.get_random_target(agent)
					if valid_action:
						# Wrongly called bluff
						bluff_caller.remove_card()
						bluff_sequence.append(BluffSequence(action, agent, bluff_caller, False, False))
						self.actions.perform_action(action, agent)
					else:
						# Called bluff correctly
						agent.remove_card()
						bluff_sequence.append(BluffSequence(action, agent, bluff_caller, True, False))
					
				else:
					# No bluff was called
					self.actions.perform_action(action, agent)

			elif action == Actions.Assasinate:
				target = self.get_random_target(agent)
				if target.has_card(Influence.Contessa):
					# target calls block with countessa
					if random.randint(0, 3) == 0:
						# agent wrongfully calls bluff
						bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, False, False))
						agent.remove_card()
					# Agent doesn't calll bluff so action is blocked
					else:
						bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, False, True))
					action_sequence.append((ActionSequence(action, agent, target, Actions.Block_Assasinate)))
				else:
					# Target cant't block card
					rand_int = random.randint(1, 3)
					if   rand_int == 1:
						# target bluffs that he has contessa
						if random.randint(0, 3) > 1:
							# Agent believes the bluff; loses coins and performs no action
							agent.remove_coins(3)
							action_sequence.append((ActionSequence(action, agent, target, Actions.Block_Assasinate)))
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, True))
						else:
							# Correctly called bluff so remove card of target
							bluff_sequence.append(BluffSequence(Actions.Block_Assasinate, target, agent, True, False))
							target.remove_card()
							action_sequence.append(ActionSequence(action, agent, target, Actions.Block_Assasinate))
							self.actions.perform_action(action, agent, target)
					elif rand_int == 2:
							# Target calls bluff on action
						if valid_action:
							# Wrongly called bluff
							target.remove_card()
							bluff_sequence.append(BluffSequence(action, agent, target, False, False))
							self.actions.perform_action(action, agent, target)
						else:
							# Called bluff correctly
							agent.remove_card()
							bluff_sequence.append(BluffSequence(action, agent, target, True, False))						
		
					elif rand_int == 3:
						# Call no bluff; let action through
						action_sequence.append(ActionSequence(action, agent, target))
						bluff_sequence.append(BluffSequence(action, agent, target, False, True))
						self.actions.perform_action(action, agent, target)	

			elif action == Actions.Steal:
				target = self.get_random_target(agent)
				if target.has_card(Influence.Captain):
					# target calls block with Captain
					if random.randint(0, 3) == 0:
						# agent wrongfully calls bluff
						bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, False, False))
						agent.remove_card()
					# Action is blocked
					else:
						bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, False, True))
					action_sequence.append(ActionSequence(action, agent, target, Actions.Block_Steal))
				else:
					# Target cant't block card
					rand_int = random.randint(1, 3)
					if  rand_int == 1:
						# target bluffs that he has Captain
						if random.randint(0, 3) > 1:
							# Agent believes the bluff and performs no action
							action_sequence.append(ActionSequence(action, agent, target, Actions.Block_Steal))
							bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, True, True))
						else:
							# Correctly called bluff so remove card of target
							bluff_sequence.append(BluffSequence(Actions.Block_Steal, target, agent, True, False))
							target.remove_card()
							action_sequence.append(ActionSequence(action, agent, target, Actions.Block_Steal))
							self.actions.perform_action(action, agent, target)
					elif rand_int == 2:
							# Target calls bluff on action
						if valid_action:
							# Wrongly called bluff
							target.remove_card()
							bluff_sequence.append(BluffSequence(action, agent, target, False, False))
							self.actions.perform_action(action, agent, target)
						else:
							# Called bluff correctly
							agent.remove_card()
							bluff_sequence.append(BluffSequence(action, agent, target, True, False))						
		
					elif rand_int == 3:						
						# Captain wasn't bluffed
						action_sequence.append(ActionSequence(action, agent, target))
						bluff_sequence.append(BluffSequence(action, agent, target, False, True))
						self.actions.perform_action(action, agent, target)

		print("Agent {} chose action {} with action_seq len {}and bluff_seq len {}".format(agent.identifier, action, len(action_sequence), len(bluff_sequence)))
		return action_sequence, bluff_sequence
		'''
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

		self.finished = False

