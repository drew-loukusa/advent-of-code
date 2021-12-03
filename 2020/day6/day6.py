from aocd.models import Puzzle
from collections import defaultdict as dd


def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode="w+") as f:
        data = puzzle.input_data
        f.write(data)


Year = 2020
Day = 6

puzzle = Puzzle(year=Year, day=Day)
# save_input_to_file(puzzle, day=Day)

infile = "day6ex.txt"
infile = "day6.txt"
lines = [line.rstrip() for line in open(infile)]

# Part 1
if False:
    asum = 0
    cur_set = set()
    for line in lines:
        for c in line:
            cur_set.add(c)

        if len(line) == 0:
            asum += len(cur_set)
            cur_set = set()

    asum += len(cur_set)
    print(asum)
    # puzzle.answer_a = asum

# Part 2

p2Answer = 3158


def common_in(group):
    common_qs = set("abcdefghijklmnopqrstuvwxqyz")
    for k, v in group.items():
        common_qs = common_qs & v
    return len(common_qs)


if True:
    asum, i, group = 0, 0, dd(set)
    for line in lines:
        for c in line:
            group[i].add(c)
        i += 1

        if len(line) == 0:
            asum += common_in(group)
            group, i = dd(set), 0

    asum += common_in(group)
    print(asum)

    # puzzle.answer_b = asum
