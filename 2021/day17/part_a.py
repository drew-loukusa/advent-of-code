# https://adventofcode.com/2021/day/17

import sys
import math
import functools
from collections import namedtuple
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

AxisRange = namedtuple("AxisRange", ['min','max'])
TargetRange = namedtuple("TargetRange", ['x', 'y'])

def process(infile):
    """Process the input file into a data structure for solve()"""
    tokens = open(infile).readline().rstrip().split()
    xs, xe = tokens[2].lstrip("x=").rstrip(',').split("..")
    ys, ye = tokens[3].lstrip("y=").split("..")
    x = AxisRange(int(xs), int(xe))
    y = AxisRange(int(ys), int(ye))
    return TargetRange(x,y)

@functools.cache
def launch_probe(t: TargetRange , vx, vy):
    max_y = 0
    tx: AxisRange = t.x 
    ty: AxisRange = t.y

    x,y = 0,0 # Always starts at the origin 
    points: set = {(0,0)}

    # step indefinitly, (for now...)
    while True:
        # Update position 
        x += vx 
        y += vy 
        max_y = max(y, max_y)

        points.add((x,y))

        # Update velocities
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1

        vy -= 1

        # Landed in the target area
        if ((x >= tx.min and x <= tx.max) and 
            (y >= ty.min and y <= ty.max)):
            return True, max_y

        elif ((x > tx.max and y > ty.max)
            or (vy < 0 and y < ty.min)):
            return False, 0

def solve(target_range: TargetRange):
    tx: AxisRange = target_range.x 
    max_height = 0

    # This is dumb. If you give the probe a greater y velocity than x velocty
    # then it just hits a wall and it starts to "travel" straight up, until
    # it runs out of postive y velocity. 

    # All you have to do is give the probe the minimum velocity needed 
    # to reach the square, then just run the launch_probe a bunch.

    # I picked 1000 computations, arbitrarily. Just keep increasing the y velocity
    # and then return the highest one. 
    
    # We want to travel K distance. Since the x velocity decreases by 1 each 
    # step due to drag, we can calculate how much initial velocity to give the probe
    # by using the formual for a sum of numbers from 1 to n:
    # k = n(n+1)/2 
    # 2k = n^2 + n 
    # n^2 + n - 2k = 0
    # Use quadratic formula:
    # n = 1/2 * sqrt((8*k+1) - 1) 
    vx = math.ceil(0.5 * (math.sqrt(8 * tx.min + 1) - 1)) + 1
    vy = 0

    # If increasing vy failed, and decreasing vx failed, 
    # then we have a max height arc and are done
    calculations = 0
    while calculations < 1000:
        # Simulate the probe launch 
        # It's cached, so really this is just retreiving the results from the last
        # succesful launch
        in_area, new_max_height = launch_probe(target_range, vx, vy)

        # Check arc height vs current max arc height 
        # but only if the last launch landed in the target zone
        if in_area:
            max_height = max(max_height, new_max_height)

        # Always increase vy
        vy += 1
        increase_vy, _ = launch_probe(target_range, vx, vy)

        calculations += 1

    return max_height

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 17
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("ex0.txt", ans=45)

    # Run question 
    aoc.test("puzzle_input.txt", ans=3916, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
