# Redundant tile support class from an old version of the Tile class

class TileRef:
    def __init__(self, image_tile):
        self.image_tile = image_tile

    def __str__(self):
        return str(self.image_tile)