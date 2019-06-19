from Coup import Coup
import tkinter as tk
from PIL import Image, ImageTk

class MainApplication(tk.Frame):
    def __init__(self, root, game, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.game = game
        self.img_ref = []
        self.initUI()
        self.update()

    def initUI(self):
        self.master.title("Coup Project")
        window_w = self.root.winfo_width()
        root.columnconfigure(1, weight=1)

        title_frame = tk.Frame(self.root, bg="#F4EBE8", bd=10, width=window_w, height=100)
        game_frame = tk.Frame(self.root, bg='#DDDFDF', width=window_w, height=700)

        title_frame.grid(row=1, column=1, sticky="ew")
        game_frame.grid(row=2, column=1, sticky="ew")
        
        tk.Label(title_frame, text="Coup Game v1.0", bg='#F4EBE8', font=("Helvetica ", 22)).grid(sticky="EW")
        
        self.player_frames = []
        for i in range(self.game.n_players):
            if i % 2 == 0:
                color = "red"
            else:
                color = "green"

            if i == 0:
                sticky = "nw"
            elif i == self.game.n_players:
                sticky= "ew"
            else:
                sticky = "n"

            player_frame = tk.Frame(game_frame, width=window_w/self.game.n_players, bg=color, bd=4, height=400)
            player_frame.grid(row=1, column=i+1, sticky=sticky)
            self.player_frames.append(player_frame)


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
            for j, card in enumerate(player.cards):
                tk.Label(player_frame, image=self.load_image(self.card_image_path(card.influence), size=(175, 250))).grid(row=2, column=j+1)
            tk.Label(player_frame, text=player.coins).grid(row=3, column=1, sticky="w")
            tk.Label(player_frame, image=self.load_image("images/coin.jpg", size=(25,25))).grid(row=3, column=2, sticky="w")
        

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
        return "images/duke.jpg"
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1600x900')
    root.update()

    game = Coup(4)

    MainApplication(root,  game).grid()
    root.mainloop()