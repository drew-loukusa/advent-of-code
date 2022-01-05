# https://adventofcode.com/2021/day/18

import sys
import math
from typing import List
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

NODE_ID = 0
class BTreeNode:
    def __init__(self, value=None, left=None, right=None, parent=None):
        self.value = value 
        self.left: BTreeNode = left
        self.right: BTreeNode = right 
        if self.left is not None:
            self.left.parent = self 
        if self.right is not None:
            self.right.parent = self
        self.parent = parent
        self.depth = 0
        self.id = globals()['NODE_ID']

        globals()['NODE_ID'] += 1
    
    def __repr__(self):
        return f"<id: {self.id}, v: {self.value}>"

class TreeParser:
    def __init__(self, line):
        self._line = line 
        self.p = 0 
        self.c = line[0]
    
    def next_char(self):
        self.p += 1
        if self.p < len(self._line):
            self.c = self._line[self.p]
        else:
            self.c = None 

    def parse_tree(self, depth=1):    
        if self.c == '[':
            node = BTreeNode(value=None)
            self.next_char()                
            node.left = self.parse_tree(depth + 1)
            node.left.parent = node
            
            assert self.c == ','
            self.next_char()

            node.right = self.parse_tree(depth + 1)
            node.right.parent = node
            assert self.c == ']'
            self.next_char()
            
            node.depth = depth 
            return node 

        elif self.c >= '0' and self.c <= '9':
            buf = ""
            while self.c >= '0' and self.c <= '9':
                buf += self.c 
                self.next_char()            
            value = int(buf)
            node = BTreeNode(value=value)
            node.depth = depth 
            return node 

def set_depth(node: BTreeNode, depth=1):
    node.depth = depth
    if node.left is not None:
        set_depth(node.left, depth + 1)
    if node.right is not None:
        set_depth(node.right, depth + 1)

def flatten_tree(node: BTreeNode):
    if node.value is not None:
        return node.value

    flat_node = []
    if node.left is not None:
        flat_node.append(flatten_tree(node.left))

    if node.right is not None:
        flat_node.append(flatten_tree(node.right))
    
    return flat_node

def process(infile):
    """Process the input file into a data structure for solve()"""
    trees = []
    for line in open(infile):
        line = line.rstrip() 
        root = TreeParser(line).parse_tree()
        trees.append(root)
    return trees

def get_closest_ancestor(node: BTreeNode, direction):
    """
    Find the closest left or right ancestor.
    Pick left or right by setting direction to 'left' or 'right'
    """

    # Travel up the tree  
    parent: BTreeNode = node.parent 
    stack = [node]

    while ((direction == "left" and node != parent.right)
        or (direction == "right" and node != parent.left)):        
        node = parent 
        parent = node.parent

        # There is no ancestor in the direction selected
        if parent is None:
            return None
        
        stack.append(node)

    # Then travel down till we find a leaf
    while parent.value == None:
        if direction == "left":
            if len(stack) == 0 or parent.right != stack[-1]: 
                parent = parent.right 
            else:
                parent = parent.left 

        elif direction == "right":
            if len(stack) == 0 or parent.left != stack[-1]:
                parent = parent.left 
            else:
                parent = parent.right 
        
    return parent

def explode(node: BTreeNode):
    """
    Explode the node.
    """
    cla = get_closest_ancestor(node, "left")
    cra = get_closest_ancestor(node, "right")
    
    # Give value of children to ancestors
    if cla is not None:
        cla.value += node.left.value 
    if cra is not None:
        cra.value += node.right.value 

    # delete children, give cur node value of zero 
    node.right = None 
    node.left = None 
    node.value = 0

def split(node: BTreeNode):
    val = node.value / 2 
    node.left = BTreeNode(value=math.floor(val))
    node.right = BTreeNode(value=math.ceil(val))
    node.left.depth = node.depth + 1
    node.right.depth = node.depth + 1
    node.left.parent = node 
    node.right.parent = node 
    node.value = None 

def calculate_magnitude(node: BTreeNode):
    if node.value is not None:
        return node.value
    
    left, right = 0,0
    if node.left is not None:
        left = 3 * calculate_magnitude(node.left)
    
    if node.right is not None:
        right = 2 * calculate_magnitude(node.right)

    return left + right

def find_explode_node(node: BTreeNode):
    if (node.depth > 4 and node.left is not None and node.right is not None):
        if node.left.value is not None and node.right.value is not None:
            return node 

    left, right = None, None
    if node.left is not None:
        left = find_explode_node(node.left)
    if node.right is not None:
        right = find_explode_node(node.right)
    
    if left is not None:
        return left 
    return right
    
    #return to_explode

def find_split_node(node: BTreeNode):
    if node.value is not None and node.value >= 10:
        return node 
    left, right = None, None
    if node.left is not None:
        left = find_split_node(node.left)
    if node.right is not None:
        right = find_split_node(node.right)
    
    if left is not None:
        return left 
    return right

def reduce(node: BTreeNode):
    exp_node, split_node = 1,1
    while exp_node != None or split_node != None:
        exp_node = find_explode_node(node)
        if exp_node != None:
            explode(exp_node)
        split_node = find_split_node(node)
        if split_node != None and exp_node is None:
            split(split_node)
    return

def solve(trees: List[BTreeNode]):    
    root = trees[0]
    
    for tree in trees[1:]:
        left = root 
        root = BTreeNode()

        root.left = left
        root.left.parent = root

        root.right = tree 
        root.right.parent = root

        # After creating a new root, we have adjust the depth labels on each node
        set_depth(root)
        # After addition, explode and split as needed 
        reduce(root)

    return calculate_magnitude(root)

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 18
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("ex0.txt", ans=4140)
    aoc.test("ex1.txt", ans=3488)
    # aoc.test("ex2.txt", ans=None)
    # aoc.test("ex3.txt", ans=None)
    aoc.test("ex4.txt", ans=791)
    aoc.test("ex5.txt", ans=1137)

    # Run question 
    aoc.test("puzzle_input.txt", ans=4207, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
