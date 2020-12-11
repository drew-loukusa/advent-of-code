from aocd.models import Puzzle
from collections import defaultdict

def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode='w+') as f:
        data = puzzle.input_data
        f.write(data)

Year=2020
Day=10

# puzzle = Puzzle(year=Year, day=Day)
# save_input_to_file(puzzle, day=Day)

infile, exresult = "day10ex1.txt", (7,5)
infile, exresult = "day10ex2.txt", (22,10) #(count of 1 jolts, count of 3 jolts)
infile = "day10.txt"            
lines = [int(line.rstrip()) for line in open(infile)]
lines.sort()

# Part 1
if False:
    used_chargers = {0}
    cur_charger = 0

    one_jolts = 0
    three_jolts = 0 

    print(*lines,sep='\n')

    for i in range(len(lines)):
        charger = lines[i]
        if charger <= cur_charger + 1:
            cur_charger = charger
            one_jolts += 1

        elif charger <= cur_charger + 3:
            cur_charger = charger 
            three_jolts += 1

    print(one_jolts, three_jolts+1)
    print(one_jolts * (three_jolts+1))
    print(sum(lines))
    #puzzle.answer_a = result

# Part 2
class Node:
    def __init__(self, value):
        self.value = value 
        self.inc = [] # incoming edges
        self.out = [] # outgoing edges

    def __str__(self):
        return "(" + str(self.value) + ")"

class Edge:
    def __init__(self, source, dest, weight):
        self.source = source
        self.dest = dest
        self.weight = weight
    
    def __radd__(self, other):
        return other + self.weight

    def __str__(self):
        return str(self.source) + f" -{self.weight}-> " + str(self.dest)

if True:
    # THIS ASSUMES A SORTED LIST
    # For each charger in bag 
    # Get Node for charger (first node will be the outlet)
    # 1. Calculate all possible dest nodes (chargers in range)
    # 2. For each possible dest node 
        # a. If not in Nodes dict, create a new node for charger, give charger value as value
        # b. Create edge, give weight which is equal to sum of current nodes incoming edge weights 
        # C. Put edge in cur nodes outgoing list, and in dest nodes incoming list 

    Nodes = {} # charger-value -> Node 
    bag = lines 
    bag.insert(0,0)

    # Create a node for the "charging outlet" with an incoming edge with weight 1, (to signify starting with 1 unique path)
    node = Node(bag[0])
    node.inc.append(Edge(None, node, 1))
    Nodes[bag[0]] = node 

    for charger, i in zip(bag, range(len(bag))):
        source = Nodes[charger]

        # Find all chargers in range of the current charger 
        # Only look at chargers that are past the current one 
        for dest_charger in bag[i+1:]:
            if dest_charger > charger + 3: break 
            if dest_charger <= charger + 3:
                # Get the node  node for charger, create it if it does not exist 
                dest = Nodes.setdefault(dest_charger, Node(dest_charger))

                # Calculate what weight to give outgoing nodes of source 
                weight = sum(source.inc)
                edge = Edge(source, dest, weight)

                # Link the two nodes 
                source.out.append(edge)
                dest.inc.append(edge)

    last_charger = bag[-1]
    node = Nodes[last_charger]

    weight = sum(node.inc)
    print(weight)

    