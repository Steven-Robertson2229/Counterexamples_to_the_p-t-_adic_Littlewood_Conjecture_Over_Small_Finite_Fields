import time
import random as rn
import copy as cop
import CommonFunctions as funct
import TileObject as tile
import TileRefObject as tile_ref
import CollabVersion3 as source

def tiling_adv(prime, seq):
    # Set up initial environment in similar way to V3 tiling.
    # Generate first slice -
    # Retrieve the tile length from the pre-configured variable in the Tile class
    tile_len=tile.Tile.tile_length 
    prev_wall=[[0,0],[1,1,1,1],[seq(0),seq(1)]]
    for i in range(2, tile_len-2):
        prev_wall=source.wall_gen(prime, prev_wall, seq(i)%prime)
    current_slice=prev_wall
    slice_count=1
    growth_marker=1
    tiles={}
    tiles_by_index=[]
    #maps={}
    new_tiles={}
    known_tiles={}
    col=0
    row=0
    # Hard code zero'th tile
    # Instantiate zero'th Tile object
    tile0=tile.Tile(0, [], (-999, -999)) # The list and tuple are ignored here
    key0=str(tile0.value)
    # Add to tiles dict and ordered list
    tiles[key0]=(tile0)
    tiles_by_index.append(tile0)
    # Update mapping within Tile object - all images are other tile0's
    # Hard code first tile
    tile1val=cop.deepcopy(prev_wall)
    for i in range(((tile_len-2)//2)-1):
        tile1val.insert(0, [0 for j in range((tile_len-4)-(2*i))])
    key1=str(tile1val)
    # Instantiate first Tile object
    tile1=tile.Tile(1, tile1val, (0, 0))
    # Add to tiles dict and ordered list
    tiles[key1]=(tile1)
    tiles_by_index.append(tile1)
    # Update mapping within Tile object - left is itself, upper is tile0
    tile1.update_mapping(tile1.left_image, tile1)
    tile1.update_mapping(tile1.upper_image, tile0)
    # Add images to dictionary of tiles that should be processed, where the value implies the following:
    # 1 = left image tile
    # 2 = upper image tile
    # 3 = right image tile
    # 4 = bottom image tile
    new_tiles[(0,1)]=tile1.right_image
    new_tiles[(1,0)]=tile1.lower_image
    # Tracker for number of tiles generated
    tiles_gen=0
    # Start slice list, which holds two lists:
    # List 1 contains all the tiles from the previous slice
    # List 2 contains all of the tiles computed so far in the current slice
    # This allows any new tile in the current slice to be computed from the available information
    current_slice=[[tile1],[]]
    while(slice_count<growth_marker*2):
        slice_count += 1
        # progress tracker print statement
        if(slice_count%50==0):
            print("Slice count:", slice_count,"- Unique tiles:", len(tiles), "- Processed tiles:", tiles_gen)
        col=slice_count-1
        row=0
        for i in range(slice_count):
            new_tile_val=[]
            # Does tile (row, col) appear in new_tiles list?
            # We have to maintain a list of new tiles to have a set of TileRef objects to hand
            image_tile_ref=new_tiles.get((row,col))
            if(image_tile_ref != None):
            # If yes, generate tiling, check uniqueness, find parent tile to add index to mapping, and remove from new_tiles
            # If no then tile exists in known_tiles, add Tile to slice wall, and add image Tiles to known_tiles dict
                tiles_gen += 1
                # Generate tile with tile_gen function
                new_tile_val=[]
                if (row == 0): # Top row needs specific handling
                    sequence=[seq(i)%prime for i in range(((slice_count-1)*tile_len)-2, ((slice_count)*tile_len)-2)]
                    new_tile_val=top_tile_gen(sequence, current_slice[0][0], prime)
                elif (row == 1): # Row 1 also needs specific handling
                    sequence=[seq(i)%prime for i in range(((slice_count-1)*tile_len)-2, ((slice_count)*tile_len)-2)]
                    new_tile_val=second_tile_gen(sequence, current_slice[0][0], prime)
                else:
                    new_tile_val=tile_gen(current_slice[0][1], current_slice[0][0], current_slice[1][row-1], prime)
                    current_slice[0].pop(0)
                # Check if tile is new/unique
                key=str(new_tile_val)
                unique=tiles.get(key)
                tile_index=len(tiles)
                if (unique == None): # If tile not in tiles dict, its a new unique tile
                    new_tile=tile.Tile(tile_index, new_tile_val, (row,col))
                    tiles[key]=new_tile # Add to tiles dit
                    tiles_by_index.append(new_tile)
                    growth_marker=slice_count
                    # Also record location of image tiles
                    if(row==0): # If we're on the top row, the upper image tile will be a zero tile
                        new_tile.update_mapping(new_tile.upper_image, tile0)
                    else:
                        new_tiles[(row*2-1,col*2+1)]=new_tile.upper_image # Upper image tile
                    new_tiles[(row*2,col*2)]=new_tile.left_image # Left image tile
                    new_tiles[(row*2,col*2+1)]=new_tile.right_image # Right image tile
                    new_tiles[((row*2)+1,(col*2))]=new_tile.lower_image # Lower image tile
                    image_tile_ref.image_tile=new_tile
                else: # Otherwise it is actually a previously seen tile
                    image_tile_ref.image_tile=unique
                    new_tile=unique
                    # Add image tiles to list of known future tiles
                    #if(slice_count<7500): # known tiles cheat
                    if(row!=0): # If we're on the top row, the upper image tile will be a zero tile
                        known_tiles[(row*2-1,col*2+1)]=new_tile.upper_image # Upper image tile
                    known_tiles[(row*2,col*2)]=new_tile.left_image # Left image tile
                    known_tiles[(row*2,col*2+1)]=new_tile.right_image # Right image tile
                    known_tiles[((row*2)+1,(col*2))]=new_tile.lower_image # Lower image tile
                new_tiles.pop((row,col))
                current_slice[1].append(new_tile)
            else:
                # Update image_tile_ref to the actual known TileRef
                image_tile_ref=known_tiles.pop((row,col))
                image_tile=image_tile_ref.image_tile
                current_slice[1].append(image_tile)
                if (row>1):
                    current_slice[0].pop(0)
                # Add image tiles to list of known future tiles
                #if(slice_count<7500): # known tiles cheat
                if(row!=0): # If we're on the top row, the upper image tile will be a zero tile
                    known_tiles[(row*2-1,col*2+1)]=image_tile.upper_image # Upper image tile
                known_tiles[(row*2,col*2)]=image_tile.left_image # Left image tile
                known_tiles[(row*2,col*2+1)]=image_tile.right_image # Right image tile
                known_tiles[((row*2)+1,(col*2))]=image_tile.lower_image # Lower image tile
            # Increment row and decrement col here
            row += 1
            col -= 1
        # Remove old previous slice, append new empty slice for next run
        current_slice.pop(0)
        current_slice.append([])
    
    # Clear current slice to save memory
    current_slice = []
    print("Number of unique tiles:", len(tiles))
    print("Number of generated tiles:", tiles_gen)
    print("Tiles unmapped (expected=0):", len(new_tiles))
    if len(new_tiles)>0:
        for key, val in new_tiles.items():
            print("Tile", key, "from position", val)
    print("Tiles overpredicted:", len(known_tiles))
    known_tiles = []
    cell_count=slice_count*tile_len
    print("Number Wall length (tiles):", slice_count, "and (cells):", cell_count)
    return tiles, tiles_by_index, cell_count

# Generates the lower tile based on the three tiles above it
# This version of the function works for any row other than row 0
def tile_gen(left_tile: tile.Tile, upper_tile: tile.Tile, right_tile: tile.Tile, prime: int):
    tile_len=tile.Tile.tile_length
    output_tile_val=[]
    left_tile_val=left_tile.value
    upper_tile_val=upper_tile.value
    right_tile_val=right_tile.value
    incomplete_nw=[['*' for i in range(2*tile_len)] for j in range(2*tile_len-1)]
    # Left tile
    middle=(len(incomplete_nw)-1)//2
    tile_it=tile_len//2 -1
    for i in range(tile_len):
        incomplete_nw[middle][i]=left_tile_val[tile_it][i]
    for i in range(tile_it):
        for j in range(tile_len-2-2*i):
            incomplete_nw[middle-i-1][1+j+i]=left_tile_val[tile_it-1-i][j]
            incomplete_nw[middle+1+i][1+i+j]=left_tile_val[tile_it+1+i][j]
    # Right tile
    for i in range(tile_len):
        incomplete_nw[middle][i+tile_len]=right_tile_val[tile_it][i]
    for i in range(tile_it):
        for j in range(tile_len-2-2*i):
            incomplete_nw[middle-i-1][1+j+i+tile_len]=right_tile_val[tile_it-1-i][j]
            incomplete_nw[middle+1+i][1+i+j+tile_len]=right_tile_val[tile_it+1+i][j]
    # Upper tile
    for i in range(tile_len):
        incomplete_nw[tile_it][1+i+tile_it]=upper_tile_val[tile_it][i]
    for i in range(tile_it):
        for j in range(tile_len-2-2*i):
            incomplete_nw[tile_it-i-1][2+j+i+tile_it]=upper_tile_val[tile_it-1-i][j]
            incomplete_nw[tile_it+1+i][2+i+j+tile_it]=upper_tile_val[tile_it+1+i][j]
    complete_nw=source.nw_from_tuple(incomplete_nw, prime)
    # Extract calculated lower tile
    output_tile_val=[complete_nw[tile_len+tile_len//2-1][tile_len//2:tile_len+tile_len//2]]
    for i in range(tile_len//2-1):
        output_tile_val.insert(0, complete_nw[tile_len+tile_len//2-i-2][tile_len//2+i+1:tile_len+tile_len//2-i-1])
        output_tile_val.append(complete_nw[tile_len+tile_len//2+i][tile_len//2+i+1:tile_len+tile_len//2-i-1])
    complete_nw=[]
    return output_tile_val

# Generates a new tile on row 0
def top_tile_gen(seq: list, left_tile: tile.Tile, prime: int):
    tile_len=tile.Tile.tile_length
    output_tile_val=[]
    left_tile_val=cop.deepcopy(left_tile.value)
    left_tile_val.pop(0)
    left_tile_val.pop(0)
    complete_nw=source.slice_gen(prime, left_tile_val, seq)
    output_tile_val.append(cop.deepcopy(complete_nw[1]))
    for j in range((tile_len-2)//2):
        output_tile_val.insert(0, [0 for k in range(tile_len-2-2*j)])
        output_tile_val.append(complete_nw[2+j][-(tile_len-2-2*j):])
    complete_nw=[]
    return output_tile_val

# Generates a new tile on row 1
def second_tile_gen(seq: list, left_tile: tile.Tile, prime: int):
    tile_len=tile.Tile.tile_length
    output_tile_val=[]
    left_tile_val=cop.deepcopy(left_tile.value)
    left_tile_val.pop(0)
    left_tile_val.pop(0)
    complete_nw=source.slice_gen(prime, left_tile_val, seq)
    tile_mid=(tile_len//2)+1
    output_tile_val.append(cop.deepcopy(complete_nw[tile_mid]))
    for j in range((tile_len-2)//2):
        output_tile_val.insert(0, complete_nw[tile_mid-1-j][:-(j+1)*2])
        output_tile_val.append(complete_nw[tile_mid+1+j])
    complete_nw=[]
    return output_tile_val

# Primary testing function.
def main():
    # Input variables
    prime_input=7 # Currently tested with (pf) 3, 7, 11, and (apf) 5, and (pag) 3
    tile_length=8 # Currently tested with 8 and 16 length
    tile.Tile.tile_length=tile_length
    sequence=funct.pap_f # Currently pap_f, pap_f5, or pagoda
    # Naive tiling verify
    bad_verify=False
    # Official proof tiling verify
    true_verify=False
    start=time.time()
    print("Tiling Test with mod", prime_input, "and tile length", tile_length)
    # tiling_output = [tiles_dict, maps_dict, tiles_by_index, cell_count]
    tiling_output = tiling_adv(prime_input, sequence)
    tiling_time=time.time()
    print("- Tiling time =", tiling_time-start)
    # converted_tiling = [tiles_by_index, maps_by_index]
    #converted_tiling = convert_tiling(tiling_output[0], tiling_output[1], tiling_output[2])
    if(bad_verify):
        #length_check=tiling_output[3]
        #pseudo_number_wall(converted_tiling[0], converted_tiling[1], sequence, prime_input, length_check)
        return
    if(true_verify):
        tuple_start=time.time()
        #unique_tuples=four_tuples(converted_tiling[1])
        #print('Number of unique four-tuples =', len(unique_tuples))
        tuple_end=time.time()
        print("- Tuple time =", tuple_end-tuple_start)
        verify_start=time.time()
        #proof=verify_tuples(unique_tuples, converted_tiling[0], tiling_output[0], prime_input)
        verify_end=time.time()
        #print("Proof result =", proof[0])
        #if(proof[0]==False):
            #print("Expected:", proof[1])
            #print("Calculated:", proof[2])
        print("- Verify time =", verify_end-verify_start)
        end=time.time()
        print("- Full time =",end-start)
        #return unique_tuples
    return tiling_output
output=main()

# Hint: if you need to print a tile/number wall section/list, use the following and update list_name
#print('\n'.join('{}: {}'.format(*k) for k in enumerate(list_name)))
# MIN RUNTIME ON PF F7 WITH KNOWN TILE CHEAT = 285 SECS
# MAX MEMORY USAGE ON PF F7 WITH KNOWN TILE CHEAT = 18GB (>30GB without cheat)
