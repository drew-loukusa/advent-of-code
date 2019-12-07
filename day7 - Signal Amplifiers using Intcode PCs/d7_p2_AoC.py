class Computer:
    def __init__(self, name, tape, inp_stack=None):
        self.name = name
        self.enabled = True
        self.tape = tape 
        self.inp_stack = inp_stack # Op code 3 gets input from here 
        self.i = 0 # Instruction pointer

        self.last_computed_value = 0

    def set_input(self, items:list):
        self.inp_stack = items
        
    def compute(self):
        """ Iterates over self.tape, executing instructions until a HALT op is encountered, 
            or data is returned (op 4) which pauses execution of the computer
        """
        def get_params(a,b,c=None):
            p1,p2,p3 = self.tape[self.i+1], self.tape[self.i+2], c
            if a == 0: p1 = self.tape[p1]
            if b == 0: p2 = self.tape[p2]   
            if c != None: return p1, p2, p3
            else:         return p1, p2

        output = None

        while self.i < len(self.tape):
            # Process op code
            fop = str(self.tape[self.i]) 
            op = fop[len(fop)-2:]
            fop = fop[:len(fop)-2]

            a,b,c = 0,0,0
            if len(fop) > 0:
                fop = list(fop)
                reversed(fop)

                if len(fop) > 0: a = int(fop.pop())
                if len(fop) > 0: b = int(fop.pop())
                if len(fop) > 0: c = int(fop.pop())
                # Done wit op code 

            if op == '99': 
                self.enabled = False
                self.i == len(self.tape)
                break

            elif op in '01': # Add p1 + p2
                p1, p2, p3 = get_params(a,b,self.tape[self.i+3])        
                self.tape[p3] = p1 + p2        
                self.i += 4

            elif op in '02': # Multiple p1 * p2
                p1, p2, p3 = get_params(a,b,self.tape[self.i+3])        
                self.tape[p3] = p1 * p2
                self.i += 4

            elif op in '03': # Get input
                #user_in = input(">>> type a number: ")

                user_in = self.inp_stack.pop(0)
                
                p1 = self.tape[self.i+1]
                self.tape[p1] = int(user_in)
                self.i += 2

            elif op in '04': # Return output
                output = self.tape[self.tape[self.i+1]]
                self.i += 2
                self.last_computed_value = output
                return output
                #print(output)

            elif op in '05': # Jump to p2 if p1 is non-zero
                p1,p2 = get_params(a,b)      
                if p1 > 0: self.i = p2
                else: self.i += 3

            elif op in '06': # Jump to p2 if p1 is zero
                p1,p2 = get_params(a,b)       
                if p1  == 0: self.i = p2        
                else: self.i += 3

            elif op in '07': # Stores 1 in p3 if p1 < p2 else stores 0
                p1,p2,p3 = get_params(a,b, self.tape[self.i+3])        
                if p1 < p2: self.tape[p3] = 1
                else:       self.tape[p3] = 0
                self.i += 4

            elif op in '08': # Stores 1 if p1 == p2 else stores 1 
                p1,p2 = get_params(a,b)
                p3 = self.tape[self.i+3]
                if p1 == p2: self.tape[p3] = 1
                else:        self.tape[p3] = 0
                self.i += 4

        return output

from time import sleep 
from itertools import permutations

def compute_signal(amps, phase_codes):
    output = 0
    # Setup each amp with it's phase value and initial input:
    for i, name in enumerate(amps): # Run each amp:         
        amps[name].set_input([phase_codes[i], output])
        output = amps[name].compute()            

    # Loop until E halts:    
    while amps['E'].enabled:
        for i, name in enumerate(amps): # Run each amp:    
            amps[name].set_input([output])
            output = amps[name].compute()      

    return amps['E'].last_computed_value

#+----------------------------------------------------------------------------+
#|                                  Tests                                     |
#+----------------------------------------------------------------------------+
if False:
    data = [ int(n) for n in open("d7_p2_test_input.txt").readline().split(',') ] 
    amps = { char:Computer(name=char, tape=data[:]) for char in "ABCDE" }
    phase_codes = [9,7,8,5,6]
    output = compute_signal(amps, phase_codes)
    print(output)
    # 18216
    if output == 18216: print("Output is correct.")

    data = [ int(n) for n in open("d7_test_input1.txt").readline().split(',') ] 
    amps = { char:Computer(name=char, tape=data[:]) for char in "ABCDE" }
    phase_codes = [9,8,7,6,5]
    output = compute_signal(amps, phase_codes)
    print(output)
    # 139629729
    if output == 139629729: print("Output is correct.")
    #----------------------
    quit()
    #----------------------

#+----------------------------------------------------------------------------+
#|                                  Part 2                                    |
#+----------------------------------------------------------------------------+

data = [ int(n) for n in open("d7_input.txt").readline().split(',') ] 
gen_amps = lambda: { char:Computer(char, data[:]) for char in "ABCDE" }

biggest_output = 0
for perm in permutations([5,6,7,8,9]):

    output = compute_signal(gen_amps(), perm)

    if output > biggest_output: 
        biggest_output = output

print(biggest_output)

