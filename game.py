import argparse

import numpy as np
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation
from numpy.random.mtrand import randint

# constants that define whether the cell is ON or OFF
ON = 255
OFF = 0

# Updates the simulation state
def updateSim(frame_num, image, grid, map_size):
    
    # copy the grid to update simulation state
    updated_grid = grid.copy()
    for i in range(map_size):
        for j in range(map_size):
            # compute the sum of all 8 neighbors of current cell
            # the number of "ON" cells == sum / 255 (since OFF = 0)
            neighbors_sum = int(grid[i, (j + 1) % map_size] + grid[i, (j - 1) % map_size] +
                            grid[(i + 1) % map_size, (j + 1) % map_size] + 
                            grid[(i + 1) % map_size, (j - 1) % map_size] +
                            grid[(i - 1) % map_size, (j + 1) % map_size] + 
                            grid[(i - 1) % map_size, (j - 1) % map_size] + 
                            grid[(i - 1) % map_size, j] + 
                            grid[(i + 1) % map_size, j])
            num_ON = neighbors_sum / ON

            # change cell state based on the rules of the game
            if grid[i, j] == ON:
                if num_ON > 3 or num_ON < 2:
                    updated_grid[i, j] = OFF
            else:
                if num_ON == 3:
                    updated_grid[i, j] = ON
    
    # update the grid with new simulation data
    image.set_data(updated_grid)
    grid[:] = updated_grid[:]
    return image


# Randomly generate the grid
def generateRandomGrid(size):
    return np.random.choice([ON, OFF], size ** 2, p=[0.20, 0.80]).reshape((size, size))


def main():
    # parse and add required arguments
    parser = argparse.ArgumentParser(description="Conway's Game of Life Simulator")
    parser.add_argument("--map-size", dest="map_size", required=False, help="The dimensions of the map in grids (min. 10)")
    parser.add_argument("--interval", dest="interval", required=False, help="The animation delay interval (in milliseconds)")
    args = parser.parse_args()
    
    map_size = 25 # default grid dimensions is 25 x 25
    if args.map_size:
        if int(args.map_size) >= 10:
            map_size = int(args.map_size)
    
    interval = 250 # default animation interval delay set to 250 ms
    if args.interval:
        if int(args.interval) >= 1:
            interval = int(args.interval)

    
    # randomly generate the initial cell combination
    grid = generateRandomGrid(map_size)

    # set up the animation
    fig, ax = plot.subplots()
    image = ax.imshow(grid, interpolation="nearest")
    animation = FuncAnimation(fig, func=updateSim, fargs=(image, grid, map_size), interval=interval)
    plot.show()

if __name__ == "__main__":
    main()