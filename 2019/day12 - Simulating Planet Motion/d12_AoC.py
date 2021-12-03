from time import sleep
import os

data = open("d12_test_input.txt").readlines()
data = open("d12_input.txt").readlines()

# For each time step:

#   For each moon:
#
#       1. Update the velocity of the moon by applying gravity

#           To apply gravity:
#               * Big ass paragraph
#
#      2. Update the position of the moon by applying velocity
#


class Moon:
    def __init__(self, x, y, z, name):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

        self.dx = 0
        self.dy = 0
        self.dz = 0

    # def __str__(self):
    #    return f"< {self.name}, pos x:{self.x}, y:{self.y}, z:{self.z}, | vel x:{self.dx}, y:{self.dy}, z:{self.dz} >"

    def __str__(self):
        return f"{self.name}{self.x}{self.y}{self.z}{self.dx}{self.dy}{self.dz}"


# Get the data into objects:
moons = {}
for line, name in zip(data, "abcd"):
    line = line.lstrip("<").rstrip(">\n")
    line = [s.lstrip(" ") for s in line.split(",")]
    x, y, z = line
    x, y, z = int(x[2:]), int(y[2:]), int(z[2:])
    moons[name] = Moon(x, y, z, name)


def print_moons(moons):
    for _, moon in moons.items():
        print(moon)


# Part 1:
if False:
    print("**************************************")
    print("Initial setup:")
    print_moons(moons)
    for i in range(1000):
        # Update velocity by applying gravity:
        print("-" * 50)
        applied = {}
        for a, m1 in moons.items():
            for b, m2 in moons.items():
                if b == a or a + b in applied or b + a in applied:
                    continue
                # print(f" pair: {a} & {b}")

                if m1.x < m2.x:
                    m1.dx += 1
                    m2.dx -= 1
                if m1.x > m2.x:
                    m1.dx -= 1
                    m2.dx += 1

                if m1.y < m2.y:
                    m1.dy += 1
                    m2.dy -= 1
                if m1.y > m2.y:
                    m1.dy -= 1
                    m2.dy += 1

                if m1.z < m2.z:
                    m1.dz += 1
                    m2.dz -= 1
                if m1.z > m2.z:
                    m1.dz -= 1
                    m2.dz += 1

                applied[a + b] = 1
                applied[b + a] = 1

        # Update position by applying velocity:
        for moon in moons.values():
            moon.x += moon.dx
            moon.y += moon.dy
            moon.z += moon.dz

        print(f"After {i} steps:")
        print_moons(moons)

    def sum_abs(*args):
        sum = 0
        for arg in args:
            sum += abs(arg)
        return sum

    system_total_energy = 0
    for name, m in moons.items():
        moon_potential = sum_abs(m.x, m.y, m.z)
        moon_kinetic = sum_abs(m.dx, m.dy, m.dz)

        # print(name, moon_potential, moon_kinetic)

        system_total_energy += moon_potential * moon_kinetic

    print("\nTotal energy in system:", system_total_energy)
    # 10028

i = 0
os.system("cls")
os.system("cls")
applied = set()

pairs = []

for a, m1 in moons.items():
    for b, m2 in moons.items():
        if b == a or a + b in applied or b + a in applied:
            continue
        pairs.append((m1, m2))
        applied.add(a + b)
        applied.add(b + a)

# for a,b in pairs: print(a,b)

prev_states = [set()]
set_pointer = 0


def check(string):
    for _set in prev_states:
        if string in _set:
            return True
    return False


def make_new_set():
    prev_states.append(set())


while True:
    if i % 100000 == 0:
        print(f"\u001b[{1};{0}H", end="")
        print(i)
    # Update velocity by applying gravity:
    for m1, m2 in pairs:
        if m1.x < m2.x:
            m1.dx += 1
            m2.dx -= 1
        elif m1.x > m2.x:
            m1.dx -= 1
            m2.dx += 1

        if m1.y < m2.y:
            m1.dy += 1
            m2.dy -= 1
        elif m1.y > m2.y:
            m1.dy -= 1
            m2.dy += 1

        if m1.z < m2.z:
            m1.dz += 1
            m2.dz -= 1
        elif m1.z > m2.z:
            m1.dz -= 1
            m2.dz += 1

    # Update position by applying velocity:
    for moon in moons.values():
        moon.x += moon.dx
        moon.y += moon.dy
        moon.z += moon.dz

    # Generate string of current state:
    cur_state = ""
    for moon in moons.values():
        cur_state += str(moon)

    if i > 1000000:
        if check(cur_state):
            print("Steps to prev state:", i)
            break

    if i % 500000 == 0:
        make_new_set()
        set_pointer += 1

    prev_states[set_pointer].add(cur_state)

    i += 1
