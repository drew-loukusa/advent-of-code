data = [ int(n) for n in open("d7_input.txt").readline().split(',') ] 
#data = [ int(n) for n in open("d7_test_input1.txt").readline().split(',') ] 

def computer(tape, user_in_stack):
    def get_params(a,b,c=None):
        p1,p2,p3 = tape[i+1], tape[i+2], c
        if a == 0: p1 = tape[p1]
        if b == 0: p2 = tape[p2]   
        if c != None: return p1, p2, p3
        else:         return p1, p2

    output = None

    i = 0
    while i < len(tape):
        # Process op code
        fop = str(tape[i]) 
        op = fop[len(fop)-2:]
        fop = fop[:len(fop)-2]

        #time.sleep(0.5)
        #print(op, type(op))

        a,b,c = 0,0,0
        if len(fop) > 0:
            fop = list(fop)
            reversed(fop)

            if len(fop) > 0: a = int(fop.pop())
            if len(fop) > 0: b = int(fop.pop())
            if len(fop) > 0: c = int(fop.pop())
            # Done wit op code 

        if op == '99': 
            break

        elif op in '01': 
            p1, p2, p3 = get_params(a,b,tape[i+3])        
            tape[p3] = p1 + p2        
            i += 4

        elif op in '02': 
            p1, p2, p3 = get_params(a,b,tape[i+3])        
            tape[p3] = p1 * p2
            i += 4

        elif op in '03':
            #user_in = input(">>> type a number: ")
            user_in = user_in_stack.pop(0)
            p1 = tape[i+1]
            tape[p1] = int(user_in)
            i += 2

        elif op in '04':
            output = tape[tape[i+1]]
            #print(output)
            i += 2

        elif op in '05':
            p1,p2 = get_params(a,b)      
            if p1 > 0: i = p2
            else: i += 3

        elif op in '06': 
            p1,p2 = get_params(a,b)       
            if p1  == 0: i = p2        
            else: i += 3

        elif op in '07':
            p1,p2,p3 = get_params(a,b, tape[i+3])        
            if p1 < p2: tape[p3] = 1
            else:       tape[p3] = 0
            i += 4

        elif op in '08':
            p1,p2 = get_params(a,b)
            p3 = tape[i+3]
            if p1 == p2: tape[p3] = 1
            else:        tape[p3] = 0
            i += 4
    return output

import itertools
perms = list(itertools.permutations([0, 1, 2, 3, 4]))

biggest_output = 0
for perm in perms:
    user_in_stack = list(perm)
    user_in_stack.insert(1,0)
    for _ in range(5): # Run each amp:
        tape_copy = data[:]
        output = computer(tape_copy, user_in_stack)    
        user_in_stack.insert(1, output)

    if output > biggest_output: 
        biggest_output = output

print(biggest_output)