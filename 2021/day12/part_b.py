# https://adventofcode.com/2021/day/12

import sys
from collections import defaultdict as dd, Counter
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    graph = dd(list)
    for line in open(infile):
        line = line.rstrip()
        a, b = line.split('-')
        
        if a == "start":
            graph[a].append(b)
            continue
        if b == "start":
            graph[b].append(a)
            continue 
        if a == "end":
            graph[b].append(a)
            continue
        if b == "end":
            graph[a].append(b)
            continue 

        graph[a].append(b)
        graph[b].append(a)

        
    return graph

class GraphWalker:
    # Use a class because updating a class attr is easier than managing returns 
    # in a recursive function :D
    def __init__(self, graph) -> None:
        self.graph = graph
        self.paths = 0

    def dfs(self, node, graph, snc):      

        # Base case
        if node == "end":
            self.paths += 1
            return

        neighbors = graph[node]
        for neighbor in neighbors:

            # Go through neighbors and check which ones we are allowed to recurse to
            if neighbor.islower() and neighbor != "end":

                # If the neighbor is a small cave, and we haven't visited OR
                # we have visited it yet, but we haven't visited any other small caves twice yet...
                if neighbor in snc[0] or (
                    neighbor in snc[1] and len(snc[2]) == 0
                ):
                    if neighbor in snc[1]:
                        snc[1].remove(neighbor)
                        snc[2].add(neighbor)
                    if neighbor in snc[0]:
                        snc[0].remove(neighbor)
                        snc[1].add(neighbor)
                else:
                    # If the current small cave neighbor cannot be recursed to, then DON'T 
                    # recurse to it
                    continue 
            
            # RECURSE 
            self.dfs(neighbor, graph, snc)

            if neighbor.islower() and neighbor != "end":
                if neighbor in snc[1]:
                    snc[1].remove(neighbor)
                    snc[0].add(neighbor)
                if neighbor in snc[2]:
                    snc[2].remove(neighbor)
                    snc[1].add(neighbor)
        return

def solve(graph):
    lower_case_nodes = [node for node in graph if (node.islower() and node != "start")]
    small_node_tracker = {0:set(lower_case_nodes), 1:set(), 2:set()}
    gw = GraphWalker(graph)
    gw.dfs("start", graph, small_node_tracker)
    return gw.paths

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 12
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day12ex.txt", ans=36)
    aoc.test("day12ex1.txt", ans=103)
    aoc.test("day12ex2.txt", ans=3509)
    

    # # Run question 
    aoc.test("day12.txt", ans=130493, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer