
tape = [int(n) for n in open("d5_input.txt").readline().split(',')]

def get_params(a,b,c=None):
    p1,p2,p3 = tape[i+1], tape[i+2], c
    if a == 0: p1 = tape[p1]
    if b == 0: p2 = tape[p2]   
    if c != None: return p1, p2, p3
    else:         return p1, p2

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

    if op in '01': 
        p1, p2, p3 = get_params(a,b,tape[i+3])        
        tape[p3] = p1 + p2        
        i += 4

    if op in '02': 
        p1, p2, p3 = get_params(a,b,tape[i+3])        
        tape[p3] = p1 * p2
        i += 4

    if op in '03':
        user_in = input(">>> type a number: ")
        p1 = tape[i+1]
        tape[p1] = int(user_in)
        i += 2

    if op in '04':
        print(tape[tape[i+1]])
        i += 2

    if op in '05':
        p1,p2 = get_params(a,b)      
        if p1 > 0: i = p2
        else: i += 3

    if op in '06': 
        p1,p2 = get_params(a,b)       
        if p1  == 0: i = p2        
        else: i += 3

    if op in '07':
        p1,p2,p3 = get_params(a,b, tape[i+3])        
        if p1 < p2: tape[p3] = 1
        else:       tape[p3] = 0
        i += 4

    if op in '08':
        p1,p2 = get_params(a,b)
        p3 = tape[i+3]
        if p1 == p2: tape[p3] = 1
        else:        tape[p3] = 0
        i += 4

# input 5:
# answer: 14110739    

#print(tape)
#print(tape[0])