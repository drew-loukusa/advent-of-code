from aocd.models import Puzzle

def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode='w+') as f:
        data = puzzle.input_data
        f.write(data)

Year=2020
Day=5

puzzle = Puzzle(year=Year, day=Day)
#save_input_to_file(puzzle, day=Day)

infile = "day5.txt"
lines = [line.rstrip() for line in open(infile)]

#           Pass         row, col, id 
#  id = row * 8 + col 
example1 = ["BFFFBBFRRR", 70, 7, 567]
example2 = ["FFFBBBFRRR", 14, 7, 119]
example3 = ["BBFFBBFRLL", 102, 4, 820]

# Part 1

def calc_seatID(boarding_pass):
    rowmin, rowmax = 0, 127
    num_rows = 128
    colmin, colmax = 0, 7
    num_cols = 8
    for i in range(7):
        c = boarding_pass[i]
        num_rows = num_rows//2 
        if c == 'F': rowmax -= num_rows
        if c == 'B': rowmin += num_rows
    
    for i in range(7,10):
        c = boarding_pass[i]
        num_cols = num_cols//2
        if c == 'R': colmin += num_cols
        if c == 'L': colmax -= num_cols

    return rowmin*8+colmax

assert calc_seatID(example1[0]) == example1[3] 
assert calc_seatID(example2[0]) == example2[3]
assert calc_seatID(example3[0]) == example3[3]

if False:
    MaxSeatID = 0
    for line in lines: 
        if (newMax := calc_seatID(line)) > MaxSeatID:
            MaxSeatID = newMax
    
    #puzzle.answer_a = MaxSeatID

# Part 2
if True:
    SeatIDs = set()
    for line in lines: 
        SeatIDs.add(calc_seatID(line))
    missingID = 0
    left = None 
    right = None 
    for ID in SeatIDs:
        if ID + 1 not in SeatIDs: 
            if not left or ID > left: 
                left = ID 
        if ID - 1 not in SeatIDs:
            if not right or ID > right: 
                right = ID 
        if right and left and (right - 1 == left + 1):
            missingID = ID 
            print(ID)
            break 
        
    #puzzle.answer_b = missingID
