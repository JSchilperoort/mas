import sys
from Coup import Coup

def main(argv):

	n_players = 2
	game = Coup(n_players)

	print_game(game)

	n_turns = 10

	for i in range(0, n_turns):
		turn(game)

def turn(game):
	agent = game.get_next_agent()
	game.choose_action(agent)

def print_game(game):
	print("Number of players: ", game.n_players)
	players = game.get_players()
	i = 0
	for player in players:
		i += 1
		print("Player", i, "cards:", player.get_cards())

if __name__ == "__main__":
	main(sys.argv)
