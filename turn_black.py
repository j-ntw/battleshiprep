def turn_black(draw_ls):
    #given a list of Point objects, show the board

    for square_point in draw_ls:
        chosen_square = str(square_point.x + square_point.y)
         #make a dictionary: key = input letter, value = what it would mean as an x-coordinate
         letter_to_xcoord_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'J': 8, 'K': 9}
         #convert the letter into an x-coordinate number
         chosen_xcoord = letter_to_xcoord_dict[chosen_square[0]]
         square_tup = (chosen_xcoord, int(chosen_square[1]))
         print(square_tup)
         # create a black rectangle patch at (coord.x, coord.y)
         rect = patches.Rectangle( square_tup, 1, 1, angle = 0.0, facecolor = 'k')
         # add the patch to the axes
         ax.add_patch(rect)