# https://adventofcode.com/2021/day/17

import sys
import math
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

def launch_single_probe(t: TargetRange , vx, vy):
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

def launch_probes(vx, vy, inc_vy, target_range: TargetRange):
    """
    Launch probes for a given vx value until all possible vy values are exausted.
    Return all valid initial velocty pairs for a given x velocity 
    """
    tx: AxisRange = target_range.x 
    max_height = 0

    valid_initial_velocities = set()

    calculations = 0
    while calculations < 1000:
        # Simulate the probe launch 
        # It's cached, so really this is just retreiving the results from the last
        # succesful launch
        in_area, new_max_height = launch_single_probe(target_range, vx, vy)

        # Check arc height vs current max arc height 
        # but only if the last launch landed in the target zone
        if in_area:
            max_height = max(max_height, new_max_height)
            valid_initial_velocities.add((vx, vy))

        # Always increase vy
        if inc_vy:
            vy += 1
        else:
            vy -= 1

        calculations += 1

    return valid_initial_velocities

def main(infile):
    t: TargetRange = process(infile)
    vx = math.ceil(0.5 * (math.sqrt(8 * t.x.min + 1) - 1))
    vy = 0

    valid_init_velocities = set()
    for _ in range(t.x.min, t.x.max + 10000):
        valid_init_velocities.update(launch_probes(vx, vy, inc_vy=True, target_range=t))
        valid_init_velocities.update(launch_probes(vx, vy, inc_vy=False, target_range=t))
        vx += 1

    return len(valid_init_velocities)
    
if __name__ == "__main__":
    year, day = 2021, 17
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("ex0.txt", ans=112)

    # Run question 
    aoc.test("puzzle_input.txt", ans=None, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
