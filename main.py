import numpy as np
from tile import Tile
from collections import namedtuple
import os


# TODO wave function collapse
# TODO make a matrix to represent the image, fill the image with possible values and short it with the neightboor values

# We can have 2 aproaches, start with all number interpretation and change it to the images later or learn how to do it
# from the start with images.
# For the sake of my mind we'll use nambers as image names.

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
        neightboors = info[1].replace("[", "").replace("]", "").split(",")
        tile = Tile(name, neightboors)
        tiles.append(tile)
    
    return tiles

def neightboors_dictionary(tiles):
    """
    Save the array info into a dictionary
    """
    pass


def main():
    image = np.zeros((10, 10))

    tiles = load_images("D:\Workspace\Python\IA para jogos\WFC_4GAMES\Images")

    # Fill a matrix with -1 that means any image can take this place
    potential = np.full((10, 10), -1)

    print(potential, "\n\n")

    # TODO select a random point in the matrix

    x = np.random.randint(0, 10)
    y = np.random.randint(0, 10)
    index = np.random.randint(0, len(tiles))
    potential[x][y] = tiles[index].name
    print(tiles[index].name, "\n")
    print(tiles[index].get_neightboor())
    print(potential)

    # TODO make a dict of all neightboors
    # TODO Based on this random value fill the matrix with the neightboors

if __name__ == "__main__":
    main() 