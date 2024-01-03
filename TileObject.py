# This python file holds the Tile Class definition,
# which allows Tile objects to be instantiated.
# A tile is intended to be a unique set of numbers
# formed from a 'diamond-shaped' list of lists.
# Each tile holds its integer ID, unique nested list of numbers (value),
# and original Number Wall location co-ordiates tuple (?).

# We could also store the tile length if desired,
# although this can be computed at run-time, and is
# not expected to be different for each tile.

class Tile:
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