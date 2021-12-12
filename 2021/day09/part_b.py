# https://adventofcode.com/2021/day/9

import sys
import math 
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test
from part_a import process, locate_low_points

def calc_basin_size(starting_low_point, matrix) -> int:
    """
    CLASSIC.
    Use BFS to walk all the points of a given basin. (dfs would also work)
    Track what we have already walked with a visited set.
    Increment the basin size for each point that we walk.

    Return the basin size as an int.
    """
    q = [starting_low_point]
    MAX_Y = len(matrix) - 1
    MAX_X = len(matrix[0]) - 1

    visited = set()
    cur_basin_size = 0
    while len(q) > 0:
        y,x = q.pop(0)
        row = matrix[y]
        num = row[x]
        # Nines are not a part of any basin, skip them
        if num == 9: 
            continue

        if (y,x) in visited:
            continue
        visited.add((y,x))

        cur_basin_size += 1

        if x > 0 and row[x - 1] > num: # Check left
            q.append((y, x - 1))
        if x < MAX_X and row[x + 1] > num: # Check right
            q.append((y, x + 1))
        if y > 0 and matrix[y - 1][x] > num: # Check up
            q.append((y - 1, x))
        if y < MAX_Y and matrix[y + 1][x] > num: # Check down
            q.append((y + 1, x))
    return cur_basin_size

def solve(matrix):
    # It is totally workable to just run the BFS once you find a low point e.g.
    # While walking the matirx check for low points, then trigger a bfs to fill in a basin

    # BUT... I'm lazy and can re-use code from day 1
    low_points = locate_low_points(matrix)

    basin_sizes = []
    for point in low_points:
        basin_sizes.append(calc_basin_size(point, matrix))

    three_largest_basins = sorted(basin_sizes, reverse=True)[0:3]
    return math.prod(three_largest_basins)

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 9
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day9ex.txt", ans=1134)

    # Run question 
    aoc.test("day9.txt", ans=1235430, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
