
from Agent import Agent
from Action import Action
import random

class Coup:
    def __init__(self, n_players):
        self.n_players = n_players
        self.players = list()
        self.turn_counter = 0
        self.deck = ["ambassador", "ambassador", "ambassador", "assassin", "assassin","assassin", "captain", "captain","captain", "countessa","countessa","countessa", "duke", "duke", "duke"]
        self.set_players()

    def deal_card(self):
    	random.shuffle(self.deck)
    	card = self.deck.pop()
    	return card

    def set_players(self):
        for i in range(self.n_players):
            property1, property2, property3 = 1, 2, 3
            self.players.append(Agent(property1, property2, property3))
        for player in self.players:
            card = self.deal_card()
            player.add_card(card)
            card = self.deal_card()  
            player.add_card(card)
            	        	
    def choose_action(self, agent):
    	#self.deal_card()
    	bluff = 0
    	rand_int = random.randint(1, 4)
    	if rand_int >= 4:
    		bluff = 1

    	if bluff == 0:
    		# No bluff: pick one of the available card actions
    		print("no bluff")
    	else:
    		# Bluff: pick a random action
    		print("bluff")


    def get_next_agent(self):
    	agent = self.players[self.turn_counter]
    	self.turn_counter += 1

    	if self.turn_counter >= self.n_players:

    		self.turn_counter = 0
    	return agent


    def get_players(self):
    	return self.players