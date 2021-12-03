#!/usr/bin/python3


def calc_fuel(mass):
    fuel = (mass // 3) - 2

    if fuel <= 0:
        return 0
    else:
        return fuel + calc_fuel(fuel)


total = 0
for mass in open("input.txt"):
    total += calc_fuel(int(mass))

print(total)
