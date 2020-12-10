from aocd.models import Puzzle
from collections import defaultdict as dd
def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode='w+') as f:
        data = puzzle.input_data
        f.write(data)

Year=2020
Day=7

#puzzle = Puzzle(year=Year, day=Day)
#save_input_to_file(puzzle, day=Day)

infile = "day7ex.txt"
infile = "day7ex2.txt"
infile = "day7.txt"
lines = [line.rstrip() for line in open(infile)]

# Part 1
if False:
    bags = dd(dict)
    inverse_map = dd(list)
    for line in lines: 
        toks = line.split(' ')
        bag_color = toks[0] + '-' + toks[1]
        if toks[4] != 'no':
            i = 4
            while i < len(toks):
                num = toks[i]
                color = toks[i+1] + '-' + toks[i+2]
                bags[bag_color][color] = num 
                inverse_map[color].append(bag_color)
                i += 4
            pass
    
    # for k,v in inverse_map.items():
    #     print(k,v)
    
    containing_bags = set()
    queue = ['shiny-gold']
    for bag in queue:
        for parentBag in inverse_map[bag]:
            queue.append(parentBag)
            containing_bags.add(parentBag)
    
    #print(queue)
    result = len(containing_bags)
    print("Bags that could contain shiny-gold:", result)
    #puzzle.answer_a = result

# Part 2
if True:
    bags = dd(dict)
    inverse_map = dd(list)
    for line in lines: 
        toks = line.split(' ')
        bag_color = toks[0] + '-' + toks[1]
        if toks[4] != 'no':
            i = 4
            while i < len(toks):
                num = toks[i]
                color = toks[i+1] + '-' + toks[i+2]
                bags[bag_color][color] = num 
                inverse_map[color].append(bag_color)
                i += 4
            pass
    
    # for k,v in inverse_map.items():
    #     print(k,v)
    
    queue = ['shiny-gold']
    bag_count = 0
    for parent_bag in queue:
        for bag, count in bags[parent_bag].items():
            count = int(count)
            bag_count += count
            for i in range(count):
                queue.append(bag)
    
    print(bag_count)

    #puzzle.answer_b = result
