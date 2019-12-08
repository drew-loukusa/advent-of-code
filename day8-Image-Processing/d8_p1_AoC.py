data = open("d8_input.txt").readline().rstrip('\n')

width = 25
height = 6
col_proc = 0
row_proc = 0
k = 0

layers = {}
pixels = []

fewest = None
while k < len(data):
    zeros = 0
    layer = ''

    # Examine each layer:
    for _ in range(height):
        row = ''
        for j in range(width):
            c =  data[k+j]
            if int(c) == 0: zeros += 1
            row += c 
        layer += row
        k += width
    # -- End of Layer -- # 

    if fewest is None or zeros < fewest:  
        fewest = zeros
    layers[zeros] = layer

print(fewest)
print(layers[fewest])

ones, twos = 0,0
for c in layers[fewest]:
    if c == '1': ones += 1
    if c == '2': twos += 1

print(ones*twos)