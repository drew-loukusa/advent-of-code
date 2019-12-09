
class Computer:
    def __init__(self, tape, name=None, inp_stack=None):
        self.name = name
        self.enabled = True         
        self.tape = tape            # Stores this comptuers program
        self.inp_stack = inp_stack  # Op code 3 gets input from here 
        self.i = 0                  # Instruction pointer
        self.rel_base = 0

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

        output = None

        while self.i < len(self.tape):                
            # Process op code
            instr  = str(self.get_instr())
            op     = instr[len(instr)-2:]
            pmodes = instr[:len(instr)-2]

            if instr == '203' or instr == '209': 
                foo = 0; foo += 1

            # Extract parameter modes from the instruction:
            m1,m2,m3 = 0,0,0
            if len(pmodes) > 0:
                pmodes = list(pmodes)
                reversed(pmodes)

                if len(pmodes) > 0: m1 = int(pmodes.pop())
                if len(pmodes) > 0: m2 = int(pmodes.pop())
                if len(pmodes) > 0: m3 = int(pmodes.pop())

            if op == '99': 
                self.enabled = False
                self.i == len(self.tape)
                break

            elif op in '01': # Add p1 + p2
                p1, p2, p3 = get_indexes(m1,m2,m3)        
                self.tape[p3] = self.tape[p1] + self.tape[p2]        
                self.i += 4

            elif op in '02': # Multiple p1 * p2
                p1, p2, p3 = get_indexes(m1,m2,m3)        
                self.tape[p3] = self.tape[p1] * self.tape[p2]
                self.i += 4

            elif op in '03': # Get input
                #user_in = input(">>> type a number: ")
                user_in = self.inp_stack.pop(0)
                p1 = get_indexes(m1)                
                self.tape[p1] = int(user_in)
                self.i += 2

            elif op in '04': # Return output
                output = self.tape[get_indexes(m1)]                 
                self.last_computed_value = output
                #return output
                print(output)
                self.i += 2

            elif op in '05': # Jump to p2 if p1 is non-zero
                p1,p2 = get_indexes(m1,m2)      
                if self.tape[p1] > 0: self.i = self.tape[p2]
                else: self.i += 3

            elif op in '06': # Jump to p2 if p1 is zero
                p1,p2 = get_indexes(m1,m2)       
                if self.tape[p1] == 0: self.i = self.tape[p2]    
                else: self.i += 3

            elif op in '07': # Stores 1 in p3 if p1 < p2 else stores 0
                p1,p2,p3 = get_indexes(m1,m2, m3)        
                if self.tape[p1] < self.tape[p2]: self.tape[p3] = 1
                else:                             self.tape[p3] = 0
                self.i += 4

            elif op in '08': # Stores 1 if p1 == p2 else stores 1 
                p1,p2,p3 = get_indexes(m1,m2,m3)                
                if self.tape[p1] == self.tape[p2]: self.tape[p3] = 1
                else:                              self.tape[p3] = 0
                self.i += 4
            
            elif op in '09': # Change the relative boost value:
                p1 = get_indexes(m1)
                self.rel_base += self.tape[p1]
                self.i += 2

        return output

def get_data(path):
    return [ int(n.rstrip('\n')) for n in open(path).readline().split(',')]

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
boost_pc = Computer(tape=data, inp_stack=[1])
boost_pc.compute()

#+----------------------------------------------------------------------------+
#|                                  Part 2                                    |
#+----------------------------------------------------------------------------+

data = get_data("d9_input.txt")
boost_pc = Computer(tape=data, inp_stack=[2])
boost_pc.compute()
