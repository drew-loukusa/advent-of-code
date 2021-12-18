# https://adventofcode.com/2021/day/15

import sys
import heapq
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test, abs_path 

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [[int(n) for n in line.rstrip()] for line in open(infile) ] 


def solve(matrix):

    # MAX x and y of the original sized matrix
    MAX_Y, MAX_X = len(matrix) - 1, len(matrix[0]) - 1
   
    # Calculate the "extended" size of the matrix 
    # EXTENDED MAX 
    EMAX_Y = ((MAX_Y + 1) * 5) - 1
    EMAX_X = ((MAX_X + 1) * 5) - 1

    # Rather than actually extending the matrix 5 times in each direction, 
    # write a function that will calculate the cost at a given y,x coord pair based on 
    # the current location. 

    # Knowing that the original matrix is of size M x N, 
    # * Calculate what tile you are in
    # * Get the cost of the equivalent location in the original grid 
    # * Based on tile location, use modulo math to calculate how much to increment the 
    #   the current cost, (remember, it rolls over, 9 is max 1 is min)

    # Then use Dijkstra's algorithm to find the least cost path

    def get_cost(yx_pair):
        y,x = yx_pair

        # What tile would (y,x) be in? There are 5 x 5 (25) total tiles
        tile_y = y // (MAX_Y + 1)
        tile_x = x // (MAX_X + 1)

        # What are the y,x coords of the equivalent position in the original tile?
        oy = y % (MAX_Y + 1)
        ox = x % (MAX_X + 1)

        # Get the cost at that original tile
        original_cost = matrix[oy][ox]

        # Based on where the tile of (y,x) is, calculate the cost
        tcost = (original_cost + tile_y + tile_x)
        if tcost > 9: 
            tcost += 1
        cur_cost = tcost % 10

        return cur_cost

    priority_q = []
    visited = set()
    costs = dict()
    
    cur_node = (0,0)
    heapq.heappush(priority_q, (0, cur_node))

    while (EMAX_Y, EMAX_X) not in visited:
        cur_cost, cur_node = heapq.heappop(priority_q)
        if cur_node in visited:
            continue 
        y,x = cur_node

        neighbors = []
        if y > 0: neighbors.append((y - 1,x))
        if x > 0: neighbors.append((y,x - 1))
        if x < EMAX_X: neighbors.append((y,x + 1))
        if y < EMAX_Y: neighbors.append((y + 1,x))

        for neighbor in neighbors:
            if neighbor not in visited:
                ny, nx = neighbor
                new_cost = cur_cost + get_cost((ny,nx))
                neighbor_cost = costs.get(neighbor)
                if neighbor_cost is None or new_cost < neighbor_cost:
                    costs[neighbor] = new_cost
                heapq.heappush(priority_q, (costs[neighbor], neighbor))

        visited.add(cur_node)

    return costs[(EMAX_Y, EMAX_X)]

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 15
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day15ex.txt", ans=315)

    # Run question 
    aoc.test("day15.txt", ans=3012, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
