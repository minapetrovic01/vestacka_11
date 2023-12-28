import tkinter as tk
from tkinter import Spinbox, Entry, Label, Button, ttk
import numpy as np
from collections import deque
import time
from queue import PriorityQueue



class Game:
    def __init__(self, table_size, choosen_player,computer_player):
        self.table_size = table_size
        self.choosen_player = choosen_player
        self.computer_player=computer_player
        
        if(choosen_player == "Player X - black"):
            self.player_1 = Player(True, True)#human
            self.player_2 = Player(False, not computer_player)#computer
        else:
            self.player_2 = Player(True, not computer_player)#computer
            self.player_1 = Player(False, True)#human
            
        self.winner = ""
        
        self.current_color=1
        
        self.game_window = tk.Tk()
        self.table = GameTable(self.game_window, table_size)
        self.add_input_fields()
        self.current_score_display()
        
        if self.computer_player and self.player_2.is_x:
            self.computers_turn()

        self.game_window.mainloop()
        
        #print("Game radi")
        
    def change_current_player(self):
        self.current_color=1-self.current_color
    
    def check_dimensions(self,table_size):
        if table_size<6 or table_size>16 or table_size%2==1:
            return False
        return True
        
    def max_stacks(self):
        self.figure_number= (self.table_size*(self.table_size-2)) /2
        self.figure_number = self.figure_number-(self.figure_number%8)
        return self.figure_number/8
            
    def is_finished(self):
        max_stacks = self.max_stacks()
        score_computer = self.player_1.stack_score 
        score_human= self.player_2.stack_score
        
        if score_human > max_stacks/2:
            self.winner = "You are the winner (1st player)!"
            return True
        if score_computer > max_stacks/2:
            self.winner = "Computer is the winner (2nd player)!"
            return True
        if max_stacks == score_human + score_computer:
            self.winner = "No one winns! It is draw!"
            return True
        return False
    
    def current_score_display(self):
        x=self.player_1.stack_score if self.player_1.is_x else self.player_2.stack_score
        o=self.player_1.stack_score if not self.player_1.is_x else self.player_2.stack_score
        self.label_x_text = Label(self.game_window, text="X:"+str(x))
        self.label_x_text.grid(row=5, column=self.table_size + 2, sticky=tk.W)
        
        self.label_o_text = Label(self.game_window, text="O:"+str(o))
        self.label_o_text.grid(row=5, column=self.table_size + 3, sticky=tk.W)
        
    def add_input_fields(self):
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
        
        self.direction_var = tk.StringVar()
        self.direction_combobox = ttk.Combobox(self.game_window, textvariable=self.direction_var, 
                                               values=["Upper-Left", "Upper-Right", "Lower-Left", "Lower-Right"])
        self.direction_combobox.grid(row=3, column=self.table_size + 3, sticky=tk.W) 
        self.direction_combobox.config(state='readonly')
        
        self.move_button = Button(self.game_window, text="MAKE A MOVE", command=self.input_move)
        self.move_button.grid(row=4, column=self.table_size + 2, columnspan=3, sticky=tk.N+tk.E+tk.S+tk.W)
        
    def input_move(self):
        from_value = self.from_entry.get()
        index_value = self.index_entry.get()
        direction_value = self.direction_combobox.get()
        
        if(self.check_inputs(from_value, index_value, direction_value)):
            if self.move_figure(from_value, index_value, direction_value):
                
                self.change_current_player()
                if self.computer_player:
                    self.computers_turn()
                   
                while len(self.find_all_possible_moves(self.current_color,self.table.state))==0:
                    label="X"
                    if self.current_color==0:
                        label="O"
                    result = tk.Tk()
                    InfoForm(self.game_window,result, "No possible moves for player "+label +".")
                    result.mainloop()
                    self.change_current_player()
                    if self.computer_player:
                        self.computers_turn()
                      
            else:
                warning = tk.Tk()
                InfoForm(self.game_window,warning, "Unable to make a move! Try again.")
                warning.mainloop()
        else:
            warning = tk.Tk()
            InfoForm(self.game_window,warning, "Wrong input!")
            warning.mainloop()
            
    def computers_turn(self):
        start_time = time.time()
        best_move = None
        depth = 3
        time_limit = 2
        self.move_button.config(state=tk.DISABLED)
        
        while time.time() - start_time < time_limit and depth < 10:
            move, heuristic = self.minmax_alpha_beta(self.table.state, depth, True, (None, -10**6), (None, 10**6))
            if move is not None:
                best_move = move
            depth += 1
        print("Time: ", time.time() - start_time    )
        print("Depth: ", depth)
        print(best_move)
        if(best_move!=None):
            move=(str(best_move[0]+1)+chr(best_move[1]+65), str(best_move[2]), best_move[3])
            self.move_figure(move[0],move[1],move[2])
        self.change_current_player()
        self.move_button.config(state=tk.NORMAL)

            
    def move_figure(self, from_value, index_value, direction_value):
        moved,i,j= self.table.move_figure(from_value, index_value, direction_value,self.table.state)
        self.table.draw_state()
        
        if moved:
            if self.table.is_stack_full(i,j,self.table.state):
                self.table.state[i,j,:]=-1
                if self.table.state[i,j,7]==1:
                    if self.player_1.is_x:
                        self.player_1.increase_stack_score()
                    else:
                        self.player_2.increase_stack_score()
                else:
                    if self.player_1.is_x:
                        self.player_2.increase_stack_score()
                    else:
                        self.player_1.increase_stack_score()
                if self.is_finished():
                    result = tk.Tk()
                    InfoForm(self.game_window,result, self.winner)
                    result.mainloop()
            self.current_score_display()
                    
        return moved
    
    
    
    
    def find_all_possible_moves(self,color,state):
        possible_moves=[]
        for i in range(self.table_size):
            for j in range(self.table_size):
                for k in range(8):
                    if state[i,j,k]==color:
                        possible_moves.extend(self.table.find_all_possible_moves_from_position(i,j,k,state))
        print(possible_moves)
        return possible_moves
    
    def generate_all_possible_states(self, possible_moves, starting_state):
        list_of_states=[]
        
        for move in possible_moves:
            
            state=np.copy(starting_state)
            
            src_i,src_j,index_value, dest_i, dest_j, dst_index = self.table.calculate_indices(
                str(move[0]+1)+chr(move[1]+65), str(move[2]), move[3],state)
            self.table.execute_move((src_i,src_j,index_value), (dest_i, dest_j, dst_index),state)
            list_of_states.append(state)
            
        return list_of_states
    
    def check_inputs(self, from_value, index_value, direction_value):
        if len(from_value) != 2 and len(from_value) != 3:
            return False
        if not from_value[-1].isalpha():
            return False
        if not from_value[:-1].isdigit():
            return False
        column=ord(from_value[-1])-65
        row=int(from_value[:-1])-1
        if row<0 or row>self.table_size or column<0 or column>self.table_size:
            return False
        
        if self.table.state[row,column,0] == -1:
            return False
        
        index=self.check_index(row, column, index_value)   
        
        direction=self.check_direction(row,column,direction_value)
    
        return index and direction
    
    def check_index(self, row, column, index_value):
        index=int(index_value)
        if not isinstance(index, int):
            return False
        if index<0 or index>7:
            return False
        if self.table.state[row,column,index] !=self.current_color:
            return False
        return True
    
    def check_direction(self, row, column, direction_value):
        if not direction_value in ["Upper-Left", "Upper-Right", "Lower-Left", "Lower-Right"]:
            return False
        if direction_value == "Upper-Left":
            row-=1
            column-=1
        elif direction_value == "Upper-Right":
            row-=1
            column+=1
        elif direction_value == "Lower-Left":
            row+=1
            column-=1
        elif direction_value == "Lower-Right":
            row+=1
            column+=1
        if row<0 or row>=self.table_size or column<0 or column>=self.table_size:
            return False
        
        return True
    
    def countin_stacks(self,state):
        zero_stacks = np.sum(state[:, :, 7] == 0) * 100
        one_stacks = np.sum(state[:, :, 7] == 1) * 100
                        
        if self.player_2.is_x:
            return one_stacks-zero_stacks
        return zero_stacks-one_stacks
        
    def calc_num_of_top_figures(self, state):
        one_tops=0
        zero_tops=0
        for i in range(self.table_size):
            for j in range(self.table_size):
                count = np.count_nonzero(state[i, j, :] == -1)
                if count < 8:
                    if state[i,j,8-count-1]==1:
                        one_tops+=8-count
                    elif state[i,j,8-count-1]==0:
                        zero_tops+=8-count
        
        if self.player_2.is_x:
            return one_tops-zero_tops
        return zero_tops-one_tops
    
    def calc_evaluation_of_possibilities(self, state):
        one_score=0
        zero_score=0
        
        for i in range(self.table_size):
            for j in range(self.table_size):
                empty_fields = np.count_nonzero(state[i, j, :] == -1)
                if empty_fields!=0 and empty_fields!=8:
                    for x in range(empty_fields):
                        neighbors=[(i-1,j-1),(i-1,j+1),(i+1,j-1),(i+1,j+1)]
                        for ni,nj in neighbors:
                            if self.table.is_valid_position(ni, nj):
                                filled= np.count_nonzero(state[ni, nj, :] != -1)
                                if filled!=0:
                                    if x<=filled:
                                        if state[ni,nj,filled-1]==1 :
                                            one_score+=x+1
                                        else:
                                            zero_score+=x+1

        if self.player_2.is_x:
            return one_score-zero_score
        return zero_score-one_score
    
    
    # def calc_evaluation_of_possibilities(self, state):
    #     one_score = 0
    #     zero_score = 0


    #     for x in range(1, self.table_size):
    #         # Diagonal neighbors
    #         one_score += np.sum(np.diagonal(state, offset=-x) == 1) * x
    #         zero_score += np.sum(np.diagonal(state, offset=-x) == 0) * x
    #         one_score += np.sum(np.diagonal(np.flip(state, axis=1), offset=-x) == 1) * x
    #         zero_score += np.sum(np.diagonal(np.flip(state, axis=1), offset=-x) == 0) * x

    #         # Anti-diagonal neighbors
    #         one_score += np.sum(np.diagonal(state, offset=x) == 1) * x
    #         zero_score += np.sum(np.diagonal(state, offset=x) == 0) * x
    #         one_score += np.sum(np.diagonal(np.flip(state, axis=1), offset=x) == 1) * x
    #         zero_score += np.sum(np.diagonal(np.flip(state, axis=1), offset=x) == 0) * x

    #     if self.player_2.is_x:
    #         return one_score - zero_score
    #     return zero_score - one_score
    
    
    def minmax_alpha_beta(self,state,depth,is_computer,alpha,beta):
        if is_computer:
            return self.max_value(state,depth,alpha,beta,None)
        else:
            return self.min_value(state,depth,alpha,beta,None)
        
    def calc_state_evaluation(self,state):
        num_top_figures = self.calc_num_of_top_figures(state)
        # num_score_possibilities = self.calc_evaluation_of_possibilities(state)
        stack_score=self.countin_stacks(state)
        
        return 0.4*num_top_figures+0.6*stack_score
    
    def end_game(self, state):
        x=self.player_1.stack_score
        y=self.player_2.stack_score
        
        # for i in range(self.table_size):
        #     for j in range(self.table_size):
        #          empty_fields = np.count_nonzero(state[i, j, :] == -1)
        #          if empty_fields==0:
        #              if state[i,j,7]==1 and self.player_1.is_x:
        #                  x+=1
        #              elif  state[i,j,7]==1 and not self.player_1.is_x:
        #                  y+=1
        #              elif state[i,j,7]==0 and self.player_1.is_x:
        #                  y+=1
        #              else:
        #                  x+=1
                         
        x+=np.sum(state[:,:,7]==1) if self.player_1.is_x else np.sum(state[:,:,7]==0)
        y+=np.sum(state[:,:,7]==0) if self.player_1.is_x else np.sum(state[:,:,7]==1)
                         
        max_stacks=self.max_stacks()/2
                         
        if x>max_stacks:
            return 10**6
        if y>max_stacks:
            return -10**6
        
        return 0
                     
                         
    def min_value(self,state,depth,alpha,beta,move):
        end=self.end_game(state)
        if end!=0:
            return (move, end)
        move_list=None
        if self.player_2.is_x:
            move_list=self.find_all_possible_moves(1,state)#ovde je mozda greska sta se salje
        else:
            move_list=self.find_all_possible_moves(0,state)
            
        
        state_list=self.generate_all_possible_states(move_list,state)
        
        
        if depth==0 or len(move_list)==0:
            return (move, self.calc_state_evaluation(state))

        for i,s in enumerate(move_list):
            beta=self.min_state(beta, self.max_value(state_list[i],depth-1,alpha,beta,s if move is None else move))
            if beta[1]<=alpha[1]:
                return alpha
        
        return beta
        
        
    def max_value(self,state,depth,alpha,beta,move):
        end=self.end_game(state)
        if end:
            return (move, end)
        move_list=None
        if self.player_2.is_x:#probleeeeem nije ovde ovo if!!!
            move_list=self.find_all_possible_moves(1,state)
        else:
            move_list=self.find_all_possible_moves(0,state)
            
        state_list=self.generate_all_possible_states(move_list,state)
        #print(move_list)
        
        if depth==0 or len(move_list)==0:
            return (move, self.calc_state_evaluation(state))

        for i,s in enumerate(move_list):
            alpha=self.max_state(alpha, self.min_value(state_list[i],depth-1,alpha,beta,s if move is None else move))
            if beta[1]<=alpha[1]:
                return beta
        
        return alpha
    
    def max_state(self, a,b):
        if a[1]>= b[1]:
            return a
        return b
    
    def min_state(self, a,b):
        if a[1]<= b[1]:
            return a
        return b


                       
class GameTable:
    def __init__(self, master, table_size,field_size=50):
        self.master = master
        self.master.title("Byte Game")
        self.field_size = field_size
        self.table_size = table_size
        
        self.state = np.full((self.table_size, self.table_size, 8), -1, dtype=np.int8)
        
        self.set_starting_state()
        self.draw_state()
        
    def draw_all_fields(self):
        for i in range(self.table_size):
            for j in range(self.table_size):
                self.draw_field(i, j)
                
    def set_starting_state(self):
        self.figure_number= (self.table_size*(self.table_size-2)) /2
        self.figure_number = self.figure_number-(self.figure_number%8)
        crne=bele=self.figure_number/2
        
        for i in range(self.table_size - 2, 0, -1):
            for j in range(self.table_size-1,-1,-1):
                if crne>0 and i % 2 == 1 and j % 2 == 1:
                    self.state[i, j, 0] = 1
                    crne -= 1
        for i in range(1,self.table_size-1):
            for j in range(self.table_size):
                if bele>0 and i % 2 == 0 and j % 2 == 0:
                    self.state[i, j, 0] = 0
                    bele -= 1
                       
    def draw_table(self):
        # Dodaje labele sa indeksima polja sa leve i gornje strane
        for i in range(self.table_size):
            label = tk.Label(self.master, text=str(i + 1))
            label.grid(row=i + 1, column=0, sticky=tk.W)
            
            label = tk.Label(self.master, text=chr(65 + i))
            label.grid(row=0, column=i + 1, sticky=tk.N)
        
        self.table = tk.Canvas(self.master, width=self.table_size * self.field_size, height=self.table_size * self.field_size)
        self.table.grid(row=1, column=1, rowspan=self.table_size, columnspan=self.table_size, sticky=tk.N+tk.S+tk.E+tk.W)
        
        # Crta tamna i svetla polja
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

        x = column * self.field_size + 5  
        y = (row+1) * self.field_size 
        figure_number = 8-count 
        figure_height = 8  
        for i in range(figure_number):
            if(self.state[row, column, i] == 1):
                self.table.create_rectangle(x, y, x + self.field_size-10, y - figure_height, fill="black")
            else:
                self.table.create_rectangle(x, y, x + self.field_size-10, y - figure_height, fill="white")
            y -= figure_height + 2
            
    def check_empty_neighbors(self, index_i, index_j,state):
        empty_fields1= empty_fields2 =empty_fields3=empty_fields4= True

        def is_occupied(i, j,state):
            return state[i, j, 0] != -1

        if self.is_valid_position(index_i + 1, index_j + 1) :
            if is_occupied(index_i + 1, index_j + 1,state):
                empty_fields1 = False
       
        if self.is_valid_position(index_i + 1, index_j - 1):
            if is_occupied(index_i + 1, index_j - 1,state):
                empty_fields2 = False
            
        if self.is_valid_position(index_i - 1, index_j + 1):
            if is_occupied(index_i - 1, index_j + 1,state):
                empty_fields3 = False
        
        if self.is_valid_position(index_i - 1, index_j - 1):
            if is_occupied(index_i - 1, index_j - 1,state):
                empty_fields4 = False
            
        empty_fields = empty_fields1 and empty_fields2 and empty_fields3 and empty_fields4

        return empty_fields
    

    def is_valid_position(self, i, j):
        return (0 <= i) and (i < self.table_size) and (0 <= j) and (j< self.table_size)

    def find_nearest_stacks(self, start_position,state):
        visited = set()
        queue = deque([(start_position, 0)])
        min_distance = float('inf')
        nearest_positions = []

        while queue:
            (x, y), distance = queue.popleft()

            if distance > min_distance:
                break  # Stop searching if we exceed the minimum distance

            if state[x,y,0] != -1 and (x, y) != start_position:
                min_distance = distance
                nearest_positions.append((x, y))

            for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                new_x, new_y = x + i, y + j

                if self.is_valid_position(new_x, new_y) and (new_x, new_y) not in visited:
                    queue.append(((new_x, new_y), distance + 1))
                    visited.add((new_x, new_y))

        return nearest_positions
    
    def heuristic(self,position, goal):
        # A simple Manhattan distance heuristic for A*
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])
    
    def find_nearest_stacks_a_star(self, start_position, state):
        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.put((0, start_position))
        min_distance = float('inf')
        nearest_positions = []

        while not priority_queue.empty():
            distance, (x, y) = priority_queue.get()

            if distance > min_distance:
                break  # Stop searching if we exceed the minimum distance

            if state[x, y, 0] != -1 and (x, y) != start_position:
                min_distance = distance
                nearest_positions.append((x, y))

            for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                new_x, new_y = x + i, y + j

                if self.is_valid_position(new_x, new_y) and (new_x, new_y) not in visited:
                    cost = distance + 1  # Cost is the current distance plus 1
                    priority_queue.put((cost + self.heuristic((new_x, new_y), start_position), (new_x, new_y)))
                    visited.add((new_x, new_y))

        return nearest_positions
    
    def is_on_path_to_closest_stack(self, current, next_move,state):#ova ne valja nista funkcijaaa!!!!!!!!!!!!!!!!!!!!
        # nearest_stacks=self.find_nearest_stacks(current,state)
        nearest_stacks=self.find_nearest_stacks_a_star(current,state)
        on_path=False
        for stack in nearest_stacks:
            a,b=stack
            i,j=current
            x,y=next_move
            # if(abs(a-i)<abs(a-x)):
            if a+b==i+j or a-b==i-j:
                if abs(x-a)+abs(y-b)<=abs(i-a)+abs(j-b):
                    on_path=True
                    break
            else:
                if a==i and abs(b-y)<=abs(b-j):
                    on_path=True
                    break
                if b==j and abs(a-x)<=abs(a-i):
                    on_path=True
                    break
                if b>=j and y==j+1:
                    on_path=True
                    break
                if b<=j and y==j-1:
                    on_path=True
                    break
                
            
            # if abs(a-i)>=abs(a-x):
            #     if b>=j and y==j+1 and x>i:
            #         on_path=True
            #         break
            #     if j>=b and y==j-1 and x<i:
            #         on_path=True
            #         break
            # # if(abs(b-j)<abs(b-y)):
            # if abs(b-j)>=abs(b-y):
            #     if a>=i and x==i-1 and y>j:
            #         on_path=True
            #         break
            #     if a<=i and x==i+1 and y<j:
            #         on_path=True
            #         break
           
        return on_path

    def is_stack_move_valid(self, source, destination,state):
        count_in_dest = np.count_nonzero(state[destination[0], destination[1], :] == -1)
        count_in_source = np.count_nonzero(state[source[0], source[1], :] == -1)
        count_exchange=8-count_in_source-source[2]

        next_empty_in_stack = 8 - count_in_dest

        if source[2]>next_empty_in_stack:
            return False
        if count_exchange + next_empty_in_stack > 8:
            return False
        
        return True
    
    def calculate_indices(self, from_value, index_value, direction_value,state):
        
        # print(from_value, index_value, direction_value)
        dest_column=src_column=ord(from_value[-1])-65
        dest_row=src_row=int(from_value[:-1])-1
        if direction_value == "Upper-Left":
            dest_row-=1
            dest_column-=1
        elif direction_value == "Upper-Right":
            dest_row-=1
            dest_column+=1
        elif direction_value == "Lower-Left":
            dest_row+=1
            dest_column-=1
        elif direction_value == "Lower-Right":
            dest_row+=1
            dest_column+=1
        
        dst_index = np.count_nonzero(state[dest_row, dest_column, :] == -1)
        dst_index = 8 - dst_index
            
        return src_row, src_column,int(index_value), dest_row, dest_column, dst_index
    
    def is_stack_full(self, row, column,state):
        return np.count_nonzero(state[row, column, :] == -1) == 0
        
    def execute_move(self, source, destination,table):
        count = 8-np.count_nonzero(table[source[0], source[1], :] == -1) - source[2]
        table[destination[0], destination[1], destination[2]:destination[2]+count] = table[
            source[0], source[1], source[2]:source[2]+count] 
        table[source[0], source[1], source[2]:] = -1

    def move_figure(self, from_value, index_value, direction_value,state):
        src_i,src_j,index_value, dest_i, dest_j, dst_index = self.calculate_indices(
            from_value, index_value, direction_value,state
            )
        
        empty_neighbors = self.check_empty_neighbors(src_i, src_j,state)
        empty_destination = self.is_destination_empty((dest_i, dest_j),state)
        if not empty_destination and not empty_neighbors and self.is_stack_move_valid(
            (src_i,src_j,index_value), (dest_i, dest_j, dst_index),state):
            self.execute_move((src_i,src_j,index_value), (dest_i, dest_j, dst_index),state)
            # self.draw_state()
            return True, dest_i, dest_j
        
        if empty_neighbors and index_value==0:#whole stack needs to be moved to empty field
            if self.is_on_path_to_closest_stack((src_i,src_j), (dest_i, dest_j),state):
                self.execute_move((src_i,src_j,index_value), (dest_i, dest_j, dst_index),state)
                # self.draw_state()
                return True, dest_i, dest_j
        return False, -1, -1
    
    def is_destination_empty(self, destination,state):
        return np.count_nonzero(state[destination[0], destination[1], :] == -1) == 8 
      
    def draw_state(self):
        self.draw_table()
        self.draw_all_fields()
        
    def find_all_possible_moves_from_position(self, i, j, k,state):
        moves=[]
        if self.check_empty_neighbors(i, j,state):
            # print("empty neighbors",i,j,k)
            if k==0:
                if self.is_valid_position(i-1, j-1):
                    if self.is_on_path_to_closest_stack((i,j), (i-1,j-1),state):
                        moves.append((i,j,k,"Upper-Left"))
                if self.is_valid_position(i-1, j+1):
                    if self.is_on_path_to_closest_stack((i,j), (i-1,j+1),state):
                        moves.append((i,j,k,"Upper-Right"))
                if self.is_valid_position(i+1, j-1):
                    if self.is_on_path_to_closest_stack((i,j), (i+1,j-1),state):
                        moves.append((i,j,k,"Lower-Left"))
                if self.is_valid_position(i+1, j+1):
                    if self.is_on_path_to_closest_stack((i,j), (i+1,j+1),state):
                        moves.append((i,j,k,"Lower-Right"))
        else:
            if self.is_valid_position(i-1, j-1) and self.is_stack_move_valid((i,j,k), (i-1,j-1,0),state) and not self.is_destination_empty((i-1,j-1),state):
                moves.append((i,j,k,"Upper-Left"))
            if self.is_valid_position(i-1, j+1) and self.is_stack_move_valid((i,j,k), (i-1,j+1,0),state) and not self.is_destination_empty((i-1,j+1),state):
                moves.append((i,j,k,"Upper-Right"))
            if self.is_valid_position(i+1, j-1) and self.is_stack_move_valid((i,j,k), (i+1,j-1,0),state) and not self.is_destination_empty((i+1,j-1),state):
                moves.append((i,j,k,"Lower-Left"))
            if self.is_valid_position(i+1, j+1) and self.is_stack_move_valid((i,j,k), (i+1,j+1,0),state) and not self.is_destination_empty((i+1,j+1),state):
                moves.append((i,j,k,"Lower-Right"))
                
        return moves
    

            
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
        self.checkbox = tk.Checkbutton(root, text="play against computer", variable=self.checkbox_var)
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
