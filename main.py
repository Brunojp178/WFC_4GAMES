import numpy as np
from tile import Tile
from collections import namedtuple
import os

# TODO wave function collapse
# TODO make a matrix to represent the image, fill the image with possible values and short it with the neightboor values

# We can have 2 aproaches, start with all number interpretation and change it to the images later or learn how to do it
# from the start with images.
# For the sake of my mind we'll use nambers as image names.
def verifica():
    if -1 in potential:
        return True
    else:
        return False

def load_images(dir_path):
    """
    Load the images using a set of rules in the "rule.txt" file
    @dir_path the path to the directory containing the images
    and the rule.txt file

    """
    dir_path = dir_path.replace("\\", "/")

    # Arquivo de regras
    rules_file = open(dir_path + "/rules.txt", 'r')

    tiles = []

    # for each line in the rule file load a image based on the rule file and save it to the tiles array
    for line in rules_file:
        info = line.split(";")
        name = info[0]
        # Neightboors now will be the name of the image file.
        neightboors = info[1].replace("[", "").replace("]", "").replace("\n", "").split(",")
        tile = Tile(name, neightboors)
        tiles.append(tile)
    
    return tiles

def empty_neightboor(tile_pos:(int, int)):
    x, y = tile_pos
    empty = [None, None, None, None] # Array of 4 positions filled with none

    if not verifica():
        return empty

    if potential[x+1][y] == -1:
        empty[0] = ((x + 1, y))
    if potential[x][y - 1] == -1:
        empty[1] = ((x, y - 1))
    if potential[x - 1][y] == -1:
        empty[2] = ((x - 1, y))
    if potential[x][y + 1] == -1:
        empty[3] = ((x, y + 1))

    return empty

def random_neightboor(tile_pos:(int, int)):
    """
    Return the random choice of a position around a tile
    """
    x, y = tile_pos
    height, width = potential.shape
    # Possible values of x
    target_x = [x + 1, x - 1]
    target_y = [y + 1, y - 1]

    # if the father tile is on a border, remove the out of range index of the possible values for target
    if (x == 0):
        target_x[0] = x + 2
    elif(x == width):
        target_x[1] = x - 2

    if (y == 0):
        target_y[0] = y + 2
    elif(y == height):
        target_y[1] = y - 2

    final_x = np.random.choice(target_x)
    final_y = np.random.choice(target_y)

    return (final_x, final_y)

def propagate(tile:Tile, tile_pos:(int, int)):
    # TODO When propagating, check if can fill any of the neightboors of @param tile, if it can
    # got to that position but not fill it, check the sides of this empty position and make a array of possible values of this cell
    # if the cell can be, for ex. [0, 1] always choose the value diferent from 0, since 0 will have lower "weight"
    # if the positions can be multiple numbers, ex. [1, 3, 0] choose some random one diferent from 0
    # only put 0 if its the only choice.

    if not verifica():
        return 0

    possible_neightboors = empty_neightboor(tile_pos)
    # if neightboors are already filled, get a random one and propagate from it
    if len(possible_neightboors) == 0:
        # Positions of a random one
        new_posX, new_posY = random_neightboor(tile_pos)
        new_tile_name = potential[new_posX][new_posY]   # The name of this random one
        
        for tile in tiles:  # Search for the list that refer to the rules file for the tile with this name
            if tile.name == new_tile_name:
                new_tile = tile     # Set the new_tile to propagate from
        
        propagate(new_tile, (new_posX, new_posY))
    
    else:
        # Take one of the possible neightboors and fill
        for index, value in enumerate(possible_neightboors):
            if value != None:
                # checkar no array de tiles qual os possiveis valores para um determinado lado
                pass




def main():
    image = np.zeros((10, 10))

    global tiles
    tiles = load_images("D:\Workspace\Python\IA para jogos\WFC_4GAMES\Images")

    # Fill a matrix with -1 that means any image can take this place
    global potential
    potential = np.full((10, 9), -1)

    print(potential, "\n\n")

    # TODO select a random point in the matrix
    # Limiting the index of random choice
    height, width = potential.shape

    x = np.random.randint(0, width)
    y = np.random.randint(0, height)
    index = np.random.randint(0, len(tiles))
    print(tiles[index].name)    

    potential[x][y] = tiles[index].name
    print(potential)
    # TODO remember potential is a number (potential[x][y] doesn't return a tile)
    random_neightboor(tiles[index], (x, y))

    # TODO make a dict of all neightboors
    # TODO Based on this random value fill the matrix with the neightboors

if __name__ == "__main__":
    main() 