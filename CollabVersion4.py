import TileObject as TO
import time
import CommonFunctions as CF

# Set of functions to find all unique tiles and mappings/substitutions
# following the Version 4 process as defined in the CHANGELOG.md
# This function finds every image tile of every unique tile. Once
# this process is complete, every substitution rule for the number wall
# has been identified.

# The various algorithm sections as defined in our research paper
# (Counter examples to the p(t)-adic Littlewood Conjecture Over Small Finite Fields)
# have been noted at the definition of each related function, as well as in the main
# testing function at the bottom of the file.


# ***Algorithm 1.1: Initial Conditions***
# Function to ???
# When it completes, this function automatically calls the tile_computation
# function to begin the main tile generating process.
###
def input_generator(seq, write_output):
    sub_rules,coding=sub_rule_full(seq) # Generates the substitution rules used to compute input tiles
    tile_len=TO.Tile.tile_length
    prime=TO.Tile.tile_prime
    print('sub_rules=')
    for i in sub_rules:
        print(i)
    print('coding=')
    for i in coding:
        print(i)
    tiles={} # Dictionary of all unique tiles
    new_tiles=[] # List of all uncomputed tiles
    tiles_by_index=[] # List of all unique tiles in an indexable format
    # Instantiate Tile object for the tile of all zeros
    tile0_value=[[0 for i in range(tile_len)]]
    for i in range(tile_len//2 -1):
        tile0_value.insert(0,([0 for i in range(tile_len-2-2*i)]))
        tile0_value.append([0 for i in range(tile_len-2-2*i)])
    tile0=TO.Tile(0, tile0_value)
    key0=str(tile0_value)
    tiles[key0]=(tile0)
    tiles_by_index.append(tile0)
    tiles[key0].update_images(tile0, tile0, tile0, tile0)
    # Instantiate Tile object for the tile above the input row
    tile1_value=[[0 for i in range(tile_len)]]
    for i in range(tile_len//2 -2):
        tile1_value.insert(0,([0 for i in range(tile_len-2-2*i)]))
        tile1_value.append([0 for i in range(tile_len-2-2*i)])
    tile1_value.append([1,1])
    tile1_value.insert(0,[0,0])
    tile1=TO.Tile(1, tile1_value)
    key1=str(tile1.value)
    tiles[key1]=(tile1)
    tiles_by_index.append(tile1)
    tile1.update_images(tile0,tile0,tile0,tile1)
    # Generate input substitution tiles (top row tiles)
    for i in range(len(sub_rules)):
        prev_wall=[[0],[1],[int(coding[i][1][0])]]
        for j in range(1, tile_len):
            prev_wall=CF.wall_gen(prime, prev_wall, int(coding[i][1][j])%prime)
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
    # Generate images for all unique top row tiles using substitution rules + zero tile
    for i in range(len(sub_rules)):
        left=sub_rules[i][1][0]
        right=sub_rules[i][1][1]
        left_tile=tiles_by_index[int(left)+1]
        right_tile=tiles_by_index[int(right)+1]
        # Use scaffolding tile generation technique to find fourth image tile
        output=tile_gen(left_tile, tile1, right_tile, prime)
        key=str(output)
        unique=tiles.get(key)
        tile_index=len(tiles)
        if (unique == None): # If tile not in tiles dict, its a new unique tile
            new_tile=TO.Tile(tile_index, output)
            tiles[key]=new_tile # Add to tiles dit
            new_tiles.append(new_tile) # add to new_tiles list
            new_tile.scaffolding=[left_tile, tile1, right_tile] # Add scaffolding to the tile's scaffolding list
            unique=new_tile
        current_tile=tiles_by_index[i+2]
        current_tile.update_images(left_tile, tile1, right_tile, unique) # Update image tiles of current_tile
    return tile_computation(tiles, new_tiles, write_output) # Calls main tile computation function before returning

# ***Algorithm 1.2: Generating the Complete Set of Tiles***
# Add desc ***
###
def tile_computation(tiles, new_tiles, write_output):
    # Loop through list of tiles (excluding input section)
    # identifying the images of each tile
    count=1
    prime=TO.Tile.tile_prime
    if write_output:
        f=open('progress_tracker_F'+str(prime)+'.txt', 'w')
    while (new_tiles != []):
        tile=new_tiles.pop(0) # Removes tile from the list, as well as retrieveing it
        if (tile.scaffolding != -1):
            scaffolding=tile.scaffolding
            # Generate full image 4-tuples from scaffold tiles
            # to allow all four image tiles of the current tile to
            # be computed in one go.
            left_scaffold=image_to_tile(scaffolding[0])
            upper_scaffold=image_to_tile(scaffolding[1])
            right_scaffold=image_to_tile(scaffolding[2])
            if(count%10000 == 0):
                if write_output:
                    f=open('progress_tracker_F'+str(prime)+'.txt', 'a')
                    f.write("Unique tiles: "+ str(len(tiles))+ " - Processed tiles: "+ str(count*4)+  " - Unprocessed tile backlog: "+ str(len(new_tiles)))
                    f.write('\n')
                    f.close()
                print("Unique tiles:", len(tiles), "- Processed tiles:", count*4, "- Unprocessed tile backlog:", len(new_tiles))
            merged_image=nw_from_scaffold(left_scaffold, upper_scaffold, right_scaffold, prime)
            # Split merged image tiles into constituent tiles
            # ready to be assigned as images of current tile
            image=image_split(merged_image) # Returns images as [upper, left, right, lower]
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
    return tiles

# ***Algorithm 2.1: Generating all possible 4-tuples***
# Add func description
###
def generate_four_tuples(tiles):
    tuples_by_index=[]
    for i in tiles:
        tile_curr=tiles[i]
        tuples_by_index.append([tile_curr.left_image.id,tile_curr.upper_image.id,tile_curr.right_image.id,tile_curr.lower_image.id])
   # Build dict of unique images
    tuples={}
    for tups in tuples_by_index:
        key=str(tups)
        tuples[key]=tups
    # For each mapping, check the unknown tuple combinations for new tuples
    # Skip first entry, its all zeros
    count=0
    for tup in tuples_by_index:
        count+=1
        # Take care when zero tiles are present
        # Treat four-tuple rotated as a square
        image_tuple=[['*' for i in range(4)] for j in range(4)]
        entry_image1=tuples_by_index[tup[0]]
        entry_image2=tuples_by_index[tup[1]]
        entry_image3=tuples_by_index[tup[2]]
        entry_image4=tuples_by_index[tup[3]]
        # Left image
        image_tuple[0][0]=entry_image1[0]
        image_tuple[0][1]=entry_image1[1]
        image_tuple[1][0]=entry_image1[3]
        image_tuple[1][1]=entry_image1[2]
        # Upper image
        image_tuple[0][2]=entry_image2[0]
        image_tuple[0][3]=entry_image2[1]
        image_tuple[1][2]=entry_image2[3]
        image_tuple[1][3]=entry_image2[2]
        # Right image
        image_tuple[2][2]=entry_image3[0]
        image_tuple[2][3]=entry_image3[1]
        image_tuple[3][2]=entry_image3[3]
        image_tuple[3][3]=entry_image3[2]
        # Lower image
        image_tuple[2][0]=entry_image4[0]
        image_tuple[2][1]=entry_image4[1]
        image_tuple[3][0]=entry_image4[3]
        image_tuple[3][1]=entry_image4[2]

        # Search for new tuples
        new_tuples=[]
        # Take care when zero tiles are present, those should not be used when forming the Upper and Right tuples
        if tup[1]>1:
            new_tuples.append([image_tuple[0][1],image_tuple[0][2],image_tuple[1][2],image_tuple[1][1]]) # Upper tuple
            new_tuples.append([image_tuple[1][2],image_tuple[1][3],image_tuple[2][3],image_tuple[2][2]]) # Right tuple
        new_tuples.append([image_tuple[1][0],image_tuple[1][1],image_tuple[2][1],image_tuple[2][0]]) # Left tuple
        new_tuples.append([image_tuple[2][1],image_tuple[2][2],image_tuple[3][2],image_tuple[3][1]]) # Lower tuple
        new_tuples.append([image_tuple[1][1],image_tuple[1][2],image_tuple[2][2],image_tuple[2][1]]) # Middle tuple
        # Check each new tuple for uniqueness
        for new_tup in new_tuples:
            key=str(new_tup)
            unique=tuples.get(key)
            if not unique: # If tuple not in tuples dictionary
                tuples[key]=new_tup # Add to tuples dictionary
                tuples_by_index.append(new_tup)
    return tuples_by_index

# ***Algorithm 2.2: Verifying the 4-tuples***
# Add func description
###
def verify_four_tuples(tuples_by_index, tiles, write_output):
    tiles_by_index=[]
    prime=TO.Tile.tile_prime
    for i in tiles:
        tiles_by_index.append(tiles[i].value)
    tile_len=len(tiles_by_index[0])+1
    tuples_num=len(tuples_by_index)//4
    print_helper=1
    count=0
    for tup in tuples_by_index[2:]:
        if(count==(tuples_num*print_helper)):
            print("Verification process at", 25*print_helper,"% complete!")
            if write_output:
                f=open('progress_tracker_F'+str(prime)+'.txt', 'a')
                f.write("Verification process at"+ str(100*count/len(tuples_by_index))+"% complete!")
                f.write('\n')
                f.close()
            print_helper += 1
        if(tup[1]==0):
            pass
        else:
            incomplete_nw=[['*' for i in range(2*tile_len)] for j in range(2*tile_len-1)]
            # Left tile
            middle=(len(incomplete_nw)-1)//2
            tile=tiles_by_index[tup[0]]
            tile_it=tile_len//2 -1
            for i in range(tile_len):
                incomplete_nw[middle][i]=tile[tile_it][i]
            for i in range(tile_it):
                for j in range(tile_len-2-2*i):
                    incomplete_nw[middle-i-1][1+j+i]=tile[tile_it-1-i][j]
                    incomplete_nw[middle+1+i][1+i+j]=tile[tile_it+1+i][j]
            # Right tile
            tile=tiles_by_index[tup[2]]
            for i in range(tile_len):
                incomplete_nw[middle][i+tile_len]=tile[tile_it][i]
            for i in range(tile_it):
                for j in range(tile_len-2-2*i):
                    incomplete_nw[middle-i-1][1+j+i+tile_len]=tile[tile_it-1-i][j]
                    incomplete_nw[middle+1+i][1+i+j+tile_len]=tile[tile_it+1+i][j]
            # Upper tile
            tile=tiles_by_index[tup[1]]
            for i in range(tile_len):
                incomplete_nw[tile_it][1+i+tile_it]=tile[tile_it][i]
            for i in range(tile_it):
                for j in range(tile_len-2-2*i):
                    incomplete_nw[tile_it-i-1][2+j+i+tile_it]=tile[tile_it-1-i][j]
                    incomplete_nw[tile_it+1+i][2+i+j+tile_it]=tile[tile_it+1+i][j]
            # Calculate lower tile
            complete_nw=nw_from_tuple(incomplete_nw, prime)
            # Extract calculated lower tile
            calculated_four_tuple=[complete_nw[tile_len+tile_len//2-1][tile_len//2:tile_len+tile_len//2]]
            for i in range(tile_len//2-1):
                calculated_four_tuple.insert(0, complete_nw[tile_len+tile_len//2-i-2][tile_len//2+i+1:tile_len+tile_len//2-i-1])
                calculated_four_tuple.append(complete_nw[tile_len+tile_len//2+i][tile_len//2+i+1:tile_len+tile_len//2-i-1])
            expected_tuple=tiles_by_index[tup[3]]
            if (expected_tuple!=calculated_four_tuple):
                # Mismatch between computed four-tuple and expected four-tuple
                for error in incomplete_nw:
                    print(error)
                if calculated_four_tuple in tiles_by_index:
                    print('index of calculated four tuple =')
                    print(tiles_by_index.index(calculated_four_tuple))
                else:
                    print('calculated four tuple not a tile')
                    print(calculated_four_tuple)
                return [False, expected_tuple, calculated_four_tuple]
        count += 1
    # Return true here only triggers if no mismatches have been found in the entire set.
    return [True]

# Below are multiple helper functions that support the four primary
# algorithm computation functions.

# Function to split full image 4-tuple into constituent parts    
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
    complete_nw=nw_from_tuple(incomplete_nw, prime)
    # Extract calculated lower tile
    calculated_four_tuple=[complete_nw[tile_len+to2m1][to2:tile_len+to2]]
    for i in range(to2m1):
        calculated_four_tuple.insert(0, complete_nw[tile_len+to2-i-2][to2+i+1:tile_len+to2m1-i])
        calculated_four_tuple.append(complete_nw[tile_len+to2+i][to2+i+1:tile_len+to2m1-i])
    return calculated_four_tuple

# Function to merge 4 image tiles into a full 4-tuple
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

# Generates the lower tile based on the three tiles above it
# This version of the function works for any row other than row 0
# Imported from Version3Plus
### CLARIFY DIFFERENCE BETWEEN THIS AND NW_FROM_TUPLE
def tile_gen(left_tile: TO.Tile, upper_tile: TO.Tile, right_tile: TO.Tile, prime: int):
    tile_len=TO.Tile.tile_length
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
    complete_nw=nw_from_tuple(incomplete_nw, prime)
    # Extract calculated lower tile
    output_tile_val=[complete_nw[tile_len+tile_len//2-1][tile_len//2:tile_len+tile_len//2]]
    for i in range(tile_len//2-1):
        output_tile_val.insert(0, complete_nw[tile_len+tile_len//2-i-2][tile_len//2+i+1:tile_len+tile_len//2-i-1])
        output_tile_val.append(complete_nw[tile_len+tile_len//2+i][tile_len//2+i+1:tile_len+tile_len//2-i-1])
    complete_nw=[]
    return output_tile_val

# Generates the 4th tile (lower tile) of a section of number wall
# using the three tiles above. Calls nw_entry function
# for calculation logic on each cell.
def nw_from_tuple(incomplete_nw, prime):
    tile_len=len(incomplete_nw[0])//2
    # Top half of tile
    for i in range(1, tile_len//2+1):
        for j in range(2*i):
            row=tile_len+i-1
            col=tile_len-i+j
            incomplete_nw[row][col]=nw_entry(incomplete_nw, row, col, prime)
    # Bottom half of tile
    for i in range(1, tile_len//2):
        for j in range(tile_len-2*i):
            row=tile_len+tile_len//2+i-1
            col=tile_len//2+j+i
            incomplete_nw[row][col]=nw_entry(incomplete_nw, row, col, prime)
    return incomplete_nw

# Calculates number wall entry for a single cell.
# Doesn't currently include full cheat list for window frame constraints
# Potential future improvement..
def nw_entry(nw, row, col, prime):
    # Case zero - inside window
    if(nw[row-1][col]==0 and nw[row][col-1]==0):
        return 0
    # Case 1 - non-window (standard wall entry)
    elif(nw[row-2][col]!=0):
        result=(((nw[row-1][col]**2)-(nw[row-1][col-1]*nw[row-1][col+1]))*CF.div(nw[row-2][col], prime))%prime
        return result
    # Case 2 - inner window frame
    elif(nw[row-2][col]==0 and nw[row-1][col]==0):
        current=0
        diagB=0
        while(current==0):
           diagB += 1
           current=nw[row-diagB][col-diagB]
        B=current
        current=0
        diagA=0
        while(current==0):
            diagA += 1
            current=nw[row-diagB-diagA][col-diagB+diagA]
        A=current
        C=nw[row-diagA][col+diagA]
        length=diagA+diagB-1
        k=diagA
        return ((((-1)**(length*k))*B*C)*CF.div(A, prime))%prime
    # Case 3 - outer window frame
    else:
        current=0
        diagB=0
        while(current==0):
           diagB += 1
           current=nw[row-1-diagB][col-diagB]
        B=current
        F=nw[row-1-diagB][col-1-diagB]
        rB=(B*CF.div(nw[row-2-diagB][col-diagB],prime))%prime
        current=0
        diagA=0
        while(current==0):
            diagA += 1
            current=nw[row-1-diagB-diagA][col-diagB+diagA]
        A=current
        E=nw[row-2-diagB-diagA][col-diagB+diagA]
        rA=(A*CF.div(nw[row-1-diagB-diagA][col-1-diagB+diagA], prime))%prime
        C=nw[row-1-diagA][col+diagA]
        G=nw[row-1-diagA][col+diagA+1]
        rC=(C*CF.div(nw[row-1-diagA+1][col+diagA], prime))%prime
        length=diagA+diagB-1
        k=diagA
        D=nw[row-1][col]
        rD=(D*CF.div(nw[row-1][col+1], prime))%prime
        calc1=(rB*E*CF.div(A, prime))%prime
        calc2=(((-1)**k)*(rA*F*CF.div(B, prime)))%prime
        calc3=(((-1)**k)*(rD*G*CF.div(C, prime)))%prime
        calc4=(rC*CF.div(D, prime))%prime
        return ((calc1+calc2-calc3)*CF.div(calc4, prime))%prime

# Steven please define this function
def find_sub_rules(seq):
    length = 0 # 2**length is the length of the tile
    while length >= 0:
        maps = [] # these are the substitution rules
        for i in range(len(seq)//(2**(length+1))):
            # generate new map
            new_map = [[seq[i* 2**length + j] for j in range(2**length)]\
                     ,[seq[i* 2**(length+1) + j] for j in range(2**(length+1))]]
            if new_map not in maps:
                check = False
                for j in maps:
                    # check if new_map is inconsistant with existing maps
                    if j[0] == new_map[0]:
                        check = True
                        break
                if check == False:
                    maps.append(new_map)
                else: # if new_map was inconsistant, increase length by 1 and restart
                    length += 1
                    break
        if check == False:
            return maps

# Function to generate the sub_rules and the coding that governs the sequence
def maps_to_sub_rules(maps):
    sub_rules = []
    tiles = [i[0] for i in maps]
    coding = []
    for i in range(1,len(maps)+1):
        rule = [i,[]]
        length = len(maps[i-1][1])//2
        left_image = maps[i-1][1][:length]
        right_image = maps[i-1][1][length:]
        rule[1].append(tiles.index(left_image)+1)
        rule[1].append(tiles.index(right_image)+1)
        sub_rules.append(rule)
        coding.append([i,tiles[i-1]])
    return sub_rules, coding

# Function to apply the sub_rules and coding until the tiles are of desired length
def apply_coding(sub_rules, coding):
    large_coding = []
    for i in range(len(sub_rules)): # for each sub_rule
        rule = [i+1]
        image = sub_rules[i][1]
        while len(image)<TO.Tile.tile_length//(len(coding[0][1])):
            # apply sub_rules and coding until the image is long enough
            new_image = []
            for k in image:
                new_image.append(sub_rules[k-1][1][0])
                new_image.append(sub_rules[k-1][1][1])
            image = new_image
        code = []
        for j in image:
            for k in range(len(coding[0][1])):
                code.append(coding[j-1][1][k])
        rule.append(code)
        large_coding.append(rule)
    return large_coding

# Function to invoke all sub-functions and return resultant substitution rules
def sub_rule_full(seq):
    maps = find_sub_rules(seq)
    sub_rules, coding = maps_to_sub_rules(maps)
    large_coding = apply_coding(sub_rules, coding)
    return sub_rules, large_coding

def seconds_to_hours(total_time):
    minutes=total_time//60
    seconds=total_time%60
    hours=minutes//60
    minutes=minutes%60
    return 'Total time = '+str(hours)+' hours, '+str(minutes)+' minutes and '+str(seconds)+' seconds.' 
    
# Primary testing function.
def main():
    prime=3 # Currently tested with (pf) 3, 7, 11 and (apf) 5.
    TO.Tile.tile_length=8 # Set tile length from sequence coding
    TO.Tile.tile_prime=prime # Set the prime to be used in the program, to save passing the parameter to every function
    seq=[CF.pap_f(i) for i in range(0,500)] # Set the exact sequence to use, can be:
    # 'CF.pap_f' for Paper Folding sequence  OR  'CF.pap_f5' for Adapted Paper Folding sequence
    write_output = False # Instructs the progress reports to be written to disk as well as std-out
    start=time.time()
    print("Tiling Test with mod", prime, "and tile length", TO.Tile.tile_length)
    tiling_output=input_generator(seq, write_output) # Algorithm 1.1: Initial Conditions
    # This function also automatically calls Algorithm 1.2: Generating the Complete Set of Tiles
    tiling_time=time.time()
    print("- Tiling time =", tiling_time-start)
    print("Total number of unique tiles:", len(tiling_output))
    tuple_start=time.time()
    unique_tuples=generate_four_tuples(tiling_output) # Algorithm 2.1: Generating all possible 4-tuples
    print('Number of unique four-tuples =', len(unique_tuples))
    tuple_end=time.time()
    print("- Tuple time =", tuple_end-tuple_start)
    verify_start=time.time()
    proof=verify_four_tuples(unique_tuples, tiling_output, write_output) # Algorithm 2.2: Verifying the 4-tuples
    verify_end=time.time()
    print("- Verify time =", verify_end-verify_start)
    print("Proof result =", proof[0])
    end=time.time()
    print(seconds_to_hours(end-start))
    if(proof[0]==False):
        print("Expected:", proof[1])
        print("Calculated:", proof[2])
    return tiling_output

output=main()