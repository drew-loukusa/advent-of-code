import os
import time
from copy import deepcopy
from collections import defaultdict, Counter

start_time = time.time()

#get_data = lambda path: [ int(n.rstrip()) for n in open(path).readline().split(',') if len(n) > 0]
get_data = lambda path: [ line.rstrip('\n') for line in open(path)]

data = get_data("d14_test_input.txt")
data = get_data("d14_input.txt")

reactions = dict()

# Parse the input data:
for line in data:
    l,r = line.split('=>')
    #print(l, '=>',r)

    l = l.split() 
    r = r.split()

    #print(l)
    #print(r)
    
    output_amount = int(r[0])
    output_name = r[1]

    recipe = {}

    for i in range(0,len(l),2):
        input_amount = int(l[i])
        input_name = l[i+1].rstrip(',')
        recipe[input_name] = input_amount

    reactions[output_name] = { 'output_amount':output_amount, 'recipe': recipe }
    
#for name, reaction in reactions.items():
#   print(name, reaction)

class FuelError(Exception): pass

# def calc_needed_ore(mat_name, reactions, ore_count, excess_store):
#     output_amount   = reactions[mat_name]['output_amount'] # How much output this recipe makes
#     recipe          = reactions[mat_name]['recipe']        # Duh...

   
#     # Use recipe to create output:
#     for ingredient_name, ingredient_amount in recipe.items():        
        
#         # Each ingredient has it's own recipe:
#         # You may need to use an ingredients recipie 
#         # multiple times to get enough of said ingredient:
#         amount_made = 0
#         excess_amount = excess_store[ingredient_name]
        
#         while amount_made + excess_amount < ingredient_amount:
#             amount_made += calc_needed_ore(ingredient_name, reactions, ore_count, excess_store) 
        
#         # Store excess for later use:
#         excess_store[ingredient_name] = (amount_made + excess_amount - ingredient_amount)
        
#     return output_amount

def calc_needed_ore(mat_name, reactions, ore_count, matr_store):

    output_amount   = reactions[mat_name]['output_amount'] # How much output this recipe makes
    recipe          = reactions[mat_name]['recipe']        # Duh...

    if len(recipe)== 1 and 'ORE' in recipe: 
        ore_amount = recipe['ORE']
        if ore_count[0] > ore_amount:
            ore_count[0] -= ore_amount
        else:
            raise FuelError(f"Ran out of ORE while trying to make mats")
        return output_amount

    # Use recipe to create output:
    for ingr_name, ingr_amount in recipe.items():        
        
        # Each ingredient has it's own recipe. You may need to use an ingredients recipie 
        # multiple times to get enough of said ingredient:

        # Store created materials in the material store until we have enough:
        while matr_store[ingr_name] < ingr_amount:
            matr_store[ingr_name] += calc_needed_ore(ingr_name, reactions, ore_count, matr_store)            
        
        # Use however much is needed:
        matr_store[ingr_name] -= ingr_amount
        matr_store
        
    return output_amount

# Part 2:
if True:        
    FUEL_produced = 0
    ore_required = 1582325

    excess_store = Counter()
    ore_hold = [1000000000000]
    loop = True

    # Run fuel calc once to put intitial excess materials produced into data structure
    FUEL_produced += calc_needed_ore('FUEL', reactions, ore_hold, excess_store)      

    while ore_required < ore_hold[0]:
        if FUEL_produced % 10 == 0:
            print(f"\u001b[{10};{0}H",end='')
            print(ore_hold[0])
            print("FUEL:", FUEL_produced)
        FUEL_produced += 1
        cpy = deepcopy(excess_store)
        excess_store = excess_store + cpy
        ore_hold[0] -= ore_required

    while loop:        
        if FUEL_produced % 10 == 0:
            print(f"\u001b[{10};{0}H",end='')
            print(ore_hold[0])
            print("FUEL:", FUEL_produced)
        try:
            FUEL_produced += calc_needed_ore('FUEL', reactions, ore_hold, excess_store)         
        except FuelError as e:
           print(e)
           loop = False
    
    print(FUEL_produced)
    
    print("--- %s seconds ---" % (time.time() - start_time))

    #Answer is 2267486 (2,267,486)