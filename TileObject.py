#import TileRefObject as tile_ref
# UPDATE COMMENT BELOW

# This python file holds the Tile Class definition,
# which allows Tile objects to be instantiated.
# A tile is intended to be a unique set of numbers
# formed from a 'diamond-shaped' list of lists.
# Each tile holds its integer ID and unique nested list of numbers (value).
# During it's lifetime, each tile also has three tiles added to its scaffold
# list. These tiles are used to calculate the image tiles of the origin tile.
# Once computed, the scaffold list is emptied, and referrences to the image
# tiles are added to the origin tile.
# The Tile class also holds a static variable of the tile length,
# which is the length of the middle line of the tile value.
# This static variable describes the length of all tiles in the
# current computation under evaluation.

class Tile:
    tile_length = 0
    tile_prime = 0
    def __init__(self, id: int, value: list):
        self.id = id
        self.scaffolding = [] # This will hold scaffold tiles [Left, Upper, Right]
        self.value = value
        self.left_image = '*'
        self.upper_image = '*'
        self.right_image = '*'
        self.lower_image = '*'

    # We pass in the image tile ref to this function to save 'figuring out' which image variable to change
    # This function is now defunct, with the move to just using Tile objects.
    #def update_mapping (self, image_tile_ref: tile_ref.TileRef, image_tile):
    #    image_tile_ref.image_tile = image_tile

    # Function to add image tiles to a tile, and clear its scaffold list.
    def update_images (self, image_left, image_upper, image_right, image_lower):
        self.scaffolding = -1
        self.left_image=image_left
        self.upper_image=image_upper
        self.right_image=image_right
        self.lower_image=image_lower

    def tile_string(self):
        return f"Tile ID {self.id}, with value: \n {self.value}"

    def __str__(self):
        return str(self.value)
        #return f"Tile ID {self.id}, with value: \n {self.value}"

    def str_map(self):
        return f"Parent Tile ID {self.id}, left image ID {self.left_image.id}, upper image ID {self.upper_image.id}, right image ID {self.right_image.id}, lower image ID {self.lower_image.id}"

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