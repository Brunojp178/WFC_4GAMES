import numpy as np
from tile import Tile
import collections
# from collections import namedtuple
import os
import cv2


def verifica():
    """
    Verify if the matrix has empty spaces
    """
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
        image = cv2.imread(dir_path + "/" + name + ".png")

        # neighbours now will be the name of the image file.
        neighbours = info[1].replace("[", "").replace("]", "").replace("\n", "").split(",")
        tile = Tile(name, neighbours, image)
        tiles.append(tile)
    
    return tiles

def empty_neighbour(tile_pos:(int, int)):
    """
    Check around a cell for empty spaces (-1 values)
    """
    y, x = tile_pos
    height, width = potential.shape
    height -= 1
    width -= 1

    empty = [None, None, None, None] # Array of 4 positions filled with none   

    if verifica():
        return empty

    if y != 0:
        if potential[y - 1][x] == -1:
            empty[2] = ((y - 1, x))

    if y != width:
        if potential[y+1][x] == -1:
            empty[0] = ((y + 1, x))
    
    if x != 0:
        if potential[y][x - 1] == -1:
            empty[1] = ((y, x - 1))
    
    if x != height:
        if potential[y][x + 1] == -1:
            empty[3] = ((y, x + 1))
    
    return empty

def random_neighbour(tile_pos:(int, int)):
    """
    Return the y, x coordinate of a random cell around one tile.
    """
    y, x = tile_pos
    height, width = potential.shape
    height -= 1
    width -= 1

    # Possible values of y
    target_y = [y + 1, y - 1]
    target_x = [x + 1, x - 1]

    # if the father tile is on a border, remove the out of range index of the possible values for target
    if (y == 0):
        target_y[0] = y + 2
    elif(y == width):
        target_y[1] = y - 2

    if (x == 0):
        target_x[0] = x + 2
    elif(x == height):
        target_x[1] = x - 2

    # Recursive fucker
    final_y = np.random.choice(target_y)
    final_x = np.random.choice(target_x)

    if final_y == -1:
        final_y += 1

    if final_x == -1:
        final_x += 1

    if final_y == 10:
        final_y -= 1

    if final_x == 10:
        final_x -= 1

    return (final_y, final_x)

def check_around(tile_pos:(int, int)):
    """
    Return a list of possible values of a cell based on the requirements of its neighbours.
    """
    cell_y, cell_x = tile_pos
    height, width = potential.shape
    height -= 1
    width -= 1

    if cell_y == width:
        right = -1
    else:
        right = potential[cell_y + 1][cell_x]

    if cell_x == 0:
        up = -1
    else:
        up = potential[cell_y][cell_x - 1]
    
    if cell_y == 0:
        left = -1
    else:
        left = potential[cell_y - 1][cell_x]

    if cell_x == height:
        down = -1
    else:
        down = potential[cell_y][cell_x + 1]

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
    """
    Propagate values on the matrix from a specific cell
    """
    if verifica():
        return 0

    # Get all the cells around the tile and check if they are empty
    # if neighbours cells are already filled, get a random one and propagate from it
    possible_neighbours = np.zeros(0, dtype=object)
    possible_neighbours = empty_neighbour(tile_pos)

    if possible_neighbours.count(None) == 4:
        new_posY, new_posX = random_neighbour(tile_pos) # Positions of a random one

        new_tile_name = potential[new_posY][new_posX]   # The name of this random one
        new_tile = None

        # Note: the tiles list is the representation of the images in Tiles class 
        # so we search for the Tile representation of "new_tile_name"
        for tile in tiles:
            if tile.name == str(new_tile_name):
                new_tile = tile
        
        propagate(new_tile, (new_posY, new_posX))
    else:
        # Aux list that hold probabilities to use in np.random.choice(), making the probabilitie of None to be chose equal to 0
        for index, i in enumerate(possible_neighbours):
            if i == None:
                for y in possible_neighbours:
                    if y != None:
                        possible_neighbours[index] = y
                        break
        
        # creating an aux array filled with index based on possible_neighbours
        aux = []
        for i in range(len(possible_neighbours)):
            aux.append(i)
        
        target_coord = possible_neighbours[np.random.choice(aux)]
        target_y, target_x = target_coord
        
        target_requirements = check_around(target_coord)
        
        # Take out the None values on the target_requirements list
        for index, i in enumerate(target_requirements):
            if i == None:
                for y in target_requirements:
                    if y != None:
                        target_requirements[index] = y
                        break

        # if the only requirement is -1, we can put anything
        if target_requirements.count(-1) == 4:
            target_requirements = np.full(4, int(np.random.choice(tiles).name))
        
        # Get the value that it's most required to fill the cell. ( ex. [1, 2, 2, 3], "2" will be chosen )
        occurrences = collections.Counter(target_requirements)
        target_value = max(occurrences)
                
        if target_value == "-1":
            target_value = int(np.random.choice(tiles).name)

        # Get the representation of target as a Tile object on the tiles list
        target_tile = None
        for tile in tiles:
            if tile.name == str(target_value):
                target_tile = tile

        potential[target_y][target_x] = int(target_value)
        # To debug
        # print("\n", target_value, type(target_value), target_coord, "\n", potential)
        propagate(target_tile, target_coord)

def make_image():
    # TODO roda toda a potential
    # rodar todo o arquivo e a potential
    height, width = potential.shape
    
    # blank image
    img = np.zeros((tiles[0].image.shape))
    images_horizontal = []
    images_vertical = []

    for y in range(height):
        for x in range(width):
            tile_name = str(potential[y][x])
            for tile in tiles:
                if tile.name == tile_name:
                    images_horizontal.append(tile.image)
        
        aux_img = cv2.hconcat(images_horizontal)
        images_horizontal.clear()

        images_vertical.append(aux_img)
    
    result_img = cv2.vconcat(images_vertical)
    cv2.imshow("Result", result_img)
    cv2.waitKey(0)
    
    

# def rotate_matrix(matrix):
#     return np.rot90(matrix)

def main():
    image = np.zeros((10, 10))

    global tiles
    tiles = load_images("D:\Workspace\Python\IA para jogos\WFC_4GAMES\Images")

    # Fill a matrix with -1 that means any image can take this place
    global potential
    potential = np.full((10, 10), -1)
    print(potential, "\n")

    # TODO select a random point in the matrix
    # Limiting the index of random choice
    height, width = potential.shape

    y = np.random.randint(0, width)
    x = np.random.randint(0, height)
    index = np.random.randint(0, len(tiles))
    print("First tile:", tiles[index].name)

    potential[y][x] = tiles[index].name
    print(potential)
    # TODO remember potential[y][x] is a number (potential[y][x] doesn'y return a tile)
    random_neighbour((y, x))
    
    propagate(tiles[index], (y, x))

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    make_image()

if __name__ == "__main__":
    main() 