# f = open("d3_test_input.txt")
f = open("d3_input.txt")
wire1 = [(n[0], int(n[1:])) for n in f.readline().split(",")]
wire2 = [(n[0], int(n[1:])) for n in f.readline().split(",")]
f.close()

if wire1 == wire2:
    print("Oop")

import time

# print(wire1, wire2)


def calc_points(wire):
    #       x,y
    pos = [0, 0]
    points = set()
    for der, dist in wire:
        if der == "R":
            for i in range(dist):
                points.add((pos[0] + i, pos[1]))
            pos[0] += dist
        if der == "L":
            for i in range(dist):
                points.add((pos[0] - i, pos[1]))
            pos[0] -= dist
        if der == "U":
            for i in range(dist):
                points.add((pos[0], pos[1] + i))
            pos[1] += dist
        if der == "D":
            for i in range(dist):
                points.add((pos[0], pos[1] - i))
            pos[1] -= dist

        # print(pos)
        # time.sleep(0.2)

    return points


p1 = calc_points(wire1)
# print("---------------")
p2 = calc_points(wire2)

inters = p1.intersection(p2)
# print(inters)


least_dist = -1
for point in inters:
    # print(point)
    dist = abs(point[0]) + abs(point[1])
    if least_dist == -1 and dist != 0:
        least_dist = dist
    if dist < least_dist and dist != 0:
        least_dist = dist
        # time.sleep(0.5)
        # print(least_dist)

print(least_dist)
