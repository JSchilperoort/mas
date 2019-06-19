# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk
from PIL import Image, ImageTk

class MainApplication(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.img_ref = []
        self.initUI()

    def initUI(self):
        self.master.title("Coup Project")
        window_w = self.root.winfo_width()
        root.columnconfigure(1, weight=1)

        title_frame = tk.Frame(self.root, bg="#F4EBE8", bd=10, width=window_w, height=100)
        game_frame = tk.Frame(self.root, bg='#DDDFDF', width=window_w, height=700)

        title_frame.grid(row=1, column=1, sticky="ew")
        game_frame.grid(row=2, column=1, sticky="ew")
        
        tk.Label(title_frame, text="Coup Game v1.0", bg='#F4EBE8', font=("Helvetica ", 22)).grid(sticky="EW")
        
        n_players = 4
        player_frames = []
        for i in range(n_players):
            if i % 2 == 0:
                color = "red"
            else:
                color = "green"

            if i == 0:
                sticky = "nw"
            elif i == n_players:
                sticky= "ew"
            else:
                sticky = "n"

            player_frame = tk.Frame(game_frame, width=window_w/n_players, bg=color, bd=4, height=400)
            player_frame.grid(row=1, column=i+1, sticky=sticky)
            player_frames.append(player_frame)

        for i, player_frame in enumerate(player_frames):
            tk.Label(player_frame, text="Player {}".format(i+1)).grid(row=1, column=1)
            tk.Label(player_frame, image=self.load_image("images/duke.jpg", size=(175, 250))).grid(row=2, column=1)
            tk.Label(player_frame, image=self.load_image("images/duke.jpg", size=(175, 250))).grid(row=2, column=2)
            tk.Label(player_frame, text="10").grid(row=3, column=1, sticky="w")
            tk.Label(player_frame, image=self.load_image("images/coin.jpg", size=(25,25))).grid(row=3, column=2, sticky="w")

    def load_image(self, path, size=None):
        image = Image.open(path)
        if size is not None:
            image = image.resize(size, Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        self.img_ref.append(image)
        return image
        
        



        



        


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1600x900')
    root.update()
    MainApplication(root).grid()
    root.mainloop()