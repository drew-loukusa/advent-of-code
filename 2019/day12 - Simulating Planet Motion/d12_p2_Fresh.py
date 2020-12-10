from collections import defaultdict
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

print("********************")

cur_velocity = {} # i -> veloctity 
# (Px, Vx), (Py, Vy), (Pz, Vz)

states_x = {}
states_y = {}
states_z = {}

# Add initial states:
x_state, y_state, z_state = "", "", ""
for moon in moons.values():
    moon[1] += moon[4]
    moon[2] += moon[5]
    moon[3] += moon[6] 

    x_state += str(moon[1]) + ',' + str(moon[4]) + ','
    y_state += str(moon[2]) + ',' + str(moon[5]) + ','
    z_state += str(moon[3]) + ',' + str(moon[6]) + ','

k = 1
period_x, period_y, period_z = 0,0,0
while True:      
    #if i > 0 and i % 100000 == 0:
    #    print(f"\u001b[{1};{0}H",end='')
    #    print(i)
    # Update velocity by applying gravity:         
    for m1, m2 in pairs:
        if   m1[1] < m2[1]: m1[4] += 1; m2[4] -= 1
        elif m1[1] > m2[1]: m1[4] -= 1; m2[4] += 1

        if   m1[2] < m2[2]: m1[5] += 1; m2[5] -= 1
        elif m1[2] > m2[2]: m1[5] -= 1; m2[5] += 1

        if   m1[3] < m2[3]: m1[6] += 1; m2[6] -= 1
        elif m1[3] > m2[3]: m1[6] -= 1; m2[6] += 1

    # Update position by applying velocity:
    x_state, y_state, z_state = "", "", ""
    for moon in moons.values():
        moon[1] += moon[4]
        moon[2] += moon[5]
        moon[3] += moon[6] 

        x_state += str(moon[1]) + ',' + str(moon[4]) + ','
        y_state += str(moon[2]) + ',' + str(moon[5]) + ','
        z_state += str(moon[3]) + ',' + str(moon[6]) + ','
        
    
    if x_state in states_x:         
        diff = i - states_x[x_state]        
        if states_x[x_state] == 0: 
            period_x = diff
            print(f"{k} - X: i {i} prev i {states_x[x_state]} diff: {diff}")
            k += 1
            if k == 10: print("-------------------------")
            if k == 10: k = 1
            sleep(1)
    else:
        states_x[x_state] = i

    if y_state in states_y:         
        diff = i - states_y[y_state]
        if states_y[y_state] == 0: 
            print(f"{k} - Y: i {i} prev i {states_y[y_state]} diff: {diff}")
            k += 1
            if k == 10: print("-------------------------")
            if k == 10: k = 1
            sleep(1)
            period_y = diff 
    else:
        states_y[y_state] = i

    if z_state in states_z:         
        diff = i - states_z[z_state]
        if states_z[z_state] == 0:
            period_z = diff
            print(f"{k} - Z: i {i} prev i {states_z[z_state]} diff: {diff}")
            k += 1
            if k == 10: print("-------------------------")
            if k == 10: k = 1
            sleep(1)
    else:
        states_z[z_state] = i

    if period_x and period_y and period_z: break

    #if i == 2772: break

    # 5033770173190016
    # 314610635824376
    # 4686774924
    i += 1

# Then calculate the LCM of the three periods to get your answer.