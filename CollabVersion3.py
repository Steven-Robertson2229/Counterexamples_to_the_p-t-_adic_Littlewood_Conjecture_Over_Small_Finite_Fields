import time
import random as rn
import copy as cop

# This python file is the Version 3 of the Number Wall tiling functionality.
# It comes with the CommonFunctions.py code built-in.

def ratio(X, Y, prime):
   return (X*div(Y, prime)) % prime

# Note: this only works with prime 2, 3, 5, 7, 11, and 19
def div(num, prime):
    num=num%prime
    if prime==2:
        return 1
    elif prime==3:
        if num==1:
            return 1
        else: # num==2:
            return 2
    elif prime==5:
        if num==1:
            return 1
        elif num==2:
            return 3
        elif num==3:
            return 2
        else: # num==4:
            return 4
    elif prime==7:
        if num==1:
            return 1
        elif num==2:
            return 4
        elif num==3:
            return 5
        elif num==4:
            return 2
        elif num==5:
            return 3
        else: # num==6:
            return 6
    elif prime==11:
        if num==1:
            return 1
        elif num==2:
            return 6
        elif num==3:
            return 4
        elif num==4:
            return 3
        elif num==5:
            return 9
        elif num==6:
            return 2
        elif num==7:
            return 8
        elif num==8:
            return 7
        elif num==9:
            return 5
        else: # num==10:
            return 10
    else: # prime==19:
        if num==1:
            return 1
        elif num==2:
            return 10
        elif num==3:
            return 13
        elif num==4:
            return 5
        elif num==5:
            return 4
        elif num==6:
            return 16
        elif num==7:
            return 11
        elif num==8:
            return 12
        elif num==9:
            return 17
        elif num==10:
            return 2
        elif num==11:
            return 7
        elif num==12:
            return 8
        elif num==13:
            return 3
        elif num==14:
            return 15
        elif num==15:
            return 14
        elif num==16:
            return 6
        elif num==17:
            return 9
        else: # num==18:
            return 18

    # otherwise it was a bad input
    print("ERROR - bad input to div function.")
    print("Input: ", prime)
    return "ERROR"

# Function to grow an already existing Number Wall (prev_wall)
# Note: when inputting a starting wall to wall_gen, add two additional
# 1's to prev_wall row 1 to avoid an edge case bug in the top row
def wall_gen(prime, prev_wall, new_num):
    # only add rows if row 0 has odd length
    if (len(prev_wall[0])%2==0):
        prev_wall.append([])
    # skip '-2' and above rows
    # row -1 rule
    prev_wall[0].append(0)
    prev_wall[1].append(1)
    # row 0 rule, apply sequence
    prev_wall[2].append(new_num)
    for row in range(3, len(prev_wall)):
        cheat=True
        if row==len(prev_wall)-1:
            cheat=False
        # cheat rules are more efficient computations that can only
        # be used under specific scenarios
        if cheat:
            # window rule - cheat rule
            if ((prev_wall[row-1][-2]==0) and (prev_wall[row][-1]==0)):
                prev_wall[row].append(0)
            #narrow window frame rule 1 - cheat rule
            elif ((prev_wall[row-2][-4]==0) and (prev_wall[row-1][-2]==0) and (prev_wall[row][-1]!=0)):
                x = prev_wall[row][-1]
                y = prev_wall[row][-2]
                output=((x*div(y,prime))*x) % prime
                prev_wall[row].append(output)
            #narrow window frame rule 2 - cheat rule
            elif ((prev_wall[row-2][-4]!=0) and (prev_wall[row-1][-2]==0) and (prev_wall[row][-1]!=0)):
                B=prev_wall[row-1][-3]
                length=0
                current=0 # non-null
                while current==0:
                    length += 1
                    current = prev_wall[row-1-length][-2]
                A=prev_wall[row-1-length][-3]
                C=prev_wall[row-length][-1]
                output=-1
                if C==0:
                    output=0
                else:
                    output=((((-1)**(length**2))*B*C)*div(A,prime)) % prime
                prev_wall[row].append(output)
            else:
                cheat=False
        # the regular rules are more computationally expensive
        # and are roughly ordered by increasing computation cost
        if not cheat:
            # frame constraint 2
            if prev_wall[row-1][-2]==0 and prev_wall[row-2][-3]==0:
                current=0
                diagA=0
                diagB=0
                # Find B
                while (current==0):
                    diagB += 1
                    current=prev_wall[row-diagB][-1-(diagB*2)]
                B=current
                # Find A
                current=0
                if prev_wall[row-diagB][-diagB*2]!=0:
                    output=0
                else:
                    while (current==0):
                        diagA += 1
                        current=prev_wall[row-diagB-diagA][-1-(diagB*2)]
                    A=current
                    # Find C
                    C=prev_wall[row-diagA][-1]
                    # Find additionals
                    length=diagA+diagB-1
                    k=diagA
                    if C==0:
                        output=0
                    else:
                        output=((((-1)**(length*k))*B*C)*div(A,prime)) % prime
                prev_wall[row].append(output)
            # regular rule - frame constraint 1
            elif (prev_wall[row-2][-3]!=0):
                a=prev_wall[row-2][-3]
                x=prev_wall[row-1][-2]
                c=prev_wall[row-1][-3]
                d=prev_wall[row-1][-1]
                output=(((x**2)-(c*d))*div(a, prime)) % prime
                prev_wall[row].append(output)
            # outer frame rule - frame constraint 3
            else:
                # Find D
                D=prev_wall[row-1][-2]
                d=prev_wall[row-1][-1]
                Rd=ratio(D, d, prime)
                current=0
                diagA=0
                diagB=0
                # Find B
                while (current==0):
                    diagB += 1
                    current=prev_wall[row-1-diagB][-2-(diagB*2)]
                B=current
                F=prev_wall[row-1-diagB][-3-(diagB*2)]
                b=prev_wall[row-2-diagB][-3-(diagB*2)]
                Rb=ratio(B, b, prime)
                # Find A
                current=0
                while (current==0):
                    diagA += 1
                    current=prev_wall[row-1-diagB-diagA][-2-(diagB*2)]
                A=current
                E=prev_wall[row-2-diagB-diagA][-3-(diagB*2)]
                a=prev_wall[row-1-diagB-diagA][-3-(diagB*2)]
                Ra=ratio(A, a, prime)
                # Find C
                C=prev_wall[row-1-diagA][-2]
                G=prev_wall[row-1-diagA][-1]
                c=prev_wall[row-diagA][-1]
                Rc=ratio(C, c, prime)
                # Find additionals
                length=diagA+diagB-1
                k=diagA
                calc1=(Rb*E)*div(A, prime)
                calc2=((-1)**k)*((Ra*F)*div(B, prime))
                calc3=((-1)**k)*((Rd*G)*div(C, prime))
                calc4=div(Rc*(div(D, prime)),prime)
                output=((calc1+calc2-calc3)*(calc4))%prime
                prev_wall[row].append(output)

    return prev_wall    
    
# Test version of the method that also built a full Number Wall
# alongside the slice, to allow for easy comparison
def slice_gen_test(prime, prev_slice, new_nums, full_nw):
    tile_len=len(new_nums)
    new_slice=[]
    # adds padding to input to avoid edge case bug in wall_gen
    prev_slice[0].append(0)
    prev_slice[0].append(0)
    prev_slice[1].append(1)
    prev_slice[1].append(1)
    # generate new slice using old slice
    for input_num in new_nums:
        prev_slice=wall_gen(prime, prev_slice, input_num)
    # cut off old slice
    offset=(tile_len//2)-1
    for i in range(len(prev_slice)-offset):
        new_slice.append(prev_slice[i][-tile_len:])
    for i in range(offset):
        new_slice.append(prev_slice[-offset+i])
        full_nw.append([])
    full_nw.append([])
    for i in range(len(new_slice)):
        full_nw[i]=full_nw[i]+new_slice[i]
    return new_slice, full_nw

# Generates the last 'x' number of reverse columns of the Number
# Wall, where 'x' is the length of new_nums
def slice_gen(prime, prev_slice, new_nums):
    tile_len=len(new_nums)
    new_slice=[]
    # adds padding to input to avoid edge case bug in wall_gen
    prev_slice[0].append(0)
    prev_slice[0].append(0)
    prev_slice[1].append(1)
    prev_slice[1].append(1)
    # generate new slice using old slice
    for input_num in new_nums:
        prev_slice=wall_gen(prime, prev_slice, input_num)
    # cut off old slice
    offset=(tile_len//2)-1
    for i in range(len(prev_slice)-offset):
        new_slice.append(prev_slice[i][-tile_len:])
    for i in range(offset):
        new_slice.append(prev_slice[-offset+i])
    return new_slice

# Function returns the nth element of the paper folding sequence
def pap_f(n):
    n += 1
    if n == 0:
        return 0
    else:
        while n%2 == 0:
            n = n / 2
    return int(((n-1)/2)%2)

# Function returns the nth element of the adapted paper folding sequence (for F5)
def pap_f5(n):
    n += 1
    if n == 0:
        return 0
    while n-(n//2)*2 == 0:
        n=n//2
    if int(n)%8 == 1:
        return 0
    elif int(n)%8 == 3:
        return 1
    elif int(n)%8 == 5:
        return 2
    else:
        return 3

# Function returns the nth element of the pagoda sequence
def pagoda(n):
    return pap_f(n+1) - pap_f(n-1)

# Todo:
    # - Add logic into tiling loop to only collate the tile if it is in the 
    #   new tile dict (otherwise it is simply already a tile we have!)
    # - (In progress) Add logic to generate tile->image mapping dict
# Function records all unique tiles and tile->image mappings for a
# given tile length, prime, and Number Wall sequence
# Note: This function is designed around the centre of tiles on row 0
# being the input row 1 above the input sequence
def tiling(prime, seq, tile_len):
    # Generate first slice
    prev_wall=[[0,0],[1,1,1,1],[seq(0),seq(1)]]
    for i in range(2, tile_len-2):
        prev_wall=wall_gen(prime, prev_wall, seq(i)%prime)
    current_slice=prev_wall
    slice_count=1
    growth_marker=1
    tiles={}
    tiles_by_index=[]
    maps={}
    new_tiles={}
    col=0
    row=0
    # Hard code 0th tile
    tile0=[]
    tile0.append([0 for i in range(tile_len)])
    for i in range(((tile_len-2)//2)):
        tile0.insert(0, [0 for j in range((tile_len-2)-(2*i))])
        tile0.append([0 for j in range((tile_len-2)-(2*i))])
    key0=str(tile0)
    tiles[key0]=(tile0, 0)
    tiles_by_index.append([tile0,(-1,-1)])
    # Map structure - key=location; value=(parent tile index, image tile a index, ...)
    maps[(-1,-1)]=[tiles[key0][1],tiles[key0][1],tiles[key0][1],tiles[key0][1]]
    # Hard code first tile
    tile1=cop.deepcopy(prev_wall)
    for i in range(((tile_len-2)//2)-1):
        tile1.insert(0, [0 for j in range((tile_len-4)-(2*i))])
    key1=str(tile1)
    tiles[key1]=(tile1, 1) # Add to tiles
    tiles_by_index.append([tile1,(0,0)])
    # Map structure - key=location; value=(parent tile index, image tile a index, ...)
    maps[(0,0)]=[tiles[key1][1],tiles[key1][1],tiles[key0][1],-1,-1] # -1 implies a missing image tile index
    # Add images to dictionary of tiles that should be processed, where the value implies the following:
    # 1 = left image tile
    # 2 = upper image tile
    # 3 = right image tile
    # 4 = bottom image tile
    new_tiles[(0,1)]=3
    new_tiles[(1,0)]=4
    # Tracker for number of tiles generated
    tiles_gen=0
    # Loop over all slices until all new tiles found
    while(slice_count<growth_marker*2):
        current_slice=slice_gen(prime, current_slice, [seq(i)%prime for i in range((slice_count*tile_len)-2, ((slice_count+1)*tile_len)-2)])
        slice_count += 1
        # progress tracker print statement
        if(slice_count%50==0):
            print("Slice count:", slice_count,"- Unique tiles:", len(tiles), "- Processed tiles:", tiles_gen)
        col=slice_count-1
        row=0
        for i in range(slice_count):
            new_tile=[]
            # Does tile (row, col) appear in new_tiles list
            image_tile=new_tiles.get((row,col))
            if(image_tile!= None):
            # If yes, generate tiling, check uniqueness, find parent tile to add index to mapping, and remove from new_tiles
            # If no, skip
                tiles_gen += 1
                # Specific logic for the top row tiling
                if(row==0):
                    new_tile.append(cop.deepcopy(current_slice[1]))
                    for j in range((tile_len-2)//2):
                        new_tile.insert(0, [0 for k in range(tile_len-2-2*j)])
                        new_tile.append(current_slice[2+j][-(tile_len-2-2*j):])
                # All other row tilings
                else:
                    new_tile.append(cop.deepcopy(current_slice[1+i*(tile_len//2)]))
                    for j in range((tile_len-2)//2):
                        new_tile.insert(0, current_slice[i*(tile_len//2)-j][:(tile_len-2-2*j)])
                        new_tile.append(current_slice[2+i*(tile_len//2)+j][-(tile_len-2-2*j):])
                # Check if tile is new/unique
                key=str(new_tile)
                unique=tiles.get(key)
                tile_index=len(tiles)
                if not unique: # If tile not in tiles dict
                    tiles[key]=(new_tile,tile_index) # Add to tiles
                    tiles_by_index.append([new_tile,(row,col)])
                    growth_marker=slice_count
                    # Also add (row,col) to maps dict, and record location of image tiles
                    if(row==0): # If we're on the top row, the upper image tile will be a zero tile
                        maps[(row,col)]=[tile_index,-1,0,-1,-1]
                    else:
                        maps[(row,col)]=[tile_index,-1,-1,-1,-1]
                        new_tiles[(row*2-1,col*2+1)]=2 # Upper image tile
                    new_tiles[(row*2,col*2)]=1 # Left image tile
                    new_tiles[(row*2,col*2+1)]=3 # Right image tile
                    new_tiles[((row*2)+1,(col*2))]=4 # Lower image tile
                # Compute parent tile co-ordinates
                image_row=row
                image_col=col
                # Adjust co-ordinates (no action for image tile 1's)
                if(image_tile==2):
                    image_row += 1
                    image_col -= 1
                elif(image_tile==3):
                    image_col -= 1
                elif(image_tile==4):
                    image_row -= 1
                else: # Error case
                    if(image_tile!=1):
                        print("IMAGE MAPPING ERROR")
                        print("Image tile numer:", image_tile)
                parent_row=image_row//2
                parent_col=image_col//2
                # Update parent tile mapping with image tile index
                maps[(parent_row, parent_col)][image_tile]=tiles[key][1] # tile_index
                # Remove completed tile from the dict of unprocessed image tiles
                new_tiles.pop((row,col)) # Skip to save computation time?
            # Increment row and decrement col here
            row += 1
            col -= 1
    print("Number of unique tiles:", len(tiles))
    print("Number of generated tiles:", tiles_gen)
    print("Tiles unmapped (expected=0):", len(new_tiles))
    if len(new_tiles)>1:
        for key, val in new_tiles.items():
            print("Tile", key, "from position", val)
    print("Number of unique mappings:", len(maps))
    for mapping, images in maps.items():
        for i in images:
            if(i==-1):
                print("MISSED MAPPING")
                print("Tile:", mapping, "with image indexes:", images)
                break
    cell_count=slice_count*tile_len
    print("Number Wall length (tiles):", slice_count, "and (cells):", cell_count)
    return tiles, maps, tiles_by_index, cell_count

# Function to convert the output of tiling to something more useful, with inputs:
# tiles -> a dictionary containing key = str(tile) and value = (tile, tile_index)
# maps -> a dictionary containing key = (tile_row, tile_col) and value = [parent_tile_index,
#         left_image_tile_index, upper_image_tile_index, right_image_tile_index, lower_image_tile_index]
# tiles_by_index -> a list containing items of form [tile, (tile_row, tile_col)] in tile_index order
# Convert the combination of information above into whatever format is most useful!

# Returns a list of every tile and a list of the images of each tile under the mapping
# The index of the tile is given by its index in the list. For example,
# The images of tile 3 is item 3 in the maps_by_index list
def convert_tiling(tiles, maps, tiles_by_index):
    maps_by_index=[]
    for i in tiles_by_index:
        maps_by_index.append(maps[i[1]][1:])
        i.remove(i[1])
    maps_by_index[0].append(0)
    maps_by_index[2][1]=0
    return tiles_by_index, maps_by_index

# Generates the 'number wall' using only the substitution rule and
# checks if it agrees with the real number wall. Does this for every application
# of the substitution rule
# Inputs are a list of tiles, a list of their images under the substutituion,
# the sequence we are generating the number wall for, the prime we are reducing modulo
# and the number of times the substituition should be applied
def pseudo_number_wall(tiles_by_index,maps_by_index,seq,prime,input_length):
    tiling=[[1]] # Initial tiling
    # Check against a number wall double the size used to generate the substitution rules
    verification_multiplier=input_length*2
    k=0
    while((2**(k+3))<verification_multiplier):
        # Reset number wall variables to save memory
        nw=[]
        true_nw=[]
        # Generate a new tiling
        new_tiling=[]
        for i in range(2*len(tiling[0])):
            # Create shape of new tiling
            new_tiling.insert(0,['*' for j in range(i+1)])
        # Add a dump row as row -1
        new_tiling.append(['*' for j in range(2*len(tiling[0])+1)])
        # Fill in new tiling using maps
        for i in range(len(tiling)):
            for j in range(len(tiling[i])):
                new_tiling[2*i][2*j]=maps_by_index[tiling[i][j]][0]
                new_tiling[2*i-1][2*j+1]=maps_by_index[tiling[i][j]][1]
                new_tiling[2*i][2*j+1]=maps_by_index[tiling[i][j]][2]
                new_tiling[2*i+1][2*j]=maps_by_index[tiling[i][j]][3]
        new_tiling.remove(new_tiling[-1])
        tiling=cop.deepcopy(new_tiling)
        # Build the number wall
        tile_len=len(tiles_by_index[0][0])+1
        t2=tile_len//2
        # Number wall shape
        for i in range((len(new_tiling[0])*tile_len)//2):
            nw.insert(0,['*' for p in range(2*i+2)])
        # Dump rows for rows -1,-2,-3
        for i in range(tile_len//2 -1):
            nw.append(['*' for p in range(len(new_tiling[0])*tile_len)])
        # Fill in the number wall
        for i in range(len(new_tiling)):
            for j in range(len(new_tiling[i])):
                index=new_tiling[i][j]
                tile=tiles_by_index[index][0]
                for l in range(tile_len):
                    nw[t2*i][tile_len*j+l]=tile[t2-1][l]
                for m in range(t2-1):
                    for l in range(tile_len-2-2*m):
                        nw[t2*i-1-m][tile_len*j+l+2*m+2]=tile[t2-2-m][l]
                        nw[t2*i+1+m][tile_len*j+l]=tile[t2+m][l]
         # Remove dump rows
        for i in range(t2-1):
            nw.remove(nw[-1])
        # Build the true number wall
        true_nw=[[0,0],[1,1,1,1],[seq(0),seq(1)]]
        for i in range(2, tile_len*len(new_tiling[0])-2):
            true_nw=wall_gen(prime, true_nw, seq(i)%prime)
        true_nw.remove(true_nw[0])
        # Compare true and pseudo number wall
        if nw!=true_nw: 
            print(k)
            break
        else:
            print('pseudo number wall matches true number wall at length =', 2**(k+3))
        k += 1
    print("Verification complete!")

# Finds all unique four-tuples from our generated mappings.
def four_tuples(maps):
    # Build dict of unique images
    unique_tuples={}
    for tup1 in maps:
        key=str(tup1)
        unique_tuples[key]=tup1
    # For each mapping, check the unknown tuple combinations for new tuples
    # Skip first entry, its all zeros
    for tup in maps[1:]:
        skip=False
        # Take care when zero tiles are present
        if(tup[1]==0):
            skip=True
        # Treat four tuple rotated as a square
        image_tuple=[['*' for i in range(4)] for j in range(4)]
        entry_image1=maps[tup[0]]
        entry_image2=maps[tup[1]]
        entry_image3=maps[tup[2]]
        entry_image4=maps[tup[3]]
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
        if not skip:
            # When zero tiles exist, don't check the upper and right tuples
            new_tuples.append([image_tuple[0][1],image_tuple[0][2],image_tuple[1][2],image_tuple[1][1]]) # Upper tuple
            new_tuples.append([image_tuple[1][2],image_tuple[1][3],image_tuple[2][3],image_tuple[2][2]]) # Right tuple
        new_tuples.append([image_tuple[1][0],image_tuple[1][1],image_tuple[2][1],image_tuple[2][0]]) # Left tuple
        new_tuples.append([image_tuple[2][1],image_tuple[2][2],image_tuple[3][2],image_tuple[3][1]]) # Bottom tuple
        new_tuples.append([image_tuple[1][1],image_tuple[1][2],image_tuple[2][2],image_tuple[2][1]]) # Middle tuple
        # Check each new tuple for uniqueness
        for new_tup in new_tuples:
            key=str(new_tup)
            unique=unique_tuples.get(key)
            if not unique: # If tuple not in tuples dictionary
                unique_tuples[key]=new_tup # Add to tuples dictionary
                maps.append(new_tup)
    return maps

# Uses number wall calculations to generate the lower tile of
# a four-tuple, and compares to our expected four-tuple's lower tile.
def verify_tuples(tuples_by_index, tiles_by_index, tiles, prime):
    tile_len=len(tiles_by_index[0][0])+1
    index=0
    tuples_num=len(tuples_by_index)//4
    print_helper=1
    for tup in tuples_by_index[1:]:
        # Add print block for progress
        if(index==(tuples_num*print_helper)):
            print("Verification process at", 25*print_helper,"% complete!")
            print_helper += 1
        if(tup[1]==0):
            pass
        else:
            incomplete_nw=[['*' for i in range(2*tile_len)] for j in range(2*tile_len-1)]
            # Left tile
            middle=(len(incomplete_nw)-1)//2
            tile=tiles_by_index[tup[0]][0]
            tile_it=tile_len//2 -1
            for i in range(tile_len):
                incomplete_nw[middle][i]=tile[tile_it][i]
            for i in range(tile_it):
                for j in range(tile_len-2-2*i):
                    incomplete_nw[middle-i-1][1+j+i]=tile[tile_it-1-i][j]
                    incomplete_nw[middle+1+i][1+i+j]=tile[tile_it+1+i][j]
            # Right tile
            tile=tiles_by_index[tup[2]][0]
            for i in range(tile_len):
                incomplete_nw[middle][i+tile_len]=tile[tile_it][i]
            for i in range(tile_it):
                for j in range(tile_len-2-2*i):
                    incomplete_nw[middle-i-1][1+j+i+tile_len]=tile[tile_it-1-i][j]
                    incomplete_nw[middle+1+i][1+i+j+tile_len]=tile[tile_it+1+i][j]
            # Upper tile
            tile=tiles_by_index[tup[1]][0]
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
            expected_tuple=tiles_by_index[tup[3]][0]
            if (expected_tuple!=calculated_four_tuple):
                # Mismatch between computed four tuple and expected four tuple
                return [False, expected_tuple, calculated_four_tuple]
        index += 1
    return [True]
        
# Generates the 4th tile of a section of number wall
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
# Doesn't currently include full cheat list
# Potential future improvement?
def nw_entry(nw, row, col, prime):
    # Case zero
    if(nw[row-1][col]==0 and nw[row][col-1]==0):
        return 0
    # Case 1
    elif(nw[row-2][col]!=0):
        result=(((nw[row-1][col]**2)-(nw[row-1][col-1]*nw[row-1][col+1]))*div(nw[row-2][col], prime))%prime
        return result
    # Case 2
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
        return ((((-1)**(length*k))*B*C)*div(A, prime))%prime
    # Case 3
    else:
        current=0
        diagB=0
        while(current==0):
           diagB += 1
           current=nw[row-1-diagB][col-diagB]
        B=current
        F=nw[row-1-diagB][col-1-diagB]
        rB=(B*div(nw[row-2-diagB][col-diagB],prime))%prime
        current=0
        diagA=0
        while(current==0):
            diagA += 1
            current=nw[row-1-diagB-diagA][col-diagB+diagA]
        A=current
        E=nw[row-2-diagB-diagA][col-diagB+diagA]
        rA=(A*div(nw[row-1-diagB-diagA][col-1-diagB+diagA], prime))%prime
        C=nw[row-1-diagA][col+diagA]
        G=nw[row-1-diagA][col+diagA+1]
        rC=(C*div(nw[row-1-diagA+1][col+diagA], prime))%prime
        length=diagA+diagB-1
        k=diagA
        D=nw[row-1][col]
        rD=(D*div(nw[row-1][col+1], prime))%prime
        calc1=(rB*E*div(A, prime))%prime
        calc2=(((-1)**k)*(rA*F*div(B, prime)))%prime
        calc3=(((-1)**k)*(rD*G*div(C, prime)))%prime
        calc4=(rC*div(D, prime))%prime
        return ((calc1+calc2-calc3)*div(calc4, prime))%prime
    
# Primary testing function.
def main():
    # Input variables
    prime_input=3 # Currently tested with (pf) 3, 7, 11, and (apf) 5, and (pag) 3
    tile_length=8 # Currently tested with 8 and 16 length
    sequence=pap_f # Currently pap_f, pap_f5, or pagoda
    # Naive tiling verify
    bad_verify=False
    # Official proof tiling verify
    true_verify=True
    start=time.time()
    print("Tiling Test with mod", prime_input, "and tile length", tile_length)
    # tiling_output = [tiles_dict, maps_dict, tiles_by_index, cell_count]
    tiling_output = tiling(prime_input, sequence, tile_length)
    tiling_time=time.time()
    print("- Tiling time =", tiling_time-start)
    # converted_tiling = [tiles_by_index, maps_by_index]
    converted_tiling = convert_tiling(tiling_output[0], tiling_output[1], tiling_output[2])
    if(bad_verify):
        length_check=tiling_output[3]
        pseudo_number_wall(converted_tiling[0], converted_tiling[1], sequence, prime_input, length_check)
    if(true_verify):
        tuple_start=time.time()
        unique_tuples=four_tuples(converted_tiling[1])
        print('Number of unique four-tuples =', len(unique_tuples))
        tuple_end=time.time()
        print("- Tuple time =", tuple_end-tuple_start)
        verify_start=time.time()
        proof=verify_tuples(unique_tuples, converted_tiling[0], tiling_output[0], prime_input)
        verify_end=time.time()
        print("Proof result =", proof[0])
        if(proof[0]==False):
            print("Expected:", proof[1])
            print("Calculated:", proof[2])
        print("- Verify time =", verify_end-verify_start)
        end=time.time()
        print("- Full time =",end-start)
        return unique_tuples
    return tiling_output
output=main()


