from math import gcd, pi, atan2

def get_data(path): 
    asteroids = []
    ast_map = {}

    max_y, max_x = 0,0
    for y,line in enumerate(open(path)):
        if max_y == 0 or y > max_y: max_y = y
        for x, c in enumerate(line.rstrip('\n')):
            if max_x == 0 or x > max_x: max_x = x
            if c == '#':
                asteroids.append({'x':x,'y':y})
                ast_map[str(x)+','+str(y)] = {'x':x,'y':y}
            else:
                ast_map[str(x)+','+str(y)] = 0


    return asteroids, max_x, max_y, ast_map 

#+----------------------------------------------------------------------------+
#|                                  Tests                                     |
#+----------------------------------------------------------------------------+
if False:
    data = get_data("d10_p1_test1.txt")
    data = get_data("d10_p1_test2.txt")
    pass

def reduce_ratio(x,y):
    a = gcd(x,y)
    if a: return int(x/a), int(y/a)
    else: return int(x),int(y)

path = r"C:\Users\Drew\Desktop\Code Projects\advent_of_code_2019\day10"

def part_1(path):
    big_space_rocks, max_x, max_y, ast_map = get_data(path)
    #big_space_rocks, max_x, max_y, ast_map = get_data(path+"\\d10_p1_test1.txt")

    best_rock = None    
    most_rocks_visible = 0
    best_rock_visible_asteroids = None
    for dest_rock in big_space_rocks:        
        visible_asteroids = []
        # For each asteroid in the map: 
        # 1. Calculate the slope value to the destination asteroid
        # 2. Reduce it to the smallest ratio possible
        # 3. Make jumps using that ratio until you encounter an asteroid, or the destination asteroid
        #    If it's the dest asteroid, increase the visible asteroid count for dest by 1
        # 4. Move to the next asteroid in the map (left to right, top to bottom)

        rocks_visible = 0
        for rock in big_space_rocks:
            dest_x = dest_rock['x']
            dest_y = dest_rock['y']

            x,y = rock['x'], rock['y']

            if dest_x == 11 and dest_y == 13 and x == 4 and y == 0:
                foo = 0

            # Calculate the slope to the dest_rock:
            dx = dest_x - rock['x']
            dy = dest_y - rock['y']

            dx,dy = reduce_ratio(dx,dy)

            while x != dest_x or y != dest_y:
                x += dx
                y += dy

                if x < 0 or x > max_x: break
                if y < 0 or y > max_y: break

                # Clear line of sight to the dest asteroid!
                if x == dest_x and y == dest_y:
                    rocks_visible += 1
                    visible_asteroids.append(rock)
                    break
                
                # Found an asteriod in the way:
                if ast_map[str(x)+','+str(y)]: 
                    break


        if rocks_visible > most_rocks_visible: 
            most_rocks_visible = rocks_visible
            best_rock_visible_asteroids = visible_asteroids
            best_rock = dest_rock
    
    print(best_rock, most_rocks_visible)
    return best_rock, best_rock_visible_asteroids, ast_map

def angle_trunc(a):
    while a < 0.0:
        a += pi * 2
    return a

def getAngleBetweenPoints(x_orig, y_orig, x_landmark, y_landmark):
    deltaY = y_landmark - y_orig
    deltaX = x_landmark - x_orig
    #return angle_trunc(atan2(deltaY, deltaX) * 180 / pi )
    return atan2(deltaY, deltaX) * 180 / pi 

def sort_rocks(best_rock, mx, my, visible_asteroids):
    def calc_angle(best_rock, rock):       

        bx, by = best_rock['x'], best_rock['y']
        x,  y  = rock['x'], rock['y']

        return getAngleBetweenPoints(bx, by, x, y)

    for rock in visible_asteroids: 
        angle = calc_angle(best_rock, rock)
        rock['angle'] = angle

    s1 = sorted(visible_asteroids, key=lambda theta: theta['angle'])
    i = 0
    while s1[i]['angle'] != -90.0: i += 1
    return s1[i:] + s1[:i]

rep = lambda x,y: str(x) + ',' + str(y)

import time
def part_2(path, best_rock, visible_asteroids):
    all_the_rocks, max_x, max_y, ast_map = get_data(path)

    print("Total asteroids:",len(all_the_rocks)); 

    visible_asteroids = sort_rocks(best_rock, max_x, max_y, visible_asteroids)

    print("Initially Visible asteroids:", len(visible_asteroids))
    #time.sleep(2)

    #for ast in visible_asteroids: print(ast) 

    bx, by = best_rock['x'], best_rock['y']
    i = 0    
    loop = True
    vaporized_count = 0
    vaporized_order = []
    while vaporized_count < len(all_the_rocks):       
        loop = False
        if i == len(visible_asteroids): i = 0
        ast = visible_asteroids[i]
        if ast != None:
            loop = True
            x,y = ast['x'], ast['y']
            dx = x - bx 
            dy = y - by 
            
            dx,dy = reduce_ratio(dx,dy)

            x += dx 
            y += dy

            while (x >= 0 and x <= max_x) and (y >= 0 and y <= max_y):
                if rep(x,y) in ast_map and ast_map[rep(x,y)] != 0:
                    visible_asteroids[i] = ast_map[rep(x,y)]
                    break
                x += dx 
                y += dy
            
            if (x < 0 or x > max_x) or (y < 0 or y > max_y):
                visible_asteroids[i] = None

            vaporized_count += 1
            vaporized_order.append((vaporized_count, ast))
            print("Count:", vaporized_count, '-', ast)
            time.sleep(0.01)            
        i += 1

        if visible_asteroids.count(None) == len(visible_asteroids): break

    return vaporized_count, vaporized_order


if __name__ == "__main__": 
    path = path+"\\d10_input.txt"
    #path = path+"\\d10_p1_test1.txt"

    best_rock, visible_asteroids, ast_map = part_1(path)
    #for rock in visible_asteroids: print(rock)
    vap_count, vap_order = part_2(path, best_rock, visible_asteroids)

    for tup in vap_order:
        if tup[0] in [1,2,3,10,50,100,199,200,201,299]:        
            print(tup)
    
    vap_order_dict = {}
    for tup in vap_order:
        count, r = tup[0], tup[1]
        vap_order_dict[rep(r['x'],r['y'])] = r

    # Missing rocks:
    print("Missing rocks")
    for name, rock in ast_map.items():
        if name not in vap_order_dict and ast_map[name] != 0: 
            print(ast_map[name])