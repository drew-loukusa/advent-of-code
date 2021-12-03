from aocd.models import Puzzle


def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode="w+") as f:
        data = puzzle.input_data
        f.write(data)


Year = 2020
Day = 23

puzzle = Puzzle(year=Year, day=Day)
save_input_to_file(puzzle, day=Day)

infile = "day23ex.txt"
infile = "day23.txt"
lines = [line.rstrip() for line in open(infile)]

# Part 1
if True:
    for line in lines:
        pass
    # puzzle.answer_a = result

# Part 2
if True:
    pass

    # puzzle.answer_b = result
