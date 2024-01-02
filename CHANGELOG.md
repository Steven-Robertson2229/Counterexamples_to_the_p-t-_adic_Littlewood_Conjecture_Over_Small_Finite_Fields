## Preamble
This change log primarily describes the differences between the Number Wall generation process and tile/mapping computation process of various iterations of our code. The verification stage of the program only came into existence for version 3 of the program, and is unlikely to see much change during version 4 and version 5 due to limited optimisation opportunities.

## Version 1
TODO - please describe this Steven

## Version 2
TODO - please describe this Steven

## Version 3
For Version 3, the Number Wall generation process and tiling/mapping process have combined. We now generate 'slices' of the number wall, where a single slice is a new set of tiles running down the right-hand side of the Number Wall triangle. In other words, we generate enough new numbers/cells for each row of the Number Wall to allow the processing of a new column of tiles along the right-hand side of the Number Wall. This allows us to only store the data for a single slice at a time (along with the on-going set of unique tiles and mappings), rather than the entire Number Wall, saving vast amounts of memory.

The process involves repeatedly generating all the Number Wall entries for a slice, and then processing 'interesting' tiles down the length of the slice. We define 'interesting' tiles as tiles that relate back to a previously created tile mapping that has yet to be completed. For context, each unique tile maps to four tiles double the distance away on the Number Wall. So, a tile mapping is only considered complete once we have found all four of its child tiles.

When we process an 'interesting' tile, we relate it back to it's parent tile's mapping. We also check whether this tile is a new unique tile, or one we have previously seen. If it is a new tile, then we add the coordinates of its child tiles to our list of upcoming 'interesting' tiles; we also record it as a unique tile and begin building its tile mapping. By only processing 'interesting' tiles, we avoid processing tiles that we know cannot be unqiue, and are not required as part of an incomplete mapping - as skipped tiles belong to tile mappings that have already been completed (i.e. their parent tile is a previously seen tile). Earlier iterations of Version 3 did not include this skip, and so processed every single possible tile. It is worth noting that we are still generating every number/cell in a slice, we only skip processing non-unqiue tiles with this improvement.

The slice generation process halts once we have doubled the size of the Number Wall without finding any new 'interesting' tiles - at which point all of our tile mappings must be complete, meaning that there are no new unique tiles to find as we have generated a complete set of substitution rules for the given sequence and prime input.

Earlier versions of the program did not have the capability to build the tile mapping relationships, they were only able to build the set of unique tiles (which is not sufficient information to verify the integrity of our results).

Version 3 also includes several minor improvements to the Number Wall generation process, such as including more efficient 'cheat' calculations for edge-case tiles, and better inner/outer window frame computation.

Version 3 has been proven capable of computing a complete set of substitution rules for the Paper Folding sequence up to F11.

## Version 4
TODO - write up (this has previously been called Version 3.5)

## Version 5
TODO - write up (this has previously been called Version 4)