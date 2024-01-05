

class TileRef:
    def __init__(self, parent_tile, image_tile):
        self.parent_tile = parent_tile
        self.image_tile = image_tile

    def __str__(self):
        return str(self.image_tile)