
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
        self.tape += [ 0 for n in range(len(self.tape)*500) ]

    def set_input(self, items:list):
        self.inp_stack = items

    def get_instr(self):
        """ Get instruction pointed at by self.i """
        return self.tape[self.i]
        
    def compute(self):
        """ Iterates over self.tape, executing instructions until a HALT op is encountered, 
            or data is returned (op 4) which pauses execution of the computer
        """
        def get_indexes(a,b=None,c=None):
            """ Based on what a,b and c are, returns the appropriate index to be used.
                a,b, and c are the parameter modes. 

                If you enter a, it will return just one index.
                If you enter a and b, it will return two indexes.
                If you enter a, b, and c, it will return three indexes.
            """

            # The default mode is set to be immediate mode (mode 1)
            p1,p2,p3 = None, None, None
            if a != None: p1 = self.i+1
            if b != None: p2 = self.i+2
            if c != None: p3 = self.i+3

            # Handle positional mode: (mode 0)
            if a != None and a == 0: p1 = self.tape[p1]
            if b != None and b == 0: p2 = self.tape[p2]   
            if c != None and c == 0: p3 = self.tape[p3]

            # Handle Relative mode: (mode 2)
            if a != None and a == 2: p1 = self.rel_base + self.tape[p1]
            if b != None and b == 2: p2 = self.rel_base + self.tape[p2]           
            if c != None and c == 2: p3 = self.rel_base + self.tape[p3]

            if c == None and b == None: return p1
            if c == None:               return p1, p2
            if c != None:               return p1, p2, p3

        def _op_99():
            self.enabled = False
            self.i == len(self.tape)
            return 'HALT'

        def _op_01(): # Add p1 + p2
            p1, p2, p3 = get_indexes(m1,m2,m3)        
            self.tape[p3] = self.tape[p1] + self.tape[p2]        
            self.i += 4

        def _op_02(): # Multiple p1 * p2
            p1, p2, p3 = get_indexes(m1,m2,m3)        
            self.tape[p3] = self.tape[p1] * self.tape[p2]
            self.i += 4

        def _op_03():  # Get input
            #user_in = input(">>> type a number: ")
            user_in = self.inp_stack.pop(0)
            p1 = get_indexes(m1)                
            self.tape[p1] = int(user_in)
            self.i += 2

        def _op_04():  # Return output
            output = self.tape[get_indexes(m1)]                 
            self.last_computed_value = output
            
            if self.output_mode=='return': return output
            else:                          print(output)                    
            self.i += 2

        def _op_05():  # Jump to p2 if p1 is non-zero
            p1,p2 = get_indexes(m1,m2)      
            if self.tape[p1] > 0: self.i = self.tape[p2]
            else: self.i += 3

        def _op_06(): # Jump to p2 if p1 is zero
            p1,p2 = get_indexes(m1,m2)       
            if self.tape[p1] == 0: self.i = self.tape[p2]    
            else: self.i += 3

        def _op_07(): # Stores 1 in p3 if p1 < p2 else stores 0
            p1,p2,p3 = get_indexes(m1,m2, m3)        
            if self.tape[p1] < self.tape[p2]: self.tape[p3] = 1
            else:                             self.tape[p3] = 0
            self.i += 4

        def _op_08():  # Stores 1 if p1 == p2 else stores 1 
            p1,p2,p3 = get_indexes(m1,m2,m3)                
            if self.tape[p1] == self.tape[p2]: self.tape[p3] = 1
            else:                              self.tape[p3] = 0
            self.i += 4

        def _op_09(): # Change the relative boost value:
            p1 = get_indexes(m1)
            self.rel_base += self.tape[p1]
            self.i += 2

        # Tie each op to its' associated function:
        ops = { '99':_op_99, '01':_op_01, '02':_op_02, '03':_op_03, '04':_op_04,
                '05':_op_05, '06':_op_06, '07':_op_07, '08':_op_08, '09':_op_09}

        while self.i < len(self.tape):                
            # Process op code
            instr  = str(self.get_instr())
            op     = instr[len(instr)-2:]
            pmodes = instr[:len(instr)-2]

            # Extract parameter modes from the instruction:
            m1,m2,m3 = 0,0,0
            if len(pmodes) > 0:
                pmodes = list(pmodes)
                reversed(pmodes)

                if len(pmodes) > 0: m1 = int(pmodes.pop())
                if len(pmodes) > 0: m2 = int(pmodes.pop())
                if len(pmodes) > 0: m3 = int(pmodes.pop())

            # Make sure op is in correct format:
            if len(op) == 1: op = '0' + op 

            # Execute the op: 
            result = ops[op]() 
            if result != None: 
                if result == 'HALT': break 
                else: return result

get_data = lambda path: [ int(n.rstrip('\n')) for n in open(path).readline().split(',')]

#+----------------------------------------------------------------------------+
#|                                  Tests                                     |
#+----------------------------------------------------------------------------+
if False: 

    print("-"*80)
    print("TESTS:\n")

    if True:
        print("Test 1:")
        # Data is: 109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 
        # Produces a copy of itself as output, takes NO input.
        data = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        boost_pc = Computer(name='Gordon', tape=data)
        boost_pc.compute()

    if True:
        print("\nTest 2:")
        # should output a 16-digit number.
        data = [1102,34915192,34915192,7,4,7,99,0]
        boost_pc = Computer(name='Gordon', tape=data)
        boost_pc.compute()

        if len(str(boost_pc.last_computed_value)) == 16: print("Outputted a 16 digit number!")

    if True:
        print("\nTest 3")
        # should output the large number in the middle.
        data = [104,1125899906842624,99]
        boost_pc = Computer(name='Gordon', tape=data)
        boost_pc.compute()

        if boost_pc.last_computed_value == 1125899906842624: print("Outputted the correct number!")

    print("-"*80)

#+----------------------------------------------------------------------------+
#|                                  Part 1                                    |
#+----------------------------------------------------------------------------+

data = get_data("d9_input.txt")
Computer(tape=data, inp_stack=[1]).compute()

#+----------------------------------------------------------------------------+
#|                                  Part 2                                    |
#+----------------------------------------------------------------------------+

data = get_data("d9_input.txt")
Computer(tape=data, inp_stack=[2]).compute()
