import time 

GX_OFFSET = 0
GY_OFFSET = 1

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
        """ Returns a complete copy of the current VM in it's current state """
        clone = Computer(self.tape[:], inp_stack=self.inp_stack[:], output_mode=self.output_mode)
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
            
            # Execute the op:
            result = execute_[op]()
            if result != None:
                if result == 'HALT': break
                else: return result

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

if True:
    data = get_data("d17_input.txt")
    pc = Computer(data, output_mode='return')
    