import matplotlib.pyplot as plt

board = plt.figure(figsize=[8,8])
board.patch.set_facecolor((1,1,.8))
ax = board.add_subplot(111)

# draw the grid
for x in range(10):
    ax.plot([x, x], [0,9], 'k')
for y in range(10):
    ax.plot([0, 9], [y,y], 'k')

# scale the axis area to fill the whole figure
ax.set_position([0,0,1,1])

# get rid of axes and everything (the figure background will show through)
ax.set_axis_off()

# scale the plot area conveniently (the board is in 0,0..18,18)
ax.set_xlim(-1,10)
ax.set_ylim(-1,10)
plt.show()