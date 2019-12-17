import os
import time
import json 
from collections import defaultdict

G_OFFSET = 1

#+----------------------------------------------------------------------------+
#|                                Classes                                     |
#+----------------------------------------------------------------------------+

class Computer:
    def __init__(self, tape, name=None, inp_stack=None, output_mode=None):
        self.name = name
        self.enabled = True
        self.tape = tape            # Stores this comptuers program
        self.inp_stack = inp_stack  # Op code 3 gets input from here
        self.i = 0                  # Instruction pointer
        self.rel_base = 0

        self.output_mode = output_mode # By default, output is printed to stdout
                                       # if mode='return', execution in method compute()
                                       # pauses and the output is returned to the calling thread

        self.last_computed_value = 0

        # Increase the amount of "empty memory" available by default:
        #self.tape += [ 0 for n in range(len(self.tape)) ]

    def set_input(self, items:list):
        self.inp_stack = items

    def cur_instr(self):
        """ Get instruction pointed at by self.i """
        return self.tape[self.i]

    def clone(self):
        """ Returns a complete copy of the current VM """
        clone = Computer(self.tape[:], inp_stack=self.inp_stack[:] ,output_mode='return')
        clone.i = self.i 
        clone.rel_base = self.rel_base
        clone.last_computed_value = self.last_computed_value
        return clone 

    def compute(self):
        """ Iterates over self.tape, executing instructions until a HALT op is encountered,
            or data is returned (op 4) which pauses execution of the computer
        """

        def set_(index, val):
            """ Set value at position 'index' to be 'val' """
            self.tape[index] = val

        def get_(index):
            """ Return value stored at 'index' """
            return self.tape[index]

        def get_indexes(a,b=None,c=None):
            """ Method for handeling the three different parameter modes.

                Accepts up to three args which are the modes for

                Based on what a,b and c are, returns the appropriate index to be used.
                a,b, and c are the parameter modes.

                If you enter a, it will return just one index.
                If you enter a and b, it will return two indexes.
                If you enter a, b, and c, it will return three indexes.
                       
                Modes:
                -----------------------------------------------------------
                The default mode is set to be immediate mode (mode 1):
                Indexes will be offsets of the current instruction pointer

                Positional mode: (mode 0)
                Indexes will be values located at addresses pointed at by
                whatever is at the current pointer offset locations:

                Relative mode: (mode 2)
                Same as positional mode, but add the current relative base to the index 
            """
            p1,p2,p3 = None, None, None
            if a != None:
                p1 = self.i+1                               # Imediate mode
                if   a == 0: p1 = get_(p1)                  # Positional
                elif a == 2: p1 = self.rel_base + get_(p1)  # Relative

            if b != None: 
                p2 = self.i+2
                if b == 0: p2 = get_(p2)
                elif b == 2: p2 = self.rel_base + get_(p2)

            if c != None: 
                p3 = self.i+3
                if   c == 0: p3 = get_(p3)
                elif c == 2: p3 = self.rel_base + get_(p3)

            if p1 != None and p2 != None and p3 != None:    return p1, p2, p3
            if p1 != None and p2 != None:                   return p1, p2
            if p1 != None:                                  return p1


        def _op_99():
            self.enabled = False
            self.i == len(self.tape)
            return 'HALT'

        # NOTE: '<index>' Is read as, The value at 'index'.
        # EXAMPLE: <p1> + <p2> Is read as " The value at index p1 plus the value at index p2 "

        def _op_01(): # Adds <p1> + <p2>
            p1, p2, p3 = get_indexes(m1,m2,m3)
            set_( p3, val=get_(p1) + get_(p2) )
            self.i += 4

        def _op_02(): # Multiplies <p1> * <p2>
            p1, p2, p3 = get_indexes(m1,m2,m3)
            set_( p3, val=get_(p1) * get_(p2) )
            self.i += 4

        def _op_03():  # Get input
            #user_in = input(">>> type a number: 1 North, 2 South, 3 West, 4 East")
            user_in = self.inp_stack.pop(0)
            p1 = get_indexes(m1)
            set_( p1, val=int(user_in) )
            self.i += 2

        def _op_04():  # Return output
            p1 = get_indexes(m1)
            output = get_(p1)
            self.last_computed_value = output

            self.i += 2 # Increment BEFORE returning

            if self.output_mode=='return': return output
            else:                          print(output)

        def _op_05():  # Jump-If-True: Sets instr pointer to <p2> if <p1> is non-zero
            p1,p2 = get_indexes(m1,m2)
            if get_(p1) > 0:
                self.i = get_(p2)
            else:
                self.i += 3

        def _op_06(): # Jump-If-False: Sets instr pointer to <p2> if <p1> is zero
            p1,p2 = get_indexes(m1,m2)
            if get_(p1) == 0:
                self.i = get_(p2)
            else:
                self.i += 3

        def _op_07(): # Stores 1 in <p3> if <p1> < <p2> else stores 0
            p1,p2,p3 = get_indexes(m1,m2, m3)
            if get_(p1) < get_(p2): set_( p3, val=1 )
            else:                   set_( p3, val=0 )
            self.i += 4

        def _op_08():  # Stores 1 if <p1> == <p2> else stores 1
            p1,p2,p3 = get_indexes(m1,m2,m3)
            if get_(p1) == get_(p2): set_( p3, val=1 )
            else:                    set_( p3, val=0 )
            self.i += 4

        def _op_09(): # Change the relative boost value:
            p1 = get_indexes(m1)
            self.rel_base += get_(p1)
            self.i += 2

        # Tie each op to its' associated function:
        execute_ = { '99':_op_99, '01':_op_01, '02':_op_02, '03':_op_03, '04':_op_04,
                     '05':_op_05, '06':_op_06, '07':_op_07, '08':_op_08, '09':_op_09}

        while self.i < len(self.tape):
            # Process instruction:
            instr  = str(self.cur_instr())
            op     = instr[len(instr)-2:]

            # Extract parameter modes from the instruction:
            pmodes = instr[:len(instr)-2]
            m1,m2,m3 = 0,0,0
            if len(pmodes) > 0:
                pmodes = list(pmodes); reversed(pmodes)
                if len(pmodes) > 0: m1 = int(pmodes.pop())
                if len(pmodes) > 0: m2 = int(pmodes.pop())
                if len(pmodes) > 0: m3 = int(pmodes.pop())

            # Make sure op is in correct format:
            if len(op) == 1: op = '0' + op
            foo = 0
            # Execute the op:
            result = execute_[op]()
            if result != None:
                if result == 'HALT': break
                else: return result

class Path:
    """ A simple N-ary Tree class for representing connecting paths.    
        
        Class Fields:

            * Loc      ->  A tuple describing the (x,y) location of said path node (aka segment)
            * prev     ->  The "parent" path segment to this path segment
            * branches ->  A list containing 1 - 4 path segments which branch off from this path segment
                           In other words, the "children" of this path segment
         """
    def __init__(self, loc, prev):
        self.loc = loc
        self.prev = prev # Path object
        self.branches = []  # List of path objects defining possible braching paths from THIS path node

    def add_branch(self, node):
        self.branches.append(node)

class RepairBot:
    
    def __init__(self, data, interval=0.1, visualize=False, wall_data=None, computer=None):
        self.computer = Computer(data, output_mode='return')
        if computer:
            self.computer = computer 

        self.loc = (22,22)
        self.old_loc = (22,22)

        self.walls = dict()
        self.visited = set()

        self.direction = 1
        self.found_oxygen = False

        self.interval = interval
        self.visualize = visualize
        self.oxygen_location = (0,0)        
        self.steps_taken = 0

        self.wall_data = wall_data

        self.backtracking = False

        self.directions = {1:'North', 2:'South', 3:'West', 4:'East'}

        self.root = Path(self.loc,prev=None)
        self.prev = self.root
        self.oxygen_node = None
        
        self.back_track_count = 0

    def clone_bot(self):
        clone_vm = self.computer.clone()
        bot = RepairBot(
                        data=[],
                        interval=self.interval, 
                        visualize=self.visualize,                        
                        wall_data=self.wall_data,
                        computer=clone_vm
                        )
        bot.walls     = self.walls
        bot.visited   = self.visited                                 
        bot.loc       = self.loc
        bot.direction = self.direction
        return bot 

    def move_bot(self, exploring=False): 
        """"
            Calling this method will cause the bot to attempt to move in the direction it
            is currently facing (self.direction). 
            
            @Return: If it moved, it will return True
                     If not (wall in the way) it will return False

                     If it moved AND it found the oxygen system, 
                     it will set (self.found_oxygen) to True
                     and set (self.oxygen_location) to (self.loc)
        """

        # Send direction robot is facing to computer:
        self.computer.set_input([self.direction])
        
        # Compute if a move is possible:
        status = self.computer.compute()

        # If there is a wall in the way:
        if status == 0: 
            wall = (0,0)
            if   self.direction == 1: wall = (self.loc[0], self.loc[1] - 1)
            elif self.direction == 2: wall = (self.loc[0], self.loc[1] + 1)
            elif self.direction == 3: wall = (self.loc[0] - 1, self.loc[1])        
            elif self.direction == 4: wall = (self.loc[0] + 1, self.loc[1])      
            if wall not in self.walls:
                self.walls[wall] = '█'            
            return False

        # If the move was succesful, track it here in RepairBot:
        elif status == 1 or status == 2: 
            
            self.old_loc = (self.loc[0],self.loc[1])
            if self.direction == 1: 
                self.loc = (self.loc[0], self.loc[1] - 1)          
            elif self.direction == 2:
                self.loc = (self.loc[0], self.loc[1] + 1)        
            elif self.direction == 3: 
                self.loc = (self.loc[0] - 1, self.loc[1])                  
            elif self.direction == 4: 
                self.loc = (self.loc[0] + 1, self.loc[1])

            segment = None
            if self.loc not in self.visited:                
                if not exploring:
                    # If we were backtrakcing, rewind prev path to the proper place:
                    if self.backtracking:
                        for _ in range(self.back_track_count+1):
                            self.prev = self.prev.prev

                    # create a new path segment:
                    segment = Path(self.loc, self.prev)

                    # Store current in prevs branches:
                    self.prev.add_branch(segment)

                    # Change prev:
                    self.prev = segment

                    self.visited.add(self.loc)
                    self.steps_taken += 1
                    move_cursor(0,0); print("Steps taken:", self.steps_taken)

                    self.backtracking = False
            else:
                if not exploring:
                    if not self.backtracking:
                        self.backtracking = True
                        self.back_track_count = 0
                    else:                    
                        self.steps_taken -= 1
                        self.back_track_count += 1
                        move_cursor(0,0); print("Steps taken:", self.steps_taken)

                  # Found the oxygen system!:
            if status == 2:
                #self.root = segment
                self.oxygen_node = segment
                #print("Found oxygen")
                # if self.visualize:
                #     print_symbol(self.loc, self.direction, '0')
                self.found_oxygen = True     
                self.oxygen_location = self.loc           
                return True

            if self.visualize and not exploring:                              
                print_bot(self.loc, self.old_loc, self.direction); time.sleep(self.interval)

                # For some reason, using control codes means when we print the bots new location,
                # sometimes the row below the bot get deleted. So, make sure to reprint that row:
                
                #below_row = self.wall_data[self.loc[1]]
                # for loc, symbol in sorted(below_row.items()): 
                #     print_symbol(loc, 1, symbol)              

            if self.visualize:
                for x in range(42): 
                    y = self.loc[1] - 1 
                    if (x,y) in self.walls: print_symbol((x,y), 1, self.walls[(x,y)])    

                for x in range(42): 
                    y = self.loc[1]  
                    if (x,y) in self.walls: print_symbol((x,y), 1, self.walls[(x,y)])    
                
                for x in range(42): 
                    y = self.loc[1] + 1 
                    if (x,y) in self.walls: print_symbol((x,y), 1, self.walls[(x,y)])    

            return True

    def turn_left(self): # 1 North, 2 South, 3 West, 4 East
        if   self.direction == 1: self.direction = 3 
        elif self.direction == 2: self.direction = 4
        elif self.direction == 3: self.direction = 2
        elif self.direction == 4: self.direction = 1 

    def turn_right(self):  # 1 North, 2 South, 3 West, 4 East
        if   self.direction == 1: self.direction = 4
        elif self.direction == 2: self.direction = 3
        elif self.direction == 3: self.direction = 1
        elif self.direction == 4: self.direction = 2

    def turn_180(self):
        self.turn_left(); self.turn_left()

    def opposite(self, direction):
        if direction == 1: return 2
        elif direction == 2: return 1
        elif direction == 3: return 4
        elif direction == 4: return 3

    def get_input(self, input_set, message):
        user_in = None
        while user_in not in input_set:
            user_in = input(message).rstrip('\n')
            if user_in.rstrip().lstrip() == 'quit':
                quit()
            
        user_in = int(user_in)
        return user_in
    
    def check_dir(self, direc, last_direc):
        if direc == 3 and last_direc == 4: return False
        if direc == 4 and last_direc == 3: return False
        if direc == 1 and last_direc == 2: return False
        if direc == 2 and last_direc == 1: return False
        return True

    def manual_run(self, max_row):       
        dir_commands = []         
        while self.computer.enabled and not self.found_oxygen:   
            
            move_cursor(max_row + 5, 0)
            print(dir_commands)
            print()
            print()
            print()
            message = ">>> Type a number: \tNorth: 1, South: 2,\n\t\t\tWest: 3, East: 4 : "       
            self.direction = self.get_input(['1','2','3','4'], message=message)
               
            if not self.move_bot():
               print("Hit a wall!")
            else:
                dir_commands.append(self.direction)

        return dir_commands

    def semi_auto_run(self, orders):         
        move_commands_given = 0
        while self.computer.enabled and not self.found_oxygen:   
            self.direction = orders.pop(0)
            while self.move_bot(): 
                move_commands_given += 1
                pass
        print(f"Took {self.steps_taken} steps")
        return move_commands_given

    def auto_run(self, limit=None):       
        """ Calling this method will tell the bot to auto run all paths of the maze
            until it finds the oxygen system. """

        # 1. Move until we hit a wall
        # 2. Turn left 90 degrees and try to move, repeat until succesful
        # 3. Turn right ONCE, try to move 
        #       > If we were able to move, repeat step 3 until we hit a wall
        #       > If we were NOT able to move, go to step 2
        
        if limit != None:
            limit += self.steps_taken
        
        # Step 1:        
        if limit: 
            while self.move_bot() and self.steps_taken <= limit: pass
        else: 
            while self.move_bot(): pass

        while self.computer.enabled and not self.found_oxygen:    
            if limit and self.steps_taken > limit: break
            # Step 2:
            while True:
                self.turn_left()
                no_wall = self.move_bot()
                if no_wall: 
                   break 
    
            # Step  3:
            self.turn_right()
            no_wall = self.move_bot()

            if no_wall:                
                while True:
                    self.turn_right()
                    no_wall = self.move_bot()
                    if not no_wall: 
                        break                    

            self.computer.set_input([self.direction])
    
    def auto_run_inverted(self):        

        # 1. Move until we hit a wall
        # 2. Turn left 90 degrees and try to move, repeat until succesful
        # 3. Turn right ONCE, try to move 
        #       > If we were able to move, repeat step 3 until we hit a wall
        #       > If we were NOT able to move, go to step 2
        
        
        movement_commands_given = 0
        # Step 1:
        while self.move_bot(): 
            movement_commands_given += 1

        while self.computer.enabled and not self.found_oxygen:    
            # Step 2:
            while True:
                self.turn_right()
                no_wall = self.move_bot()
                movement_commands_given += 1
                if no_wall: 
                   break 
    
            # Step  3:
            self.turn_left()
            no_wall = self.move_bot()

            if no_wall:                
                while True:
                    self.turn_left()
                    no_wall = self.move_bot()
                    movement_commands_given += 1
                    if not no_wall: 
                        break                    

            self.computer.set_input([self.direction])
        
        return movement_commands_given
    
    def auto_map(self, prev_direction=None):       
        """ Calling this method will tell the bot to auto run all paths of the maze
            until it finds the oxygen system. """

        # 1. Check all 4 cardinal directions for walls by trying to move 
        #    foward, then back again if moving was succesful
        #
        #       > Add each found wall to self.walls (this is done by the bot automatically)
        #       > Add each path found to < paths to traverse > 
        #       

        while self.computer.enabled and not self.found_oxygen:    
            
            # Save my current direction:
            orig_direction = self.direction            

            # Try to move in that direction:
            orig_path_clear = self.move_bot(exploring=True)
            if orig_path_clear: 
                self.turn_180(); self.move_bot(exploring=True)

            paths = [] # Clones 
            
            wall_count = 0

            # 1. Check each direction for walls and paths:
            for direction in self.directions:
                self.direction = direction
            
                # If bot was able to move: Path found!                
                if self.move_bot(exploring=True):
                    if direction != orig_direction and direction != prev_direction:                     
                        # If original path is blocked, choose a new one:
                        if not orig_path_clear:
                            orig_direction = self.direction
                            orig_path_clear = True

                        # THIS bot is going to travel in that direction, so 
                        # no need to clone a bot to do it, and don't go backwards!
                        elif direction != orig_direction and direction != prev_direction: 
                            if self.loc not in self.visited:
                                clone = self.clone_bot()
                                clone.prev = self.prev
                                paths.append(clone)

                    # Turn around and return to the home square:
                    self.turn_180(); self.move_bot(exploring=True)
                else:
                    wall_count += 1

            # Traverse each path with a new robot:
            for clone in paths:                
                clone.auto_map()                                
                self.walls.update(clone.walls)
                self.prev.add_branch(clone.root)

                if clone.found_oxygen:
                    self.root = clone.oxygen_node

            # If we're at a dead end, return:
            if wall_count == 3 and not orig_path_clear: 
                return 

            # Continue forward in the orignal direction:
            self.direction = orig_direction
            self.move_bot()

            prev_direction = self.opposite(orig_direction)
    
#+----------------------------------------------------------------------------+
#|                              Methods                                       |
#+----------------------------------------------------------------------------+

def move_cursor(row, col):        
    print(f"\u001b[{row};{col}H", end='') 

def print_symbol(loc, direction, symbol, pause=False):
    wall = loc
    move_cursor(wall[1] + G_OFFSET, wall[0] + G_OFFSET)
    if pause: time.sleep(0.1)
    print(symbol)

def print_bot(loc, old_loc, direction):
    # Remove old bot print:
    print_symbol(old_loc, direction, symbol=' ')

    # Print new bot location:
    icons = {1:'▲', 2: '▼', 3:'◀',4: '▶'}
    print_symbol(loc, direction, symbol=icons[direction])

def get_data(path): 
    return [ int(n.rstrip('\n')) for n in open(path).readline().split(',')]

#+----------------------------------------------------------------------------+
#|                  Load Maze data for visualization:                         |
#+----------------------------------------------------------------------------+
# rows = dict()
# with open('rows_data.json') as f:
#     rows = json.load(f)

# rows2 = dict()
# with open('rows_data_inverted.json') as f:
#     rows2 = json.load(f)

int_rows = {}
# for row, d in rows.items():
#     row = int(row)
#     int_rows[row] = {}
#     for loc, sym in d.items():
#         int_rows[row][eval(loc)] = sym

# for row, d in rows2.items():
#     row = int(row)    
#     for loc, sym in d.items():
#         int_rows[row][eval(loc)] = sym

#+----------------------------------------------------------------------------+
#|                      Maze Mapping used by both parts:                      |
#+----------------------------------------------------------------------------+

os.system('cls'); os.system('cls')

visualize = False
visualize = True

INTERVAL = 0.01

min_row, min_col, max_row, max_col = 0,0,0,0

# Print Maze:
if False and visualize:
    print()
    for y_val, row in sorted(int_rows.items()):
        if y_val > max_row: max_row = y_val
        for loc, symbol in sorted(row.items()):
            print_symbol(loc, 1, symbol)
        #time.sleep(0.1)
        print()

data = get_data("d15_input.txt")
fred = RepairBot(data, interval=INTERVAL, visualize=visualize, wall_data=int_rows)
#fred.auto_run()
#fred.auto_map()

#+----------------------------------------------------------------------------+
#|                  Generate Maze data for visualization:                     |
#+----------------------------------------------------------------------------+

# every row coord gets it's own list, 
# print each row as list, sort each row by x coord
# find way to NOT use control codes to print
if False:
    rows = defaultdict(dict)
    for loc in fred.walls:
        rows[loc[1]][str(loc)] = fred.walls[loc] 

    rows_json = json.dumps(rows, indent=2, sort_keys=True)
    with open('rows_data_inverted.json',mode='w') as f:
        f.writelines(rows_json)

    print(f"Max Row: {max_row}, Max Col: {max_col}")
    print(f"min Row: {min_row}, min Col: {min_col}")

#+----------------------------------------------------------------------------+
#|                             Part 1: Hardcoded                              |
#+----------------------------------------------------------------------------+

if True:
    data = get_data("d15_input.txt")
    fred = RepairBot(data, interval=INTERVAL, visualize=visualize, wall_data=int_rows)

    direction_commands = [1, 1, 3, 3, 2, 2, 2, 2, 4, 4, 
    4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 1, 1, 3, 3, 2, 2, 2, 2, 
    2, 2, 3, 3, 3, 3, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 3, 3, 2, 2, 3, 3, 
    1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 4, 4, 2, 2, 4, 4, 1, 1, 4, 4, 1, 1, 
    1, 1, 3, 3, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 4, 4, 1, 1, 4, 4, 4, 4, 
    1, 1, 3, 3, 1, 1, 4, 4, 4, 4, 2, 2, 4, 4, 4, 4, 2, 2, 3, 3, 2, 2, 
    2, 2, 2, 2, 4, 4, 4, 4, 1, 1, 3, 3, 1, 1, 4, 4, 1, 1, 4, 4, 2, 2, 
    4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 
    3, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 2, 
    2, 2, 2, 3, 3, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 3, 3, 2, 2, 3, 3, 1, 
    1, 1, 1, 3, 3, 3, 3, 3, 3, 2, 2, 4, 4, 4, 4, 2, 2, 3, 3, 2, 2, 2, 
    2, 4, 4, 4, 4, 4, 4, 1, 1, 3, 3, 3, 3]

    print("Move commands given:",fred.auto_run_inverted())
    #print("Move commands given:",fred.semi_auto_run(direction_commands))
    print(fred.oxygen_location)
    print(f"Took {fred.steps_taken} steps")

#+----------------------------------------------------------------------------+
#|                             Part 2:                                        |
#+----------------------------------------------------------------------------+

def travel_path(node: Path, printed_locs, path_length, longest=None):
    l = node.loc

    if l not in printed_locs:
        printed_locs.add(l)
        if visualize:
            move_cursor(l[1]+1, l[0]+1)
            print('░')
            time.sleep(0.01)
        move_cursor(45,0); print("Current path length:",path_length)
        path_length += 1
    
    if node.prev and node.prev.loc not in printed_locs:
        travel_path(node.prev, printed_locs, path_length, longest)

    for branch in ( b for b in node.branches if b.loc not in printed_locs):
        travel_path(branch, printed_locs, path_length, longest)

    if path_length > longest[0]: longest[0] = path_length

if False:
    printed_locs = set()
    length = [0]
    travel_path(fred.root, printed_locs, 0, length)
    
    move_cursor(50,0); print("Longest path length is: ", length[0]-1)