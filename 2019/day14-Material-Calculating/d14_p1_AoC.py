import os
from time import sleep
from collections import defaultdict

# get_data = lambda path: [ int(n.rstrip()) for n in open(path).readline().split(',') if len(n) > 0]
get_data = lambda path: [line.rstrip("\n") for line in open(path)]

data = get_data("d14_test_input.txt")
data = get_data("d14_input.txt")

reactions = dict()

# Parse the input data:
for line in data:
    l, r = line.split("=>")
    # print(l, '=>',r)

    l = l.split()
    r = r.split()

    # print(l)
    # print(r)

    output_amount = int(r[0])
    output_name = r[1]

    recipe = {}

    for i in range(0, len(l), 2):
        input_amount = int(l[i])
        input_name = l[i + 1].rstrip(",")
        recipe[input_name] = input_amount

    reactions[output_name] = {"output_amount": output_amount, "recipe": recipe}


def output_mat_store_state(material_store):
    print(f"\u001b[{6};{0}H", end="")
    for name, amount in material_store.items():
        print(f"{name} : {amount}")
    # sleep(0.5)


def calc_needed_ore(mat_name, reactions, ore_count, matr_store):

    if mat_name == "ORE":
        ore_count[0] += 1
        return 1

    output_amount = reactions[mat_name][
        "output_amount"
    ]  # How much output this recipe makes
    recipe = reactions[mat_name]["recipe"]  # Duh...

    # Use recipe to create output:
    for ingr_name, ingr_amount in recipe.items():

        # Each ingredient has it's own recipe. You may need to use an ingredients recipie
        # multiple times to get enough of said ingredient:

        # Store created materials in the material store until we have enough:
        while matr_store[ingr_name] < ingr_amount:
            matr_store[ingr_name] += calc_needed_ore(
                ingr_name, reactions, ore_count, matr_store
            )

        # Use however much is needed:
        matr_store[ingr_name] -= ingr_amount
        matr_store

    return output_amount


# Part 1:
if True:
    matr_store = defaultdict(int)
    total_ore_count = [0]
    calc_needed_ore("FUEL", reactions, total_ore_count, matr_store)
    print(f"Minimum, {total_ore_count[0]} ORE is required to make 1 Fuel")
    output_mat_store_state(matr_store)
