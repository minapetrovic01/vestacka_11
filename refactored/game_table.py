import tkinter as tk
import numpy as np
from collections import deque
from queue import PriorityQueue


class GameTable:
    def __init__(self, master, table_size,field_size=50):
        self.master = master
        self.master.title("Byte Game")
        self.field_size = field_size
        self.table_size = table_size
        
        self.state = np.full((self.table_size, self.table_size, 8), -1, dtype=np.int8)
        
        self.set_starting_state()
        self.draw_state()
        
           
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

    def draw_all_fields(self):
        for i in range(self.table_size):
            for j in range(self.table_size):
                self.draw_field(i, j)
     
    def draw_state(self):
        self.draw_table()
        self.draw_all_fields()
      
    def calculate_indices(self, from_value, index_value, direction_value,state):
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
    
    def is_valid_position(self, i, j):
        return (0 <= i) and (i < self.table_size) and (0 <= j) and (j< self.table_size)

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
    
    def is_destination_empty(self, destination,state):
        return np.count_nonzero(state[destination[0], destination[1], :] == -1) == 8 
      
    def is_stack_full(self, row, column,state):
        return np.count_nonzero(state[row, column, :] == -1) == 0
     
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
    
    def is_on_path_to_closest_stack(self, current, next_move,state): 
        nearest_stacks=self.find_nearest_stacks_a_star(current,state)
        on_path=False
        for stack in nearest_stacks:
            a,b=stack
            i,j=current
            x,y=next_move

            #current i stack u istoj vrsti
            if a==i:
                if b>j and y==j+1:
                    on_path=True
                    break
                elif b<j and y==j-1:
                    on_path=True
                    break

            #current i stack u istoj koloni
            if b==j:
                if a>i and x==i+1:
                    on_path=True
                    break
                elif a<i and x==i-1:
                    on_path=True
                    break

            #current i stack su na istoj dijagonali
            if abs(i - a) == abs(j - b):
                if i < a and j < b and x==i+1 and y==j+1:
                    on_path=True
                    break
                elif i < a and j > b and x==i+1 and y==j-1:
                    on_path=True
                    break
                elif i > a and j < b and x==i-1 and y==j+1:
                    on_path=True
                    break
                elif i > a and j > b and x==i-1 and y==j-1:
                    on_path=True
                    break


            #ostalo, gledaju se prostori koje odredjuju glavna 
            #i sporedna dijagonala koje prolaze kroz current
            sum_ij = i + j
            sum_ab = a + b
            if sum_ab > sum_ij:
                if b>a: #desno od sporedne
                    if y==j+1: #desni trougao
                        on_path=True
                        break
                else:
                    if x==i+1: #donji trougao
                        on_path=True
                        break

            elif sum_ab < sum_ij:
                if b>a: #levo od sporedne
                    if x==i-1: #gornji trougao
                        on_path=True
                        break
                else:
                    if y==j-1: #levi trougao
                        on_path=True
                        break

        return on_path

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
    
    def find_nearest_stacks_a_star(self, start_position, state):
        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.put((0, start_position))
        min_distance = float('inf')
        nearest_positions = []

        while not priority_queue.empty():
            distance, (x, y) = priority_queue.get()

            if distance > min_distance:
                break  # pretraga trazenja ako se dostigne minimalna distanca

            if state[x, y, 0] != -1 and (x, y) != start_position:
                min_distance = distance
                nearest_positions.append((x, y))

            for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                new_x, new_y = x + i, y + j

                if self.is_valid_position(new_x, new_y) and (new_x, new_y) not in visited:
                    cost = distance + 1 
                    priority_queue.put((cost + self.heuristic((new_x, new_y), start_position), (new_x, new_y)))
                    visited.add((new_x, new_y))

        return nearest_positions
    def heuristic(self,position, goal):
        # Manhattan distance heuristic for A*
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])
    


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
            return True, dest_i, dest_j
        
        if empty_neighbors and index_value==0:#ceo stek treba da se prebaci na prazno polje
            if self.is_on_path_to_closest_stack((src_i,src_j), (dest_i, dest_j),state):
                self.execute_move((src_i,src_j,index_value), (dest_i, dest_j, dst_index),state)
                return True, dest_i, dest_j
        return False, -1, -1
    

  
    def find_all_possible_moves_from_position(self, i, j, k,state):
        moves=[]
        if self.check_empty_neighbors(i, j,state):
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
    
