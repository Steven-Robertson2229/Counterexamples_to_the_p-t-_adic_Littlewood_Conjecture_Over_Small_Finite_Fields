import TileRefObject as tile_ref
# This python file holds the Tile Class definition,
# which allows Tile objects to be instantiated.
# A tile is intended to be a unique set of numbers
# formed from a 'diamond-shaped' list of lists.
# Each tile holds its integer ID, unique nested list of numbers (value),
# and original Number Wall location co-ordiates tuple (?).
# The Tile class also holds a static variable of the tile length,
# which is the length of the middle line of the tile value.
# This static variable describes the length of all tiles in the
# current computation under evaluation.

# We could also store additional information such as the parent tile index of
# each tile, but it is unclear if that would be useful at this point in time.

class Tile:
    tile_length = 0
    def __init__(self, id: int, value: list):
        self.id = id
        # Specific constructor for zeroth tile
        if id==0:
            self.value = []
            self.value.append([0 for i in range(Tile.tile_length)])
            for i in range((Tile.tile_length-2)//2):
                self.value.insert(0, [0 for j in range((Tile.tile_length-2)-(2*i))])
                self.value.append([0 for j in range((Tile.tile_length-2)-(2*i))])
            #zeroRef=tile_ref.TileRef(self)
            self.left_image = self
            self.upper_image = self
            self.right_image = self
            self.lower_image = self
        else:
            self.value = value
            self.left_image = -1
            self.upper_image = -1
            self.right_image = -1
            self.lower_image = -1

    # We pass in the image tile ref to this function to save 'figuring out' which image variable to change
    def update_mapping (self, image_tile_ref: tile_ref.TileRef, image_tile):
        image_tile_ref.image_tile = image_tile

    def __str__(self):
        return f"Tile ID {self.id}, with value: \n {self.value}"

    def str_map(self):
        return f"Parent Tile ID {self.id}, left image ID {self.left_image}, upper image ID {self.upper_image}, right image ID {self.right_image}, lower image ID {self.lower_image}"

# This function is simply a set of tests to demonstrate some key principles about using the Tile class
def main():
    print("Tile object test -")
    test = Tile(1, [[1,2,3],[4,5,6],[7,8,9]], (1,2))
    print(test)
    print("Updating Tile location variable -")
    test.location = (123, 456)
    print("Specific Tile variable retrieval test -", test.location)
    print("TileRef pointer interaction test -")
    tile_ref=test.left_image
    ref_test = [tile_ref]
    tile_ref.image_tile = Tile(2, [[1,],[4,5,6],[7]], (3,4))
    print(ref_test[0]) # Proves that updating the TileRef object in one place updates it in every place
    ref_test.append(test.upper_image)
    print(ref_test[1]) # Proves concept still works with unmapped image tiles in a TileRef

#main()