# https://adventofcode.com/2021/day/12

from os import path
import sys
from collections import defaultdict as dd
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
    def __init__(self, graph) -> None:
        self.graph = graph
        self.paths = set()
    
    def dfs_with_restriction(self, node, small_nodes_visited, path_stack):
        
        

        if node == "end":
            path_to_str = ''.join(["start"] + path_stack)
            if path_to_str not in self.paths:
                self.paths.add(path_to_str)
                #print(["start"] + path_stack)
            return 

        for neighbor in self.graph[node]:
            neighbor: str
            if neighbor != "end" and neighbor.islower():
                # if neighbor not in small_nodes_visited:
                if neighbor not in path_stack:
                    # new_set = set(small_nodes_visited)
                    # new_set.add(neighbor)
                    self.dfs_with_restriction(neighbor, small_nodes_visited, list(path_stack) + [neighbor])
                else:
                    continue 
            self.dfs_with_restriction(neighbor, small_nodes_visited, list(path_stack) + [neighbor])
        return

def solve(graph):
    gw = GraphWalker(graph=graph)
    smv = set()
    gw.dfs_with_restriction(node="start", small_nodes_visited=smv, path_stack=[])
    return len(gw.paths)
    
def main(infile):
    return solve(process(infile))

if __name__ == "__main__":
    year, day = 2021, 12
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day12ex.txt", ans=10)
    aoc.test("day12ex1.txt", ans=19)

    # Run question 
    aoc.test("day12.txt", ans=4707, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer