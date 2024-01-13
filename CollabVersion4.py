import TileObject as TO
import time
import CommonFunctions as CF
import CollabVersion3 as V3
import TileRefObject as TR
import CollabVersion3Plus as V3P

# Function to find all unique tiles and mappings/substitutions
# following the Version 4 process as defined in the CHANGELOG.md
# This function finds every image tile of every unique tile. Once
# this process is complete, every substitution rule for the number wall
# has been identified.
def v4(sub_rules, coding, prime):
    tile_len=TO.Tile.tile_length
    tiles={}
    new_tiles=[]
    tiles_by_index=[]
    # Instantiate zero'th Tile object
    tile0=TO.Tile(0, []) # The list is ignored here
    key0=str(tile0.value)
    # Add to tiles dict and ordered list
    tiles[key0]=(tile0)
    tiles_by_index.append(tile0)
    ones=tile0.value
    ones[-1]=[1,1]
    # Generate input substitution tiles (top row tiles)
    for i in range(len(sub_rules)):
        prev_wall=[[0],[1],[int(coding[i][1][0])]]
        for j in range(1, tile_len):
            prev_wall=V3.wall_gen(prime, prev_wall, int(coding[i][1][j])%prime)
        for j in range(2):
            prev_wall[0].remove(0)
            prev_wall[0].remove(0)
            prev_wall[1].remove(1)
        for j in range(tile_len//2-3):
            prev_wall.insert(0,[0 for k in range(tile_len-6-2*j)])
        key=str(prev_wall)
        new_tile=TO.Tile(len(tiles),prev_wall)
        tiles[key]=new_tile
        tiles_by_index.append(new_tile)
    # Generate images for top row tiles using substitution rules + zero tile
    for i in range(len(sub_rules)):
        left=sub_rules[i][1][0]
        right=sub_rules[i][1][1]
        left_tile=tiles_by_index[int(left)]
        right_tile=tiles_by_index[int(right)]
        # Use scaffolding tile generation technique to find fourth image tile
        output=V3P.tile_gen(left_tile, tile0, right_tile, prime)
        key=str(output)
        unique=tiles.get(key)
        tile_index=len(tiles)
        if (unique == None): # If tile not in tiles dict, its a new unique tile
            new_tile=TO.Tile(tile_index, output)
            tiles[key]=new_tile # Add to tiles dit
            new_tiles.append(new_tile)
            new_tile.scaffolding=[left_tile, tile0, right_tile] # Add scaffolding to the scaffolding list
            unique=new_tile
        current_tile=tiles_by_index[i+1]
        current_tile.update_images(left_tile, tile0, right_tile, unique)
    # Loop through list of tiles (excluding input section)
    # identifying the images of each tile
    count = 0
    while (new_tiles != []):
        tile=new_tiles.pop(0)
        if (tile.scaffolding != -1): # REMOVE******
            scaffolding=tile.scaffolding
            # Generate full image 4-tuples from scaffold tiles
            # to allow all four image tiles of the current tile to
            # be computed in one go.
            left_scaffold=image_to_tile(scaffolding[0])
            upper_scaffold=image_to_tile(scaffolding[1])
            right_scaffold=image_to_tile(scaffolding[2])
            if(count%10000 == 0):
                print("Unique tiles:", len(tiles), "- Processed tiles:", count*4, "- Remaining to process:", len(new_tiles))
            merged_image=nw_from_scaffold(left_scaffold, upper_scaffold, right_scaffold, prime)
            # Split merged image tiles into constituent tiles
            # ready to be assigned as images of current tile
            image=image_split(merged_image) # Returns images as [upper,left,right,lower]
            images=[]
            for i in range(len(image)):
                value=image[i]
                key=str(value)
                unique=tiles.get(key)
                index=len(tiles)
                # If the image tile is unique, add to tiles dict and new_tiles
                # list ready to have its own images processed
                if unique==None:
                    new_tile=TO.Tile(index, value)
                    tiles[key]=new_tile
                    new_tiles.append(new_tile)
                    # Construct scaffolding for new_tile
                    # For surety on scaffolding assembly, check 'general case' diagram
                    # Hint: scaffolding variable is a list of [left, upper, right] scaffold tiles for the parent tile
                    if(i == 0): # Upper tile
                        new_tile.scaffolding=[scaffolding[0].right_image, scaffolding[1].lower_image, scaffolding[2].left_image]
                    elif(i == 1): # Left tile
                        new_tile.scaffolding=[scaffolding[0].lower_image, scaffolding[0].right_image, images[0]]
                    elif(i == 2): # Right tile
                        new_tile.scaffolding=[images[0], scaffolding[2].left_image, scaffolding[2].lower_image]
                    elif(i == 3): # Lower tile
                        new_tile.scaffolding=[images[1], images[0], images[2]]
                    else:
                        return "ERROR"
                    unique=new_tile
                images.append(unique)
            # Update the image tiles of the current tile
            tile.update_images(images[1], images[0], images[2], images[3])
        count+=1
    # Instantiate true zero'th Tile object
    true_tile0=TO.Tile(0, []) # The list is ignored here
    true_key0=str([0])
    # Add to tiles dict
    tiles[true_key0]=(true_tile0)
    return tiles

# Function to split full image 4 tuple into constituent parts    
def image_split(image):
    tile_len=TO.Tile.tile_length
    to2=tile_len//2
    to2m1=to2-1
    # Upper tile
    upper=[]
    for i in range(to2):
        upper.append(image[i])
    for i in range(to2m1):
        upper.append(image[to2+i][2+2*i:-2-2*i])
    # Lower tile
    lower=[]
    for i in range(to2):
        lower.insert(0, image[-i-1])
    for i in range(to2m1):
        lower.insert(0, image[-to2-1-i][2+2*i:-2-2*i])
    # Left tile
    left=[]
    middle=tile_len-1
    left.append(image[middle][:-tile_len])
    for i in range(to2m1):
        left.insert(0, image[middle-1-i][:tile_len-2*i-2])
        left.append(image[middle+1+i][:tile_len-2*i-2])
    # Right tile
    right=[]
    right.append(image[middle][-tile_len:])
    for i in range(to2m1):
        right.insert(0, image[middle-1-i][-tile_len+2*i+2:])
        right.append(image[middle+1+i][-tile_len+2*i+2:])
    return [upper,left,right,lower]

# Function to calculate full image (all four tiles) from input scaffolding
def nw_from_scaffold(left_scaffold, upper_scaffold, right_scaffold, prime):
    tile_len=TO.Tile.tile_length*2
    to2=tile_len//2
    to2m1=to2-1
    incomplete_nw=[['*' for i in range(2*tile_len)] for j in range(2*tile_len-1)]
    # Left tile
    middle=(tile_len-1)
    tile=left_scaffold
    tile_it=tile_len//2 -1
    for i in range(tile_len):
        incomplete_nw[middle][i]=tile[tile_it][i]
    for i in range(tile_it):
        for j in range(tile_len-2-2*i):
            incomplete_nw[middle-i-1][1+j+i]=tile[tile_it-1-i][j]
            incomplete_nw[middle+1+i][1+i+j]=tile[tile_it+1+i][j]
    # Right tile
    tile=right_scaffold
    for i in range(tile_len):
        incomplete_nw[middle][i+tile_len]=tile[tile_it][i]
    for i in range(tile_it):
        for j in range(tile_len-2-2*i):
            incomplete_nw[middle-i-1][1+j+i+tile_len]=tile[tile_it-1-i][j]
            incomplete_nw[middle+1+i][1+i+j+tile_len]=tile[tile_it+1+i][j]
    # Upper tile
    tile=upper_scaffold
    for i in range(tile_len):
        incomplete_nw[tile_it][1+i+tile_it]=tile[tile_it][i]
    for i in range(tile_it):
        for j in range(tile_len-2-2*i):
            incomplete_nw[tile_it-i-1][2+j+i+tile_it]=tile[tile_it-1-i][j]
            incomplete_nw[tile_it+1+i][2+i+j+tile_it]=tile[tile_it+1+i][j]
    # Calculate lower tile
    complete_nw=V3.nw_from_tuple(incomplete_nw, prime)
    # Extract calculated lower tile
    calculated_four_tuple=[complete_nw[tile_len+to2m1][to2:tile_len+to2]]
    for i in range(to2m1):
        calculated_four_tuple.insert(0, complete_nw[tile_len+to2-i-2][to2+i+1:tile_len+to2m1-i])
        calculated_four_tuple.append(complete_nw[tile_len+to2+i][to2+i+1:tile_len+to2m1-i])
    return calculated_four_tuple

# Function to merge 4 image tiles into a full 4 tuple
def image_to_tile(tile: TO.Tile):
    left_tile=tile.left_image
    upper_tile=tile.upper_image
    right_tile=tile.right_image
    lower_tile=tile.lower_image
    tile_len=TO.Tile.tile_length
    length=tile_len*2
    to2=tile_len//2
    to2m1=to2-1
    output=[['*' for i in range(length)]]
    for i in range(length//2-1):
        output.insert(0, ['*' for i in range(length-2*i-2)])
        output.append(['*' for i in range(length-2*i-2)])
    # Upper tile
    for i in range(to2):
        output[i]=upper_tile.value[i]
    for i in range(to2m1):
        for j in range(tile_len-2-2*i):
            output[to2+i][2+j+2*i]=upper_tile.value[to2+i][j]
    # Lower tile
    for i in range(to2):
        output[-i-1]=lower_tile.value[-i-1]
    for i in range(to2m1):
        for j in range(tile_len-2-2*i):
            output[-(to2+i)-1][2+j+2*i]=lower_tile.value[-(to2+i)-1][j]
    middle=tile_len-1
    tile_middle=tile_len//2-1
    # Left tile
    for i in range(tile_len):
        output[middle][i]=left_tile.value[tile_middle][i]
    for i in range(to2m1):
        for j in range(tile_len-2-2*i):
            output[middle-1-i][j]=left_tile.value[tile_middle-1-i][j]
            output[middle+1+i][j]=left_tile.value[tile_middle+1+i][j]
    # Right tile
    for i in range(tile_len):
        output[middle][i+tile_len]=right_tile.value[tile_middle][i]
    for i in range(to2m1):
        for j in range(tile_len-2-2*i):
            output[middle-1-i][j+tile_len]=right_tile.value[tile_middle-1-i][j]
            output[middle+1+i][j+tile_len]=right_tile.value[tile_middle+1+i][j]
    return output

# Primary testing function.
def main():
    # *_sub_rules is the input substitution rules for tiles on the top row of this sequence
    pf_sub_rules=[['1','12'],['2','32'],['3','14'],['4','34']]
    sub_rules=pf_sub_rules # Pick the substitution rules of your desired sequence
    # *_coding is the input sequence split into the size of the input tiles
    pf_coding=[['1','00100110'],['2','00110110'],['3','00100111'],['4','00110111']]
    coding=pf_coding # Must match sequence used for sub_rules
    prime=3 # Currently tested with (pf) 3, 7 and (apf) N/A, and (pag) N/A
    TO.Tile.tile_length=len(coding[0][1]) # Set tile length from sequence coding
    start=time.time()
    print("Tiling Test with mod", prime, "and tile length", TO.Tile.tile_length)
    tiling_output=v4(sub_rules,coding,prime)
    tiling_time=time.time()
    print("- Tiling time =", tiling_time-start)
    print("Total number of unique tiles:", len(tiling_output))
    return tiling_output

output=main()
    