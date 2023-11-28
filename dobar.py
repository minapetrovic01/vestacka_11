import tkinter as tk
from tkinter import Spinbox, Entry, Label, Button, ttk
import numpy as np

class Game:
    def __init__(self, table_size, choosen_player):
        self.table_size = table_size
        self.choosen_player = choosen_player
        
        if(choosen_player == "Player X - black"):
            self.player_1 = Player(True, True)
            self.player_2 = Player(False, False)
        else:
            self.player_2 = Player(True, False)
            self.player_1 = Player(False, True)
            
        self.winner = ""
        self.current_color=1
        
        self.game_window = tk.Tk()
        self.table = GameTable(self.game_window, table_size)
        self.add_input_fields()

        self.game_window.mainloop()
        
    def max_stacks(self):
        self.figure_number= (self.table_size*(self.table_size-2)) /2
        self.figure_number = self.figure_number-(self.figure_number%8)
        return self.figure_number/8
            
    def is_finished(self):
        max_stacks = self.max_stacks()
        score_human = self.player_1.stack_score 
        score_computer = self.player_2.stack_score
        
        if score_human > max_stacks/2:
            self.winner = "You are the winner!"
            return True
        if score_computer > max_stacks/2:
            self.winner = "Computer is the winner!"
            return True
        if max_stacks == score_human + score_computer:
            self.winner = "No one winns! It is draw!"
            return True
        return False
        
    def add_input_fields(self):
        # Dodaj input polja i dugme sa desne strane table
        self.from_label = Label(self.game_window, text="FROM:")
        self.from_label.grid(row=1, column=self.table_size + 2, sticky=tk.W)
        
        self.from_entry = Entry(self.game_window)
        self.from_entry.grid(row=1, column=self.table_size + 3, sticky=tk.W)
        
        self.index_label = Label(self.game_window, text="INDEX IN STACK:")
        self.index_label.grid(row=2, column=self.table_size + 2, sticky=tk.W)
        
        self.index_entry = Entry(self.game_window)
        self.index_entry.grid(row=2, column=self.table_size + 3, sticky=tk.W)
        
        self.direction_label = Label(self.game_window, text="DIRECTION:")
        self.direction_label.grid(row=3, column=self.table_size + 2, sticky=tk.W)
        
        # self.to_entry = Entry(self.game_window)
        # self.to_entry.grid(row=3, column=self.table_size + 3, sticky=tk.W)
        self.direction_var = tk.StringVar()
        self.direction_combobox = ttk.Combobox(self.game_window, textvariable=self.direction_var, values=["Upper-Left", "Upper-Right", "Lower-Left", "Lower-Right"])
        self.direction_combobox.grid(row=3, column=self.table_size + 3, sticky=tk.W) 
        self.direction_combobox.config(state='readonly')
        
        self.move_button = Button(self.game_window, text="MAKE A MOVE", command=self.input_move)
        self.move_button.grid(row=4, column=self.table_size + 2, columnspan=2, sticky=tk.W)
        
    def input_move(self):
        from_value = self.from_entry.get()
        index_value = self.index_entry.get()
        direction_value = self.direction_combobox.get()
        
        if(self.check_inputs(from_value, index_value, direction_value)):
            self.table.move_figure(from_value, index_value, direction_value)
        else:
            warning = tk.Tk()
            InfoForm(self.game_window,warning, "Wrong input!")
            warning.mainloop()
            
            
        
    def check_inputs(self, from_value, index_value, direction_value):
        return self.check_from(from_value) and self.check_index(index_value) and self.check_direction(direction_value)
    def check_from(self, from_value):
        return True
    def check_index(self, index_value):
        return True
    def check_direction(self, direction_value):
        return True
    
    
class GameTable:
    def __init__(self, master, table_size,field_size=50):
        self.master = master
        self.master.title("Byte Game")
        self.field_size = field_size
        self.table_size = table_size
        
        self.state = np.full((self.table_size, self.table_size, 8), -1, dtype=np.int8)
        
        # Dodajte polja za unos
        self.set_starting_state()
        self.draw_table()
        self.draw_all_fields()
        # self.add_input_fields()
        
    def draw_all_fields(self):
        for i in range(self.table_size):
            for j in range(self.table_size):
                self.draw_field(i, j)
                
    def set_starting_state(self):
        self.figure_number= (self.table_size*(self.table_size-2)) /2
        self.figure_number = self.figure_number-(self.figure_number%8)
        print(self.figure_number)
        crne=bele=self.figure_number/2
        
        for i in range(self.table_size - 2, 0, -1):
            for j in range(self.table_size-1,-1,-1):
                print(i,j)
                if crne>0 and i % 2 == 1 and j % 2 == 1:
                    self.state[i, j, 0] = 1
                    crne -= 1
        for i in range(1,self.table_size-1):
            for j in range(self.table_size):
                if bele>0 and i % 2 == 0 and j % 2 == 0:
                    self.state[i, j, 0] = 0
                    bele -= 1
                       
        # self.state[4,4,:] = [1,1,0,0,1,-1,-1,-1]
        
        
    def draw_table(self):
        # Dodaj labele sa indeksima polja sa leve i gornje strane
        for i in range(self.table_size):
            label = tk.Label(self.master, text=str(i + 1))
            label.grid(row=i + 1, column=0, sticky=tk.W)
            
            label = tk.Label(self.master, text=chr(65 + i))
            label.grid(row=0, column=i + 1, sticky=tk.N)
        
        # Dodaj dodatni red i kolonu za labele izvan table
        # for i in range(self.table_size + 1):
        #     label = tk.Label(self.master, text="")
        #     label.grid(row=i, column=self.table_size + 1, sticky=tk.W)
        
        # for i in range(self.table_size + 1):
        #     label = tk.Label(self.master, text="")
        #     label.grid(row=self.table_size + 1, column=i + 1, sticky=tk.N)
        
        self.table = tk.Canvas(self.master, width=self.table_size * self.field_size, height=self.table_size * self.field_size)
        self.table.grid(row=1, column=1, rowspan=self.table_size, columnspan=self.table_size, sticky=tk.N+tk.S+tk.E+tk.W)
        
        # Nacrtajte tamna i svetla polja
        for i in range(self.table_size):
            for j in range(self.table_size):
                if (i + j) % 2 == 0:
                    boja = "lightgray"
                else:
                    boja = "white" 
                x1, y1, x2, y2 = j * self.field_size, i * self.field_size, (j + 1) * self.field_size, (i + 1) * self.field_size
                self.table.create_rectangle(x1, y1, x2, y2, fill=boja)
       
    
   
    
    def draw_field(self, row, column):
        x = column * self.field_size + 25
        y = row * self.field_size + 25
        
        x1, y1, x2, y2 = column * self.field_size, row * self.field_size, (column + 1) * self.field_size, (row + 1) * self.field_size
        
        count = np.count_nonzero(self.state[row, column, :] == -1)
        
        if(count == 8):
            return
        if(count == 7):
            if(self.state[row, column, 0] == 1):
                self.table.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black")
            else:
                self.table.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white")
            return

        x = column * self.field_size + 5  # x koordinata - polje u drugoj koloni
        y = (row+1) * self.field_size  # y koordinata - donja ivica polja
        figure_number = 8-count  # Promenite broj pravougaonika prema potrebi
        figure_height = 8  # Promenite visinu pravougaonika prema potrebi
        for i in range(figure_number):
            if(self.state[row, column, i] == 1):
                self.table.create_rectangle(x, y, x + self.field_size-10, y - figure_height, fill="black")
            else:
                self.table.create_rectangle(x, y, x + self.field_size-10, y - figure_height, fill="white")
            y -= figure_height + 2

    def move_figure(self, from_value, index_value, direction_value):
        # Implementirajte logiku za pomeranje figure na osnovu unetih vrednosti
        pass
class GamePropertiesForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Properties")
        
        # Dobavi širinu i visinu ekrana
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # Postavi veličinu prozora na 1/5 ekrana
        window_width = screen_width // 5
        window_height = screen_height // 5
        
        self.master.geometry(f"{window_width}x{window_height}+{screen_width//2-window_width//2}+{screen_height//2-window_height//2}")
        
        self.label = tk.Label(self.master, text="Enter table size:")
        self.label.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.table_size_picker = Spinbox(self.master, from_=6, to=16, width=3, increment=2, state="readonly")
        self.table_size_picker.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.labelPlayer = tk.Label(self.master, text="Choose your player")
        self.labelPlayer.grid(row=3, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.direction_var = tk.StringVar()
        self.choosen_player = ttk.Combobox(self.master, textvariable=self.direction_var, values=["Player X - black", "Player O - white"])
        self.choosen_player.grid(row=4, column=1, sticky=tk.W) 
        self.choosen_player.config(state='readonly')
        
        self.start_game_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_game_button.grid(row=5, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def start_game(self):
        table_size = int(self.table_size_picker.get())
        choosen_player = self.choosen_player.get()
        # Zatvori trenutni prozor
        self.master.destroy()
        
        game=Game(table_size,choosen_player)
        
        
        # Koristi novu instancu Tk za drugi prozor

class InfoForm:
    def __init__(self, parent,master, message):
        self.master = master
        self.master.title("Info")
        self.parent = parent
        # Dobavi širinu i visinu ekrana
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # Postavi veličinu prozora na 1/5 ekrana
        window_width = screen_width // 5
        window_height = screen_height // 5
        
        self.master.geometry(f"{window_width}x{window_height}+{screen_width//2-window_width//2}+{screen_height//2-window_height//2}")
        
        self.label = tk.Label(self.master, text=message)
        self.label.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.start_game_button = tk.Button(self.master, text="OK", command=self.close_window)
        self.start_game_button.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        
    def close_window(self):
        self.master.destroy()   
    
    
class Player:
    def __init__(self, is_x, is_human):
        self.is_x = is_x # X je crni igrac i igra prvi
        self.is_human = is_human
        self.stack_score = 0
    def increase_stack_score(self):
        self.stack_score += 1

if __name__ == "__main__":
    root = tk.Tk()
    game_properties_form = GamePropertiesForm(root)
    root.mainloop()
