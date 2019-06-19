
"""
ZetCode Tkinter tutorial

The example draws lines on the Canvas.

Author: Jan Bodnar
Last modified: April 2019
Website: www.zetcode.com
"""

import tkinter as tk
from PIL import Image, ImageTk
import os

class Application(tk.Frame):

    def __init__(self, root):
        super().__init__()
        self.root = root
        self.initUI()


    def initUI(self):
        self.master.title("Coup Project")
        # #F4EBE8

        w = self.winfo_width()
        title_frame = tk.Frame(self.root, bg='black', width=w, height=50)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        title_frame.grid(row=0)
    '''
        # create all of the main containers
        top_frame = tk.Frame(self.root, bg='cyan', width=450, height=50, pady=3)
        center = tk.Frame(self.root, bg='gray2', width=50, height=40, padx=3, pady=3)
        btm_frame = tk.Frame(self.root, bg='white', width=450, height=45, pady=3)
        btm_frame2 = tk.Frame(self.root, bg='lavender', width=450, height=60, pady=3)

        # layout all of the main containers
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        top_frame.grid(row=0, sticky="ew")
        center.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")
        btm_frame2.grid(row=4, sticky="ew")

        # create the widgets for the top frame
        model_label = tk.Label(top_frame, text='Model Dimensions')
        width_label = tk.Label(top_frame, text='Width:')
        length_label = tk.Label(top_frame, text='Length:')
        entry_W = tk.Entry(top_frame, background="pink")
        entry_L = tk.Entry(top_frame, background="orange")

        # layout the widgets in the top frame
        model_label.grid(row=0, columnspan=3)
        width_label.grid(row=1, column=0)
        length_label.grid(row=1, column=2)
        entry_W.grid(row=1, column=1)
        entry_L.grid(row=1, column=3)

        # create the center widgets
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        ctr_left = tk.Frame(center, bg='blue', width=100, height=190)
        ctr_mid = tk.Frame(center, bg='yellow', width=250, height=190, padx=3, pady=3)
        ctr_right = tk.Frame(center, bg='green', width=100, height=190, padx=3, pady=3)

        ctr_left.grid(row=0, column=0, sticky="ns")
        ctr_mid.grid(row=0, column=1, sticky="nsew")
        ctr_right.grid(row=0, column=2, sticky="ns")
   
        self.img_ref = []
        self.grid()
        self.canvas = tk.Canvas(self, width=1600, height=900)
        card_size = (175, 250)
        card_displacement = 50
        x_card = 200
        y_card = 200
        self.create_card_image((x_card, y_card), card_size, "images/contessa.jpg")
        self.create_card_image((x_card + card_size[0] + card_displacement, y_card), card_size, "images/duke.jpg")
        self.canvas.pack(fill="both", expand=True)
    
    def create_player_frame(self, playerID):
        frame = tk.Frame()
        

    def create_card_image(self, coord, size, path):
        x,y = coord 
        w, h = size
        card_image = Image.open(path)
        card_image = card_image.resize((w, h), Image.ANTIALIAS)
        card_image = ImageTk.PhotoImage(card_image)
        self.canvas.create_image(x-25, y-25, image=card_image,
                                anchor='nw', tags="image")
        self.img_ref.append(card_image)  # Keep reference to image

    '''
def main():
    root = tk.Tk()
    root.geometry('{}x{}'.format(1600, 900))
    app = Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()