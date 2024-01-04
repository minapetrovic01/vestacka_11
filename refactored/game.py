import tkinter as tk
from tkinter import Entry, Label, Button, ttk
import numpy as np
from collections import deque
import time
from player import Player
from game_table import GameTable
from info_form import InfoForm
import random


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
           

        
    def check_possible_moves(self):
        if len(self.find_all_possible_moves(self.current_color,self.table.state))==0:
            return False
        return True

    def input_move(self):
        from_value = self.from_entry.get()
        index_value = self.index_entry.get()
        direction_value = self.direction_combobox.get()
        
        if(self.check_inputs(from_value, index_value, direction_value)):
            if self.check_possible_moves():
                moved = self.move_figure(from_value, index_value, direction_value)
                if not moved:
                    warning = tk.Tk()
                    InfoForm(self.game_window,warning, "Unable to make a move! Try again.")
                    warning.mainloop()
            else:
                label="X"
                if self.current_color==0:
                    label="O"
                warning = tk.Tk()
                InfoForm(self.game_window,warning, "No possible moves for player" + label + ".")
                warning.mainloop()
            self.change_current_player()
            if self.computer_player:
                self.computers_turn()
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
        print("Time: ", time.time() - start_time)
        print("Depth: ", depth)
        print(best_move)
        if(best_move!=None):
            move=(str(best_move[0]+1)+chr(best_move[1]+65), str(best_move[2]), best_move[3])
        else:
            possible_moves=self.find_all_possible_moves(self.current_color,self.table.state)
            next_move=random.choice(possible_moves)
            move=(str(next_move[0]+1)+chr(next_move[1]+65), str(next_move[2]), next_move[3])

        self.move_figure(move[0],move[1],move[2])
        self.change_current_player()
        if not self.check_possible_moves():
            self.change_current_player()
            self.computers_turn()
        self.move_button.config(state=tk.NORMAL)   



    def max_stacks(self):
        self.figure_number= (self.table_size*(self.table_size-2)) /2
        self.figure_number = self.figure_number-(self.figure_number%8)
        return self.figure_number/8
            
    def is_finished(self):
        max_stacks = self.max_stacks()
        score_computer = self.player_2.stack_score 
        score_human= self.player_1.stack_score
        
        if score_human > max_stacks/2:
            if self.player_1.is_x:
                self.winner = "X is the winner!"
                return True
            else:
                self.winner = "O is the winner!"
                return True

        if score_computer > max_stacks/2:
            if self.player_2.is_x:
                self.winner = "X is the winner!"
                return True
            else:
                self.winner = "O is the winner!"
                return True
        if max_stacks == score_human + score_computer:
            self.winner = "No one winns! It is draw!"
            return True
        return False
    
    def change_current_player(self):
        self.current_color=1-self.current_color
    
    def move_figure(self, from_value, index_value, direction_value):
        moved,i,j= self.table.move_figure(from_value, index_value, direction_value,self.table.state)
        self.table.draw_state()
        
        if moved:
            if self.table.is_stack_full(i,j,self.table.state):
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
                self.table.state[i,j,:]=-1
                if self.is_finished():
                    result = tk.Tk()
                    InfoForm(self.game_window,result, self.winner)
                    result.mainloop()
            self.current_score_display()
                    
        return moved
    



    def current_score_display(self):
        x=self.player_1.stack_score if self.player_1.is_x else self.player_2.stack_score
        o=self.player_2.stack_score if self.player_1.is_x else self.player_1.stack_score
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
    
    def check_dimensions(self,table_size):
        if table_size<6 or table_size>16 or table_size%2==1:
            return False
        return True
    

    def find_all_possible_moves(self,color,state):
        possible_moves=[]
        for i in range(self.table_size):
            for j in range(self.table_size):
                for k in range(8):
                    if state[i,j,k]==color:
                        possible_moves.extend(self.table.find_all_possible_moves_from_position(i,j,k,state))
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
    
    def calc_state_evaluation(self,state):
        num_top_figures = self.calc_num_of_top_figures(state)
        # num_score_possibilities = self.calc_evaluation_of_possibilities(state)
        stack_score=self.countin_stacks(state)
        
        return 0.4*num_top_figures+0.6*stack_score
    
    def end_game(self, state):
        x=self.player_1.stack_score
        y=self.player_2.stack_score
                         
        x+=np.sum(state[:,:,7]==1) if self.player_1.is_x else np.sum(state[:,:,7]==0)
        y+=np.sum(state[:,:,7]==0) if self.player_1.is_x else np.sum(state[:,:,7]==1)
                         
        max_stacks=self.max_stacks()/2
                         
        if x>max_stacks:
            return 10**6
        if y>max_stacks:
            return -10**6
        
        return 0



    def minmax_alpha_beta(self,state,depth,is_computer,alpha,beta):
        if is_computer:
            return self.max_value(state,depth,alpha,beta,None)
        else:
            return self.min_value(state,depth,alpha,beta,None)
        
    def min_value(self,state,depth,alpha,beta,move):
        end=self.end_game(state)
        if end!=0:
            return (move, end)
        move_list=None
        if self.player_2.is_x:
            move_list=self.find_all_possible_moves(1,state)
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
        if self.player_2.is_x:
            move_list=self.find_all_possible_moves(1,state)
        else:
            move_list=self.find_all_possible_moves(0,state)

        state_list=self.generate_all_possible_states(move_list,state)
        
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

