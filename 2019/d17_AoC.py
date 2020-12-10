import os
import time 
from collections import defaultdict

GX_OFFSET = 0
GY_OFFSET = 1

#+----------------------------------------------------------------------------+
#|                                Classes                                     |
#+----------------------------------------------------------------------------+

class Computer:
    def __init__(self, tape, name=None, inp_stack=None, output_mode=None, input_mode=None):
        self.name = name
        self.enabled = True
        self.tape = tape            # Stores this comptuers program
        self.inp_stack = inp_stack  # Op code 3 gets input from here

        if self.inp_stack == None: self.inp_stack = []

        self.i = 0                  # Instruction pointer
        self.rel_base = 0

        self.output_mode = output_mode # By default, output is printed to stdout
                                       # if mode='return', execution in method compute()
                                       # pauses and the output is returned to the calling thread

        self.input_mode = input_mode 

        self.last_computed_value = 0

        self.output_list = []

        # Increase the amount of "empty memory" available by default:
        self.tape += [ 0 for n in range(len(self.tape)*500) ]

        # Make tape a dict because why not ? Just doing this to see if it will be faster.
        #self.tape = { n:val for n,val in enumerate(self.tape) }
    
    def clone(self):
        """ Returns a complete copy of the current VM in it's current state """
        clone = Computer(self.tape[:], inp_stack=self.inp_stack[:], output_mode=self.output_mode)
        clone.i = self.i 
        clone.rel_base = self.rel_base
        clone.last_computed_value = self.last_computed_value
        return clone 


    def set_input(self, items:list):
        self.inp_stack = items

    def cur_instr(self):
        """ Get instruction pointed at by self.i """
        return self.tape[self.i]

    def set_(self, index, val):
        """ Set value at position 'index' to be 'val' """
        self.tape[index] = val

    def get_(self, index):
        """ Return value stored at 'index' """
        return self.tape[index]

    def get_indexes(self, *args):
        """ Method for handeling the three different parameter modes.

            Accepts up to N args which are the modes for N parameters.

            Based on what a,b and c, etc are, returns the appropriate index to be used.
            a,b, and c, etc are the parameter modes.

            If you enter a, it will return just one index.
            If you enter a and b, it will return two indexes.
            If you enter a, b, and c, it will return three indexes.
            
            Up to N arguments.

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
        def get_index(a, offset):
            p = self.i + offset                            # Imediate mode
            if   a == 0: p = self.get_(p)                  # Positional
            elif a == 2: p = self.rel_base + self.get_(p)  # Relative
            return p

        indexes = [ get_index(arg, offset) for offset,arg in enumerate(args,start=1) ]

        return indexes[0] if len(indexes) == 1 else indexes

    def compute(self, user_inp=None):
        """ Iterates over self.tape, executing instructions until a HALT op is encountered,
            or data is returned (op 4) which pauses execution of the computer
        """
        # NOTE: '<index>' Is read as, The value at 'index'.
        # EXAMPLE: <p1> + <p2> Is read as " The value at index p1 plus the value at index p2 "

        if user_inp != None:
            self.inp_stack.insert(0, user_inp)

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

            # Execute the op:
            if op == '01': # Adds <p1> + <p2>
                p1, p2, p3 = self.get_indexes(m1,m2,m3)
                self.set_( p3, val=(self.get_(p1) + self.get_(p2)) )
                self.i += 4

            elif op ==  '02': # Multiplies <p1> * <p2>
                p1, p2, p3 = self.get_indexes(m1,m2,m3)
                self.set_( p3, val=(self.get_(p1) * self.get_(p2)) )
                self.i += 4

            elif op ==  '03':  # Get input
                input_val = None
                if self.input_mode == 'user':
                    input_val = input(">>>: ").rstrip()
                else:
                    input_val = self.inp_stack.pop(0)
                
                if input_val == "\\n": input_val = '\n'
                if len(input_val) == 1: 
                    input_val = ord(input_val)

                p1 = self.get_indexes(m1)
                #self.set_( p1, val=input_val )
                self.set_( p1, val=int(input_val) )
                self.i += 2

            elif op ==  '04':  # Return output
                p1 = self.get_indexes(m1)
                output = self.get_(p1)
                self.last_computed_value = output

                self.i += 2 # Increment BEFORE returning

                if self.output_mode=='return': return output
                else:                          print(output)

            elif op ==  '05':  # Jump-If-True: Sets instr pointer to <p2> if <p1> is non-zero
                p1,p2 = self.get_indexes(m1,m2)
                if self.get_(p1) > 0:
                    self.i = self.get_(p2)
                else:
                    self.i += 3

            elif op ==  '06': # Jump-If-False: Sets instr pointer to <p2> if <p1> is zero
                p1,p2 = self.get_indexes(m1,m2)
                if self.get_(p1) == 0:
                    self.i = self.get_(p2)
                else:
                    self.i += 3

            elif op ==  '07': # Stores 1 in <p3> if <p1> < <p2> else stores 0
                p1,p2,p3 = self.get_indexes(m1,m2, m3)
                if self.get_(p1) < self.get_(p2): self.set_( p3, val=1 )
                else:                   self.set_( p3, val=0 )
                self.i += 4

            elif op ==  '08':  # Stores 1 if <p1> == <p2> else stores 1
                p1,p2,p3 = self.get_indexes(m1,m2,m3)
                if self.get_(p1) == self.get_(p2): self.set_( p3, val=1 )
                else:                    self.set_( p3, val=0 )
                self.i += 4

            elif op ==  '09': # Change the relative boost value:
                p1 = self.get_indexes(m1)
                self.rel_base += self.get_(p1)
                self.i += 2
            
            elif op == '99':
                self.enabled = False
                self.i == len(self.tape)
                return 0

# class Scaffold:
#     def __init__(self, loc):
#         self.loc = loc
#         self.connecting_count = 0

#+----------------------------------------------------------------------------+
#|                              Methods                                       |
#+----------------------------------------------------------------------------+

def move_cursor(row, col):        
    print(f"\u001b[{row};{col}H", end='') 

def print_symbol(loc, direction, symbol, pause=False):
    wall = loc
    move_cursor(wall[1] + GY_OFFSET, wall[0] + GX_OFFSET)
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
#|                                Part 1                                      |
#+----------------------------------------------------------------------------+

def check_neighbors(l, scaffolding, connections):    
    for n in [(l[0], l[1]-1), (l[0], l[1]+1),(l[0]-1, l[1]), (l[0]+1, l[1])]:
        if n in scaffolding and (n,l) not in connections and (l,n) not in connections:
            scaffolding[n] += 1
            scaffolding[l] += 1
            connections.add((n,l))
            connections.add((l,n))

if False:
    data = get_data("d17_input.txt")
    pc = Computer(data, output_mode='return')

    row, col = 0, 0
    scaffolding = dict()
    connections = set()
    total_output_count = 0
    while pc.enabled:
        output = chr(pc.compute())
        total_output_count += 1
        
        if output == '.': print(' ', end='');  col += 1            

        elif output == '#': 
            # Add current scaffold to the dict:
            scaffolding[(row, col)] = 0 

            # Check for neighboring scaffolding:
            # Function will count how many neighbors each scaffold peice has
            check_neighbors((row,col), scaffolding, connections)

            print('▒', end='')
            col += 1

        else: 
            print(output, end='')
            if output == '\n':
                row += 1
                col = 0
            else:
                col += 1
    print("Total output chars printed", total_output_count)

    # Check each scaffold peice; Peices with 4 neighbors are intersections:
    sum_align_params = 0
    for peice, count in scaffolding.items():
        if count == 4: 
            align_param = peice[0]*peice[1]
            sum_align_params += align_param
            
    print(sum_align_params)

#+----------------------------------------------------------------------------+
#|                                Part 2                                      |
#+----------------------------------------------------------------------------+

def commatize(*args):
    a_list = []
    for arg in args:
        for item in arg:
            a_list.append(item)
            a_list.append(',')
        a_list.pop()
        a_list.append('\n')
    return a_list

if True:
    os.system('cls'); os.system('cls') 
    
    data = get_data("d17_input.txt"); data[0] = 2
    pc = Computer(data, output_mode='return')
    
    A = "R91L93R6"     
    B = "R6R91R93R6" 
    C = "R91L93L93"    

    funcs = {
        'Main': "AABCBCBCBA",
        'A'    : A,
        'B'    : B,
        'C '   : C,
        'feed' : 'n',
    }

    path_string = """ R 10 L 12 R 6 R 10 L 12 R 6 R 6 R 10 R 12 R 6 R 10 L 12 L 12 R 6 R 10 R 12 R 6
                      R 10 L 12 L 12 R 6 R 10 R 12 R 6 R 10 L 12 L 12 R 6 R 10 R 12 R 6 R 10 L 12 R 6"""

    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    move_cursor(0,0)

    chars_printed = 0
    row, col = 0, 0
    pc.inp_stack = commatize(*funcs.values())

    row_str = ''

    dust_collected = 0
    while pc.enabled:        
        num_out = pc.compute()
        output = chr(num_out)
        if len(str(num_out)) > 3: 
            dust_collected = num_out
        
        if output not in 'vVX' and (output in abc or output in abc.lower() or output in ':?'):
            #input("Pause...")
            continue 

        chars_printed += 1
        
        if chars_printed > 1718:
            #move_cursor(0,0)
            chars_printed = 1
            #time.sleep(0.0001)   
            row = 0        
        
        if output == '.': 
            #print(' ', end='');  
            row_str += ' '
            col += 1            

        elif output == '#': 
            #print('▒', end='')
            row_str += '▒'
            col += 1

        else: 
            #print(output, end='')
            row_str += output
            if output == '\n':
                #move_cursor(row, 0)
                if len(row_str) > 4:
                    print(row_str, end='')
                row_str = ''
                row += 1
                col = 0
                
            else:
                col += 1
    
    print(dust_collected)
                