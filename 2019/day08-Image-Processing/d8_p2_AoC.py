data = open("d8_input.txt").readline().rstrip("\n")

width = 25
height = 6
k = 0
image = []


# Initialize pixels:
# -----------------------------------------------------------------------------
# Give each pixel position (x,y) its own list which will hold ALL pixels values
# from all layers for a given pixel positon:
#
#   Every pixel value in position (5,4) will be contained in a single list,
#   with the first layers value being at position 0, and the last layers
#   value being at position -1
#
for _ in range(height):
    row = []
    for j in range(width):
        c = data[k + j]
        row.append([int(c)])
    image.append(row)
    k += width
# -- End of Layer -- #

# Go through the rest of the layers, putting pixel values into the appropriate lists:
while k < len(data):
    # Examine each layer:
    for i in range(height):
        for j in range(width):
            c = data[k + j]
            image[i][j].append(int(c))
        k += width

for row in image:
    for pixel_list in row:
        for val in pixel_list:
            if val == 2:
                continue  # Transparent, do nothing
            if val == 0:
                print(".", end="")
                break
            if val == 1:
                print("▮", end="")
                break

    print()  # Done printing row, CARRAGE RETURN
