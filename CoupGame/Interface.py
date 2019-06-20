from Coup import Coup
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import threading

class MainApplication(tk.Frame):
    def __init__(self, root, game, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)	
        self.game = game

        self.img_ref = []
        self.initUI()
        self.update()

    def initUI(self):
        self.master.title("Coup Project")
        window_w = self.root.winfo_width()
        self.player_w = window_w / self.game.n_players
        self.card_size = (181, 250)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(self.game.n_players+1, weight=1)
        title_frame = tk.Frame(self.mainframe, width=window_w, height=100)
        game_frame = tk.Frame(self.mainframe, bg='#DDDFDF', width=window_w, height=700)

        title_frame.grid(row=1, column=1, sticky="ew")
        game_frame.grid(row=2, column=1, sticky="ew")

        tk.Label(title_frame, text="Coup Game v1.0", font=("Arial", 22)).grid(sticky="EW")
        
        self.player_frames = []
        for i in range(self.game.n_players):
            if i % 2 == 0:
                color = "#D5D3CC"
            else:
                color = "#E7E6E2"
            player_frame = tk.Frame(game_frame, width=self.player_w, bg=color, bd=2, relief = "groove",  height=400)
            player_frame.grid(row=1, column=i+1, sticky="ew")
            self.player_frames.append(player_frame)

        game_frame.rowconfigure(0, weight=1)
        game_frame.columnconfigure(0, weight=1)
        game_frame.columnconfigure(self.game.n_players+1, weight=1)

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

            tk.Label(player_frame, text="Player {}".format(i+1), bg=color, font=("Helvetica", 13)).grid(row=1, column=1, sticky="news")
            
            current_cards = []
            for j, card in enumerate(player.cards):
                card_image = tk.Label(player_frame, image=self.load_image(self.card_image_path(card.influence), size=self.card_size))
                card_image.grid(row=2, column=j+1)
                current_cards.append(card_image)
                
            self.player_cards.append(current_cards)
            coin_frame = tk.Frame(player_frame, width=150, height=50, bg="#fdeca6")
            coin_frame.grid(row=3, column=1, columnspan=2, sticky="nsew")

            
            coin_label = tk.Label(coin_frame, text=player.coins, font=("Helvetica", 11),  bg="#fdeca6")
            coin_label.grid(row=1, column=1)
            self.coin_labels.append(coin_label)

            tk.Label(coin_frame, image=self.load_image("images/coin.jpg", size=(25,25)), bg="#fdeca6").grid(row=1, column=2, sticky="nw")

            action_frame = tk.Frame(player_frame, width=50, height=200)
            action_frame.grid(row=4, column=1, columnspan=2, sticky="nsew")
            action_frame.grid_propagate(0)
            action_text = tk.Text(action_frame)
            action_text.grid(row=1, column=1, sticky="nsew")
  
            self.action_texts.append(action_text) 
            i += 1
        

    def update(self):
        self.update_players()
        game.is_finished()
        if game.finished:
            self.update_players(finished=True)
            return

        self.after(1000, self.update)

    def update_players(self, finished=False):
        i = 0
        agent = self.game.get_next_agent()
        # TODO Add something to the winning player
        for player, coin_label, card_labels, action_text in zip(self.game.players, self.coin_labels, self.player_cards, self.action_texts):
            if i == agent.identifier:
                action_text.insert(tk.END, "Player's turn\nChosen action: ")
            else:
                action_text.delete(1.0, tk.END)
            if len(player.dead_cards) == 1:
                card_labels[0].config(image=self.load_image(self.card_image_path(player.cards[0].influence), size=self.card_size))
                card_labels[1].config(image=self.load_image(self.card_image_path("death"), size=self.card_size))
            elif len(player.dead_cards) == 2:
                card_labels[0].config(image=self.load_image(self.card_image_path("death"), size=self.card_size))
                card_labels[1].config(image=self.load_image(self.card_image_path("death"), size=self.card_size))

            coin_label.config(text=player.coins)
            
            i += 1
        action = self.game.choose_action(agent)
        self.action_texts[agent.identifier].insert(tk.END, action)


        



    def load_image(self, path, size=None):
        image = Image.open(path)
        if size is not None:
            image = image.resize(size, Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        self.img_ref.append(image)
        return image
        
    def card_image_path(self, name):
        if name is "ambassador":
            return "images/ambassador.png"
        elif name is "assassin":
            return "images/assasin.jpg"
        elif name is "captain":
            return "images/captain.jpg"
        elif name is "countessa":
            return "images/contessa.jpg"
        elif name is "duke":
            return "images/duke.jpg"
        elif name is "dead":
            return "images/dead.jpg"
        return "images/dead.jpg"
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1600x900')
    root.update()

    game = Coup(4)

    MainApplication(root,  game).grid()
    root.mainloop()