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
                color = "red"
            else:
                color = "green"
            player_frame = tk.Frame(game_frame, width=self.player_w, bg=color, bd=4, height=400)
            player_frame.grid(row=1, column=i+1, sticky="ew")
           # player_frame.grid_propagate(False)
            self.player_frames.append(player_frame)

        game_frame.rowconfigure(0, weight=1)
        game_frame.columnconfigure(0, weight=1)
        game_frame.columnconfigure(self.game.n_players+1, weight=1)

    def update(self):
        self.set_players()
        self.turn()
        self.after(100, self.update)



    def set_players(self):
        i = 0
        for player_frame, player in zip(self.player_frames, self.game.players):
            for child in player_frame.winfo_children():
                child.destroy()
            i += 1
            tk.Label(player_frame, text="Player {}".format(i)).grid(row=1, column=1)

            dead_cards = 2 - len(player.cards)

            col = 1
            for card in player.cards:
                tk.Label(player_frame, image=self.load_image(self.card_image_path(card.influence), size=(175, 250))).grid(row=2, column=col)
                col += 1
                
            
            for j in range(0, dead_cards):
                tk.Label(player_frame, image=self.load_image(self.card_image_path("dead"), size=(175, 250))).grid(row=2, column=col)
                col += 1

           # coin_frame = tk.Frame(player_frame, width=self.player_w, height=50, bg="yellow").grid(row=3, column=1)
           # tk.Label(coin_frame, text=player.coins).grid(row=1, column=1)
           # tk.Label(coin_frame, image=self.load_image("images/coin.jpg", size=(25,25))).grid(row=1, column=1)
        

    def turn(self):
        agent = self.game.get_next_agent()

        print("Agent", agent.get_identifier(), "turn:")
        print("Alive = {0}".format(agent.alive))
        print("Coins:", agent.get_coins())
        print("Cards:")
        for card in agent.get_cards():
            print(card.get_influence())

        self.game.choose_action(agent)
        print("\n")


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