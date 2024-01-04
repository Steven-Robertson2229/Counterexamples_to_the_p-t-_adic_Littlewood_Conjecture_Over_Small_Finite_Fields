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
    def __init__(self, id, value, coord):
        self.id = id
        self.value = value
        self.location = coord
    
    def __str__(self):
        return f"Tile ID {self.id}, location {self.location}, with value: \n {self.value}"

def main():
    print("Tile object test -")
    test = Tile(1, [[1,2,3],[4,5,6],[7,8,9]], (1,2))
    print(test)
    print("Updating Tile location variable -")
    test.location = (123, 456)
    print("Specific Tile variable retrieval test -", test.location)
main()