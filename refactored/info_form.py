import tkinter as tk

class InfoForm:
    def __init__(self, parent,master, message):
        self.master = master
        self.master.title("Info")
        self.parent = parent
        
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        window_width = screen_width // 5
        window_height = screen_height // 5
        
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        self.master.geometry(f"{window_width}x{window_height}+{screen_width//2-window_width//2}+{screen_height//2-window_height//2}")
        
        self.label = tk.Label(self.master, text=message)
        self.label.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.start_game_button = tk.Button(self.master, text="OK", command=self.close_window)
        self.start_game_button.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
    def close_window(self):
        self.master.destroy()   
    