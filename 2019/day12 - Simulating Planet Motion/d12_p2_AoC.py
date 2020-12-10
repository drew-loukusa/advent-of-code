from collections import defaultdict
from time import sleep
import os

data = open("d12_input.txt").readlines()
data = open("d12_test_input.txt").readlines()

# For each time step:

#   For each moon:
#       
#       1. Update the velocity of the moon by applying gravity

#           To apply gravity:
#               * Big ass paragraph
# 
#      2. Update the position of the moon by applying velocity 
#             

# Get the data into objects:
moons = {}
for line, name in zip(data, "abcd"):    
    line = line.lstrip('<').rstrip('>\n')
    line = [ s.lstrip(' ') for s in line.split(',')]    
    x,y,z = line 
    x,y,z = int(x[2:]), int(y[2:]), int(z[2:])
                  # 0   1 2 3 4 5 6
    moons[name] = [name,x,y,z,0,0,0]

def print_moons(moons):
    for _, moon in moons.items(): print(moon)

i = 0
os.system('cls')
os.system('cls')
applied = set()

pairs = []

for a, m1 in moons.items():
    for b, m2 in moons.items():
        if b == a or a+b in applied or b+a in applied: 
            continue    
        pairs.append((m1,m2))    
        applied.add(a+b)        
        applied.add(b+a)

#for a,b in pairs: print(a,b)

pxs=set()
pys=set()
pzs=set()
prev_pos_states = set()
prev_vel_states = set()
prev_states = defaultdict(set)

def check(string):
    key = string[:8]
    if string in prev_states[key]: return True
    return False
print("*************")

cur_velocity = {} # i -> veloctity 

while True:      
    if i > 0 and i % 100000 == 0:
        print(f"\u001b[{1};{0}H",end='')
        print(i)
    # Update velocity by applying gravity:         
    for m1, m2 in pairs:
        if   m1[1] < m2[1]: m1[4] += 1; m2[4] -= 1
        elif m1[1] > m2[1]: m1[4] -= 1; m2[4] += 1

        if   m1[2] < m2[2]: m1[5] += 1; m2[5] -= 1
        elif m1[2] > m2[2]: m1[5] -= 1; m2[5] += 1

        if   m1[3] < m2[3]: m1[6] += 1; m2[6] -= 1
        elif m1[3] > m2[3]: m1[6] -= 1; m2[6] += 1

    # Update position by applying velocity:
    for moon in moons.values():
        moon[1] += moon[4]
        moon[2] += moon[5]
        moon[3] += moon[6] 

    # x match: i 80, [0, 0, 0, 0] 
    # y match: i 80, [3, -2, -5, 4]
    # z match: i 80, [2, 4, -4, -2]


    # Generate string of current state:
    cur_state = ""
    cur_pos = ""
    cur_vel = ""
    cx=[]
    cy=[]
    cz=[]
    for moon in moons.values():
        cur_state += str(moon)
        cur_pos += str(moon[:5])
        cur_vel += str(moon[5:])
        cx.append(moon[4])
        cy.append(moon[5])
        cz.append(moon[6])

    # if cur_pos in prev_pos_states: 
    #     print(f"i: {i} POS Match: {cur_state}")

    if check(cur_state): 
        print("Steps to prev state:", i)
        break    

    if cur_vel in prev_vel_states:
        prev_i = cur_velocity[cur_vel]
        diff = i - prev_i
        print(f"i {i}, prev i {prev_i} diff {diff}: {cur_state}")

    # print("*"*40)
    # if str(cx) in pxs: print(f"x match: i {i}, {cx} ")
    # if str(cy) in pys: print(f"y match: i {i}, {cy} ")
    # if str(cz) in pzs: print(f"z match: i {i}, {cz} ")
    # print("*"*40)

    prev_states[cur_state[:8]].add(cur_state)
    prev_pos_states.add(cur_pos)
    prev_vel_states.add(cur_vel)
    cur_velocity[cur_vel] = i

    pxs.add(str(cx))
    pys.add(str(cy))
    pzs.add(str(cz))

    #sleep(0.1)
    

    i += 1

# (Px, Vx), (Py, Vy), (Pz, Vz)