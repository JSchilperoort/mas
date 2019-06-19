# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk
from PIL import Image, ImageTk

class MainApplication(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
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

        n_players = 3
        player_frames = []
        for i in range(n_players):
            if i % 2 == 0:
                color = "red"
            else:
                color = "green"

            player_frame = tk.Frame(game_frame, width=window_w/n_players, bg=color, bd=4, height=400)
            player_frame.grid(row=1, column=i+1, sticky="NEW")
            player_frames.append(player_frame)

        #for player_frame in player_frames:
        player_frame = player_frames[0] 
        card_image = Image.open("images/duke.jpg")
        card_image = card_image.resize((175, 250), Image.ANTIALIAS)
        card_image = ImageTk.PhotoImage(card_image)

        tk.Label(player_frame, image=card_image).grid(row=1, column=1)
        tk.Label(player_frame, image=card_image).grid(row=1, column=2)



        



        


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1600x900')
    root.update()
    MainApplication(root).grid()
    root.mainloop()