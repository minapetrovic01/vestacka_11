import tkinter as tk
from tkinter import Spinbox,ttk
from game import Game

class GamePropertiesForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Properties")
        
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        window_width = screen_width // 5
        window_height = screen_height // 5
        
        for i in range(6):
            self.master.grid_columnconfigure(i, weight=1)

        for i in range(9):
            self.master.grid_rowconfigure(i, weight=1)

        self.master.geometry(f"{window_width}x{window_height}+{screen_width//2-window_width//2}+{screen_height//2-window_height//2}")
        
        self.label = tk.Label(self.master, text="Enter table size:")
        self.label.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.table_size_picker = Spinbox(self.master, from_=6, to=16, width=3, increment=2, state="readonly")
        self.table_size_picker.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.labelPlayer = tk.Label(self.master, text="Choose first player")
        self.labelPlayer.grid(row=3, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.direction_var = tk.StringVar()
        self.choosen_player = ttk.Combobox(
            self.master, textvariable=self.direction_var, values=["Player X - black", "Player O - white"])
        self.choosen_player.grid(row=4, column=2, sticky=tk.N+tk.S+tk.E+tk.W) 
        self.choosen_player.config(state='readonly')
        
        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self.master, text="play against computer", variable=self.checkbox_var)
        self.checkbox_var.set(False)
        self.checkbox.grid(row=5, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.start_game_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_game_button.grid(row=7, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        

    def start_game(self):
        table_size = int(self.table_size_picker.get())
        choosen_player = self.choosen_player.get()
        computer_player = self.checkbox_var.get()
        self.master.destroy()

        game=Game(table_size,choosen_player,computer_player)
