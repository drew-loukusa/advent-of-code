from aocd.models import Puzzle
from collections import defaultdict as dd

def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode='w+') as f:
        data = puzzle.input_data
        f.write(data)

Year=2020
Day=8

# puzzle = Puzzle(year=Year, day=Day)
# save_input_to_file(puzzle, day=Day)

infile = "day8ex.txt"
infile = "day8.txt"
lines = [line.rstrip() for line in open(infile)]

# Part 1
if False:
    i = 0
    accumulator = 0
    processed_instrs = set()
    while i < len(lines):
        
        if instr_id in processed_instrs:
            break 
        else:
            processed_instrs.add(instr_id)

        tokens = lines[i].replace('+','').split(' ')
        instr, offset = tokens[0], int(tokens[1])

        # print("cur intstr and offset:", instr, offset)
        # print("accumulator", accumulator)

        if instr == 'acc': 
            accumulator += offset
            i += 1

        elif instr == 'jmp': 
            i += offset

        elif instr == 'nop': 
            i += 1
            continue 

        # print("AFTER PROCESSING INSTR:")
        # print("cur intstr and offset:", instr, offset)
        # print("accumulator", accumulator)
        # input(">>>")

    print(accumulator)

    #puzzle.answer_a = result

# Part 2
if True:

    def process_instructions(lines):
        i = 0
        accumulator = 0
        processed_instrs = set()
        while i < len(lines):
            line = lines[i]
            instr_id = line + str(i)
            if instr_id in processed_instrs:
                i = len(lines)
                accumulator = None
                continue
            else:
                processed_instrs.add(instr_id)

            tokens = line.replace('+','').split(' ')
            instr, offset = tokens[0], int(tokens[1])

            if instr == 'acc': 
                accumulator += offset
                i += 1

            elif instr == 'jmp': 
                i += offset

            elif instr == 'nop': 
                i += 1
                continue 

        return accumulator
    
    for i in range(len(lines)):
        line = lines[i]
        tokens = line.replace('+','').split(' ')
        instr, offset = tokens[0], int(tokens[1])

        if instr in ['jmp', 'nop']: 
            lines_cpy = lines[:]
            a,b = ('jmp','nop') if instr == 'jmp' else ('nop', 'jmp')
            lines_cpy[i] = lines_cpy[i].replace(a,b)
            ans = process_instructions(lines_cpy)
            if ans != None:
                print(ans)

    #puzzle.answer_b = result
