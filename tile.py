import numpy as np
import cv2

class Tile:
    """
    Constructor
    @param name - The name of the tile
    @param neightboors - The arraylist with the possible neightboors of this tile in the order (right, up, left, down)
    """
    def __init__(self, name, neightboors, image=None):
        self.name = name
        self.neightboors = neightboors
        self.sides = {"direita":self.neightboors[0], "cima":self.neightboors[1], "esquerda":self.neightboors[2], "baixo":self.neightboors[3]}
        self.image = image
    
    """
    Return the array of all the neightboors
    """
    def get_neightboors(self):
        return self.neightboors

    def get_neightboor(self, direction:str):
        """
        Return a specific direction neightboor
        @param direction - The direction to get the neightboor of
        """
        return self.sides.get(direction)