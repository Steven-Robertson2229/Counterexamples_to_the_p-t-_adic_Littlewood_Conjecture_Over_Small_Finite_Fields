
# This python file holds the Tile Class definition,
# which allows Tile objects to be instantiated.
# A tile is intended to be a unique set of numbers
# formed from a 'diamond-shaped' list of lists.
# Each Tile holds its integer ID and unique nested list of numbers (value).
# During it's lifetime, each Tile also has three other Tiles added to its scaffold
# list. These Tiles are used to calculate the image Tiles of the origin Tile.
# Once computed, the scaffold list is emptied, and referrences to the image
# Tiles are added to the origin Tile.
# The Tile class holds a static variable of the tile length,
# which is the length of the middle line of the Tile's value.
# This static variable describes the length of all tiles in the
# current computation under evaluation.
# The Tile class holds a static variable of the Tile's prime,
# which can be used to find the prime number used for computing
# values for all Tiles in a single program execution.

class Tile:
    tile_length = 0
    tile_prime = 0
    # Tile Class constructor
    def __init__(self, id: int, value: list):
        self.id = id
        self.scaffolding = [] # This will hold scaffold tiles [Left, Upper, Right]
        self.value = value
        self.left_image = '*'
        self.upper_image = '*'
        self.right_image = '*'
        self.lower_image = '*'

    # Function to add image tiles to a Tile, and clear its scaffold list.
    def update_images (self, image_left, image_upper, image_right, image_lower):
        self.scaffolding = -1
        self.left_image=image_left
        self.upper_image=image_upper
        self.right_image=image_right
        self.lower_image=image_lower

    # Function to return a print-friendly overview of a Tile
    def tile_string(self):
        return f"Tile ID {self.id}, with value: \n {self.value}"

    # Function to return the raw integer list ('value') of a Tile as a string
    def __str__(self):
        return str(self.value)

    # Function to return a print-friendly overview of a Tile and its images
    def str_map(self):
        return f"Parent Tile ID {self.id}, left image ID {self.left_image.id}, upper image ID {self.upper_image.id}, right image ID {self.right_image.id}, lower image ID {self.lower_image.id}"
