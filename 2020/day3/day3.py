from aocd.models import Puzzle

def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode='w+') as f:
        data = puzzle.input_data
        f.write(data)

Year=2020
Day=3

puzzle = Puzzle(year=Year, day=Day)
#save_input_to_file(puzzle, day=Day)

infile = "day3ex.txt"
infile = "day3.txt"

def count_trees_per_slope(dx,dy):
    x,y = 0,0
    num_trees = 0
    lines = [line.rstrip() for line in open(infile)]
    while y < len(lines):
        line = lines[y]
        
        # Check if current positon has a tree
        if line[x] == '#':
            num_trees += 1

        # Move position 
        max_x = len(line)
        x += dx 
        y += dy
        if x >= max_x: x = x - max_x 
    return num_trees

# Part 1
if False:
    dx,dy = 3,1
    num_trees = count_trees_per_slope(dx,dy)
    print(num_trees)
    #puzzle.answer_a = num_trees

# Part 2
if True:
    slopes = [(1,1),(3,1),(5,1),(7,1),(1,2)]
    result = 1
    for dx,dy in slopes:
        result *= count_trees_per_slope(dx,dy)
    print(result)

    #puzzle.answer_b = result
