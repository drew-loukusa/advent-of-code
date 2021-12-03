# +---------------------------------------------------------------------------+
# |                           Get the input:                                  |
# +---------------------------------------------------------------------------+
# f = open("d3_test_input.txt")

f = open("d3_input.txt")
wire1 = [(n[0], int(n[1:])) for n in f.readline().split(",")]
wire2 = [(n[0], int(n[1:])) for n in f.readline().split(",")]
f.close()

# +---------------------------------------------------------------------------+
# |                           Methods:                                        |
# +---------------------------------------------------------------------------+
def gen_points_and_steps(points, steps, dist, sum_dist, pos, x_or_y, p_or_m):
    """Generate each point between 'pos' and 'pos' + 'dist', where
    dist is added to x or y in pos based on what 'x_or_y' is set to.

    * points - The complete set of points for the wire
    * steps  - The complete dict of str(point) -> distance_traveled_to_said_point
    * sum_dist - the sum of the distances traveled thus far
    * pos - A list [x,y] which decribes the current position
    * x_or_y - 'x' or 'y'
    * p_or_m -  '+' or '-'

    Store each point in the set 'points'

    Also put each point into the dict 'steps' with the (x,y) point as a
    string as key and the total distance traveled to said point as the value:

        Ex: {'(50, 6)':102}
    """
    # Select x or y coord to modify:
    k = 0 if x_or_y == "x" else 1

    for i in range(1, dist + 1):
        if p_or_m == "+":
            pos[k] += 1
        elif p_or_m == "-":
            pos[k] -= 1

        points.add((pos[0], pos[1]))
        steps[str((pos[0], pos[1]))] = sum_dist + i

    return sum_dist + dist


def calc_points(wire):
    """Generate every possible point in the path defined by 'wire'
    Returns two items:
    *   points - A set containing every point in the path
    *   steps  - A dict of (point:str) -> (steps_taken_to_reach_point:int)
    """
    pos, points, steps, sum_dist = [0, 0], set(), {}, 0
    dirs = {"R": "x+", "L": "x-", "U": "y+", "D": "y-"}

    for direction, dist in wire:
        sum_dist = gen_points_and_steps(
            points,
            steps,
            dist,
            sum_dist,
            pos,
            x_or_y=dirs[direction][0],
            p_or_m=dirs[direction][1],
        )
    return points, steps


# +---------------------------------------------------------------------------+
# |           Generate set of points, and dict of points->steps:              |
# +---------------------------------------------------------------------------+
p1s, p1d = calc_points(wire1)
p2s, p2d = calc_points(wire2)

# Find all intersections between the two wires:
inters = list(p1s.intersection(p2s))
print("len inters:", len(inters))

# +---------------------------------------------------------------------------+
# |    Iterate through our intersection set, find the smallest step count     |
# +---------------------------------------------------------------------------+
least_steps = p1d[str(inters[0])] + p2d[str(inters[0])]
for point in inters[1:]:
    steps = p1d[str(point)] + p2d[str(point)]
    if steps < least_steps and steps != 0:
        least_steps = steps

# Answer: 43848
print(least_steps)
