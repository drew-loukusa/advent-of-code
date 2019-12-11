#!/usr/bin/python3

total = 0
for mass in open("input.txt"):
    total += (int(mass) // 3) - 2

print(total)
