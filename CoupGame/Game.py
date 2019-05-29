import sys
from Coup import Coup


def main(argv):

	n_players = 6
	n_games = 5

	for i in range(0, n_games):
		game = Coup(n_players)

		print_game(game)

		n_turns = 100

		# for i in range(0, n_turns):
		while not game.finished:
			turn(game)
			game.remove_dead_players()
		input()


def turn(game):
	agent = game.get_next_agent()

	print("Agent", agent.get_identifier(), "turn:")
	print("Alive = {0}".format(agent.alive))
	print("Coins:", agent.get_coins())
	print("Cards:")
	for card in agent.get_cards():
		print(card.get_influence())
	#print("\n")
	game.choose_action(agent)
	print("\n")

def print_game(game):
	print("Number of players: ", game.n_players, "\n")
	players = game.get_players()
	i = 0
	for player in players:
		i += 1
		print("Player", i, "cards:")
		for card in player.get_cards():
			print(card.get_influence())
		print("\n")
		#print("Player", i, "cards:", player.get_cards())

if __name__ == "__main__":
	main(sys.argv)
