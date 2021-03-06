from Coup import Coup
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from Enums import Influence, Actions

class MainApplication(tk.Frame):
    def __init__(self, root, game, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky="nsew")
        # Setup root configure
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)	
        self.img_ref = []
        self.game = game
        # Game fields
        self.pause = False
        self.turn_count = 1
        self.card_size = (181, 250)
        self.game_speed = 1000
        # Width for player frames
        self.player_w = self.root.winfo_width() / self.game.n_players
        
        self.initUI()
        # Run update to run the update loop that keeps the game played
        self.update()

    def initUI(self):
        # Set mainframe config
        self.master.title("Coup Project")      
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(self.game.n_players+1, weight=1)

        # Initialize the top frame that contains buttons and turn info
        top_frame = tk.Frame(self.mainframe, width=self.root.winfo_width() , height=100)
        top_frame.grid(row=1, column=1, sticky="ew")
        # Game label
        tk.Label(top_frame, text="Coup Game v1.0", font=("Arial", 22)).grid(row=1, column=1, sticky="EW")
        # Button that pauses the game
        pause_button = tk.Button(top_frame, text="Pause")
        pause_button.bind("<Button-1>", self.pause_game)
        pause_button.grid(row=1, column=2, sticky="EW")
        # Button that resets the game
        reset_button = tk.Button(top_frame, text="Reset")
        reset_button.bind("<Button-1>", self.reset_game)
        reset_button.grid(row=1, column=3, sticky="EW")
        # Label that manages the turn count
        self.turn_count_label = tk.Label(top_frame, text="Turn: 1", font=("Arial", 14))
        self.turn_count_label.grid(row=1, column=4, sticky="E")

        self.world_count_label = tk.Label(top_frame, text="Worlds:" + str(self.game.model.count_worlds()), font=("Arial", 14))
        self.world_count_label.grid(row=1, column=5, sticky="E")

        self.relation_count_label = tk.Label(top_frame, text="Relations: " +str(self.game.model.count_relations()), font=("Arial", 14))
        self.relation_count_label.grid(row=1, column=6, sticky="E")

        # Setup the game frame
        game_frame = tk.Frame(self.mainframe, bg='#DDDFDF', width=self.root.winfo_width(), height=700)     
        game_frame.grid(row=2, column=1, sticky="ew")
        # Configure frame to have content centered using empty columns to left and right
        game_frame.rowconfigure(0, weight=1)
        game_frame.columnconfigure(0, weight=1)
        game_frame.columnconfigure(self.game.n_players+1, weight=1)
        # Setup frames for every player
        self.player_frames = []
        for i in range(self.game.n_players):
            # striped coloring
            if i % 2 == 0:
                color = "#D5D3CC"
            else:
                color = "#E7E6E2"
            player_frame = tk.Frame(game_frame, width=self.player_w, bg=color, bd=2, relief = "groove",  height=400)
            player_frame.grid(row=1, column=i+1, sticky="ew")
            self.player_frames.append(player_frame)

        # Initialize every player frame
        i = 0
        self.player_cards = []
        self.coin_labels = []
        self.current_player_labels = []
        self.action_texts = []
        for player_frame, player in zip(self.player_frames, self.game.players):
            if i % 2 == 0:
                color = "#D5D3CC"
            else:
                color = "#E7E6E2"

            # Player label
            tk.Label(player_frame, text="Player {}".format(i+1), bg=color, font=("Helvetica", 13)).grid(row=1, column=1, sticky="news")
            
            # Initialize card images
            current_cards = []
            for j, card in enumerate(player.cards):
                card_image = tk.Label(player_frame, image=self.load_image(self.card_image_path(card.influence), size=self.card_size))
                card_image.grid(row=2, column=j+1)
                current_cards.append(card_image)
                
            # Initialize coin frame
            self.player_cards.append(current_cards)
            coin_frame = tk.Frame(player_frame, width=150, height=50, bg="#fdeca6")
            coin_frame.grid(row=3, column=1, columnspan=2, sticky="nsew")
            # Coin labels 
            coin_label = tk.Label(coin_frame, text=player.coins, font=("Helvetica", 11),  bg="#fdeca6")
            coin_label.grid(row=1, column=1)
            self.coin_labels.append(coin_label)
            # Coin image label
            tk.Label(coin_frame, image=self.load_image("images/coin.jpg", size=(25,25)), bg="#fdeca6").grid(row=1, column=2, sticky="nw")

            # Initialize action frame that contains gameplay text
            action_frame = tk.Frame(player_frame, width=50, height=200)
            action_frame.grid(row=4, column=1, columnspan=2, sticky="nsew")
            # Use propagate to keep width of textbox to parent frame
            action_frame.grid_propagate(0)
            # Gameplay text
            action_text = tk.Text(action_frame)
            action_text.grid(row=1, column=1, sticky="nsew")

            self.action_texts.append(action_text) 
            i += 1

        bottom_frame = tk.Frame(self.mainframe, width=self.root.winfo_width(), height = 900)     
        bottom_frame.grid(row=3, column=1, sticky="nsew")
        self.game_console =  tk.Text(bottom_frame)
        self.game_console.grid(row=1, column=1, columnspan=3, sticky="nsew")
        scroll = tk.Scrollbar(bottom_frame)
        self.game_console.configure(yscrollcommand=scroll.set)
	
        
    def pause_game(self, event):
        # Set the pause to the opposite of it's current value
        if self.pause:
            self.pause = False
        else:
            self.pause = True

    
    def reset_game(self, event):
        # Reset game and turn count and update the game 
        self.game.reset_game()
        self.turn_count = 0
        self.update()

    def update(self):
        if not self.pause:
            self.turn_count += 1
            self.turn_count_label.config(text="Turn: "+ str(self.turn_count))
            self.update_players()
            game.is_finished()
            if game.finished:
                # Stop the repeating loop when game is finished by return before .after
               # self.update_players(finished=True)
                return

        self.after(self.game_speed, self.update)

    def update_players(self, finished=False):
        self.world_count_label.config(text="Worlds: "+str(self.game.model.count_worlds()))
        self.relation_count_label.config(text="Relations: "+str(self.game.model.count_relations()))
        # Get the agent whos turn it is

        agent = self.game.get_next_agent()
        action_counter = 0

        for i, action_text in enumerate(self.action_texts):
            if i == agent.identifier:
                action_text.delete(1.0, tk.END)
                self.game_console.insert(tk.END, "Player {}'s turn\n".format(i))
    
                action_text.insert(tk.END, "Player's turn\n")
            else:
                action_text.delete(1.0, tk.END)

        action_seq, bluff_seq = self.game.choose_action(agent)

        perform_action = True
        for action_info in action_seq:
            action_counter += 1
            print(action_info.action_string(action_counter))
            self.game_console.insert(tk.END, action_info.action_string(action_counter))
            self.action_texts[action_info.agent.identifier].insert(tk.END, action_info.action_string(action_counter))
            if action_info.target is not None:
                action_counter += 1
                print(action_info.target_string(action_counter))
                self.game_console.insert(tk.END, action_info.target_string(action_counter))
                self.action_texts[action_info.target.identifier].insert(tk.END, action_info.target_string(action_counter))
                if action_info.block_action is not None:
                    action_counter += 1
                    if action_info.action is Actions.Foreign_Aid:
                        action_counter -= 1
                    print(action_info.block_string(action_counter))
                    self.game_console.insert(tk.END,action_info.block_string(action_counter))
             
                    self.action_texts[action_info.target.identifier].insert(tk.END, action_info.block_string(action_counter))
                    perform_action = False
                else:
                    if action_info.action is not Actions.Coup:
                        action_counter += 1
                        self.game_console.insert(tk.END,"{}. Player does not block the action\n".format(action_counter))
             
                        print("{}. Player does not block the action\n".format(action_counter))
                        self.action_texts[action_info.target.identifier].insert(tk.END, "{}. Player does not block the action\n".format(action_counter))

            if len(bluff_seq) > 0:
                bluff_info = bluff_seq[0]

                self.game_console.insert(tk.END, bluff_info.result_string(action_counter))
             
                print(bluff_info.result_string(action_counter))
                action_counter += 1
                
                self.action_texts[bluff_info.bluff_caller.identifier].insert(tk.END, bluff_info.agent_string(action_counter))
                if bluff_info.belief is not True:
                    action_counter += 1
                    print(bluff_info.agent_string(action_counter))
                    self.game_console.insert(tk.END, bluff_info.agent_string(action_counter))
             
                    self.action_texts[bluff_info.bluff_caller.identifier].insert(tk.END, bluff_info.result_string(action_counter))
                if bluff_info.bluff and not bluff_info.belief:
                    # Bluff called correctly
                    perform_action = False
                elif bluff_info.bluff and bluff_info.belief:
                     perform_action = False


            if perform_action:
                action_counter += 1
                self.game_console.insert(tk.END, "{}. Player performs action\n".format(action_counter))
             
                print("{}. Player performs action\n".format(action_counter))
                self.action_texts[action_info.agent.identifier].insert(tk.END, "{}. Player performs action\n".format(action_counter))
            self.game_console.insert(tk.END, "\n-------------------------------\n")
            
            print("\n\n\n")

        # Update every player frame
        for player, coin_label, card_labels, action_text in zip(self.game.players, self.coin_labels, self.player_cards, self.action_texts):

            # Update the cards with the dead cards
            i = 0
            for card in player.cards:
                card_labels[i].config(image=self.load_image(self.card_image_path(card.influence), size=self.card_size))
                i += 1
            if i < 2:
                for card in player.dead_cards:
                    card_labels[i].config(image=self.load_image(self.card_image_path(card.influence, dead=True), size=self.card_size))
                    i += 1

            coin_label.config(text=player.coins)
        game.is_finished()
        if game.finished:
            for player in game.players:
                if player.is_alive():
                    self.game_console.insert(tk.END, "*************Player won the game*************\n")
                    self.action_texts[player.identifier].insert(tk.END, "*************Player won the game*************\n")
                    return



    def load_image(self, path, size=None):
        # Loads an image and resizes it to the given size
        image = Image.open(path)
        if size is not None:
            image = image.resize(size, Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        # Img ref is needed to display multiple images
        self.img_ref.append(image)
        return image
        
    def card_image_path(self, influence, dead=False):
        # Returns the path for the card name"
        if dead:
            path = "images/dead_"
        else:
            path = "images/"

        if influence is Influence.Ambassador:
            return path+"ambassador.png"
        elif influence is Influence.Assassin:
            return path+"assassin.jpg"
        elif influence is Influence.Captain:
            return path+"captain.jpg"
        elif influence is Influence.Contessa:
            return path+"contessa.jpg"
        elif influence is Influence.Duke:
            return path+"duke.jpg"

        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1600x900')
    root.update()

    game = Coup(3)

    MainApplication(root,  game).grid()
    root.mainloop()