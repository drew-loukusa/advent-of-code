pos_cor = 0
for i in range(171309, 643603 + 1):

    rep = str(i)

    last = -1
    found_adj = False
    adj_count = 1

    perm_found = False

    for c in rep:

        # Must always increase:
        if int(c) >= last:

            # If same as last digit:
            if int(c) == last:
                # We have TWO adjacent digits that are the same!
                if adj_count < 2:
                    found_adj = True

                # Oops, we have more than two adjactent digits that are the same >:(
                else:
                    found_adj = False

                # Tally how many adjacent digits are the same:
                adj_count += 1

            # If cur digit is bigger than the last one:
            else:
                # If the previous chain was the correct size, Remember that:
                if adj_count == 2:
                    perm_found = True

                # Reset the adjacent count:
                adj_count = 1
            last = int(c)

        # Not increasing, INVALID NUMBER
        else:
            break
    else:
        if found_adj or perm_found:
            pos_cor += 1

print(pos_cor)
