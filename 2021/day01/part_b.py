# Sonar sweep part 2
# https://adventofcode.com/2021/day/1#part2

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    return [int(line.rstrip()) for line in open(infile)]

def solve(data):
    increases = 0
    last3sum = None
    cur_sum = 0
    window = []
    for num in data:
        # Shrink window
        if len(window) >= 3:
            if last3sum is not None:
                if last3sum < cur_sum:
                    # print("Increase", end=" ")
                    increases += 1
            # print("last sum:", last3sum)
            last3sum = cur_sum
            cur_sum -= window.pop(0)
        # Grow window
        if len(window) < 3:
            window.append(num)
            cur_sum += num
    # print("Final 3 sum:", last3sum)
    if last3sum is not None:
        if last3sum < cur_sum:
            # print("Increase", end=" ")
            increases += 1
    # print("last sum:", last3sum)
    last3sum = cur_sum
    cur_sum -= window.pop(0)
    return increases

def main(infile):
    return solve(process(infile))

if __name__ == "__main__":
    # Setup
    year, day = 2021, 1
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS
    aoc.test("day1ex.txt", ans=5)

    # Run question 
    aoc.test("day1.txt", ans=1589, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
