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
    if int("-1") in potential:
        return False
    else:
        return True

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
        # neighbours now will be the name of the image file.
        neighbours = info[1].replace("[", "").replace("]", "").replace("\n", "").split(",")
        tile = Tile(name, neighbours)
        tiles.append(tile)
    
    return tiles

def empty_neighbour(tile_pos:(int, int)):
    x, y = tile_pos
    height, width = potential.shape
    height -= 1
    width -= 1

    empty = [None, None, None, None] # Array of 4 positions filled with none   

    if verifica():
        return empty

    if x != 0:
        if potential[x - 1][y] == -1:
            empty[2] = ((x - 1, y))

    if x != width:
        if potential[x+1][y] == -1:
            empty[0] = ((x + 1, y))
    
    if y != 0:
        if potential[x][y - 1] == -1:
            empty[1] = ((x, y - 1))
    
    if y != height:
        if potential[x][y + 1] == -1:
            empty[3] = ((x, y + 1))
    
    print(empty)
    return empty

def random_neighbour(tile_pos:(int, int)):
    """
    Return the x, y coordinate of a random cell around one tile.
    """
    x, y = tile_pos
    height, width = potential.shape
    height -= 1
    width -= 1

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

    # Recursive fucker
    final_x = np.random.choice(target_x)
    final_y = np.random.choice(target_y)

    if final_x == -1:
        final_x += 1

    if final_y == -1:
        final_y += 1

    if final_x == 10:
        final_x -= 1

    if final_y == 10:
        final_y -= 1

    return (final_x, final_y)

def check_around(tile_pos:(int, int)):
    """
    Return a list of possible values of a cell based on the requirements of its neighbours.
    """
    cell_x, cell_y = tile_pos
    height, width = potential.shape
    height -= 1
    width -= 1

    if cell_x == width:
        right = -1
    else:
        right = potential[cell_x + 1][cell_y]

    if cell_y == 0:
        up = -1
    else:
        up = potential[cell_x][cell_y - 1]
    
    if cell_x == 0:
        left = -1
    else:
        left = potential[cell_x - 1][cell_y]

    if cell_y == height:
        down = -1
    else:
        down = potential[cell_x][cell_y + 1]

    right_requirements = None
    up_requirements = None
    left_requirements = None
    down_requirements = None

    # Run throught tiles list and get the requirements of each tile that has the same name as the values around the cell
    for tile in tiles:
        if right != -1:
            if tile.name == str(right):
                right_requirements = int(tile.sides.get("esquerda"))
        
        if up != -1:
            if tile.name == str(up):
                up_requirements = int(tile.sides.get("baixo"))

        if left != -1:
            if tile.name == str(left):
                left_requirements = int(tile.sides.get("direita"))

        if down != -1:
            if tile.name == str(down):
                down_requirements = int(tile.sides.get("cima"))

    requirements = [right_requirements, up_requirements, left_requirements, down_requirements]
    
    if requirements.count(None) == 4:
        requirements[0] = int(np.random.choice(tiles).name)

    return requirements

def propagate(tile:Tile, tile_pos:(int, int)):
    # TODO When propagating, check if can fill any of the neighbours of @param tile, if it can
    # got to that position but not fill it, check the sides of this empty position and make a array of possible values of this cell
    # if the cell can be, for ex. [0, 1] always choose the value diferent from 0, since 0 will have lower "weight"
    # if the positions can be multiple numbers, ex. [1, 3, 0] choose some random one diferent from 0
    # only put 0 if its the only choice.

    if verifica():
        exit()

    # Get all the cells around the tile and see if they are empty
    # if neighbours cells are already filled, get a random one and propagate from it
    possible_neighbours = np.zeros(0, dtype=object)
    possible_neighbours = empty_neighbour(tile_pos)

    if possible_neighbours.count(None) == 4:
        new_posX, new_posY = random_neighbour(tile_pos) # Positions of a random one

        new_tile_name = potential[new_posX][new_posY]   # The name of this random one
        new_tile = None

        # Note: the tiles list is the representation of the images in Tiles class 
        # so we search for the Tile representation of "new_tile_name"
        for tile in tiles:
            if tile.name == str(new_tile_name):
                new_tile = tile
        
        propagate(new_tile, (new_posX, new_posY))
    else:
        # Aux list that hold probabilities to use in np.random.choice(), making the probabilitie of None to be chose equal to 0
        for index, i in enumerate(possible_neighbours):
            if i == None:
                for x in possible_neighbours:
                    if x != None:
                        possible_neighbours[index] = x
                        break
        
        # creating an aux array filled with index based on possible_neighbours
        aux = []
        for i in range(len(possible_neighbours)):
            aux.append(i)
        
        target_coord = possible_neighbours[np.random.choice(aux)]
        target_x, target_y = target_coord
        
        target_requirements = check_around(target_coord)
        
        # TODO CHOOSE ONE OF THE VALUES TO FILL THE CELL
        for index, i in enumerate(target_requirements):
            if i == None:
                for x in target_requirements:
                    if x != None:
                        target_requirements[index] = x
                        break
        
        if target_requirements.count(-1) == 4:
            # if the only requirement is -1, we can put anything
            # TODO For the sake of testing, it will be 1
            target_requirements = np.full(4, int(np.random.choice(tiles).name))
    
        target_value = np.random.choice(target_requirements)  
        
        if target_value == "-1":
            target_value = int(np.random.choice(tiles).name)

        # Get the target as a Tile object
        target_tile = None
        for tile in tiles:
            if tile.name == str(target_value):
                target_tile = tile

        potential[target_x][target_y] = int(target_value)
        print("\n", target_value, type(target_value), target_coord, "\n", potential)
        propagate(target_tile, target_coord)


def main():
    image = np.zeros((10, 10))

    global tiles
    tiles = load_images("D:\Workspace\Python\IA para jogos\WFC_4GAMES\Images")

    # Fill a matrix with -1 that means any image can take this place
    global potential
    potential = np.full((10, 10), -1)
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
    random_neighbour((x, y))
    
    propagate(tiles[index], (x, y))
    # TODO make a dict of all neighbours
    # TODO Based on this random value fill the matrix with the neighbours

if __name__ == "__main__":
    main() 