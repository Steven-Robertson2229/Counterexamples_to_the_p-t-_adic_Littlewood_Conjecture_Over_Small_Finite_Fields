import TileObject as TO
import time
import CommonFunctions as CF
import CollabVersion3 as V3

# Function to find all unique tiles and mappings/substitutions
# following the Version 4 process as defined in the CHANGELOG.md
# This function finds every image tile of every unique tile. Once
# this process is complete, every substitution rule for the number wall
# has been identified.

#Finds all the tile that have entries making up with zeroth row of
#the number wall
def one_up_sub(seq,prime,tile_len):
    #Generate a large portion of the number wall
    prev_wall=[[0],[1],[seq[0]]]
    for i in range(1,len(seq)):
        prev_wall=V3.wall_gen(prime, prev_wall, seq[i])
    tiling=[[],[]]
    tiles=[]
    #split the top row into tiles and check for uniqueness
    for i in range(len(seq)//tile_len):
        new_tile=[[1 for i in range(tile_len)]]
        for j in range(tile_len//2-1):
            row=[]
            zrow=[]
            for k in range(tile_len-2-2*j):
                zrow.append(0)
                row.append(prev_wall[2+j][tile_len*i+k])
            new_tile.append(row)
            new_tile.insert(0,zrow)
        if new_tile not in tiles:
            tiles.append(new_tile)
        tiling[0].append(tiles.index(new_tile))
    #find the second row of tiles and check for uniqueness
    for i in range(len(seq)//tile_len-1):
        second_tile=[[prev_wall[1+tile_len//2][j] for j in range(tile_len*i,tile_len*(i+1))]]
        for j in range(tile_len//2-1):
            urow=[]
            lrow=[]
            for k in range(tile_len-2-2*j):
                urow.append(prev_wall[0+tile_len//2-j][tile_len*i+k+2+2*j])
                lrow.append(prev_wall[2+tile_len//2+j][tile_len*i+k])
            second_tile.append(lrow)
            second_tile.insert(0,urow)
        if second_tile not in tiles:
            tiles.append(second_tile)
        tiling[1].append(tiles.index(second_tile))
    return tiles,tiling

#Version 4 of the tiling algorithm, but using the one up trick
#v3tiles=V3.main()
    
def v4_1_up_apf(seq, prime, tile_len):
    #find tiles making up the zeroth row of the number wall
    row_1_2_tiles,row_1_2_tiling=one_up_sub(seq, prime, tile_len) 
    tiles={}
    new_tiles=[]
    tiles_by_index=[]
    # Instantiate Tile object for the tile f all zeros
    tile0_value=[[0 for i in range(tile_len)]]
    for i in range(tile_len//2 -1):
        tile0_value.insert(0,([0 for i in range(tile_len-2-2*i)]))
        tile0_value.append([0 for i in range(tile_len-2-2*i)])
    true_tile0=TO.Tile(0, tile0_value)
    true_key0=str(tile0_value)
    tiles[true_key0]=(true_tile0)
    tiles_by_index.append(true_tile0)
    tiles[true_key0].update_images(tiles[true_key0],tiles[true_key0],tiles[true_key0],tiles[true_key0])
    # Instantiate Tile object for tiles making up the zeroth row
    # Generate input substitution tiles (top row tiles)
    set1=[4,8]
    set2=[5,9,11,13]
    set3=[6,10]
    set4=[7,12,14,15]
    for i in row_1_2_tiles:
        key=str(i)
        new_tile=TO.Tile(len(tiles),i)
        #if the tiles appear on the second row of tiles, then their scaffolding
        #needs to be calculated also
        if row_1_2_tiles.index(i) in set1:
            new_tile.scaffolding=[tiles_by_index[1],tiles_by_index[0],tiles_by_index[2]]
        elif row_1_2_tiles.index(i) in set2:
            new_tile.scaffolding=[tiles_by_index[2],tiles_by_index[0],tiles_by_index[3]]
        elif row_1_2_tiles.index(i) in set3:
            new_tile.scaffolding=[tiles_by_index[3],tiles_by_index[0],tiles_by_index[4]]
        elif row_1_2_tiles.index(i) in set4:
            new_tile.scaffolding=[tiles_by_index[4],tiles_by_index[0],tiles_by_index[1]]
        tiles[key]=new_tile
        tiles_by_index.append(new_tile)
        #print(new_tile)
    #Due to the second row of tiles containing some of the zeroth row of the
    #number wall, a list is created storing the additional entries of the sequence
    #missing from any tiles on second row
    lis=[[3,0],[3,0],[3,1],[3,0],[3,2],[3,1],[3,3],[3,2],[3,1],[3,3],[3,2],[3,3]]
    # Generate images for top row tiles using substitution rules + zero tile
    for i in range(len(tiles_by_index)):
        #The all zero tile already has its image
        if str(tiles_by_index[i].value)==true_key0:
            pass
        #The tiles that appear on the first row of tiles have their images predefined
        elif tiles_by_index[i].value==row_1_2_tiles[0]:
            #print(tiles_by_index[0])
            tiles[str(tiles_by_index[i].value)].update_images(tiles[str(tiles_by_index[1].value)], tiles[str(tiles_by_index[0].value)],\
                                   tiles[str(tiles_by_index[2].value)], tiles[str(tiles_by_index[5].value)])
        elif tiles_by_index[i].value==row_1_2_tiles[1]:
            #print(tiles_by_index[0])
            tiles[str(tiles_by_index[i].value)].update_images(tiles[str(tiles_by_index[3].value)], tiles[str(tiles_by_index[0].value)],\
                                   tiles[str(tiles_by_index[4].value)], tiles[str(tiles_by_index[7].value)])
        elif tiles_by_index[i].value==row_1_2_tiles[2]:
            #print(tiles_by_index[0])
            tiles[str(tiles_by_index[i].value)].update_images(tiles[str(tiles_by_index[1].value)], tiles[str(tiles_by_index[0].value)],\
                                   tiles[str(tiles_by_index[2].value)], tiles[str(tiles_by_index[9].value)])
        elif tiles_by_index[i].value==row_1_2_tiles[3]:
            #print(tiles_by_index[0])
            tiles[str(tiles_by_index[i].value)].update_images(tiles[str(tiles_by_index[3].value)], tiles[str(tiles_by_index[0].value)],\
                                   tiles[str(tiles_by_index[4].value)], tiles[str(tiles_by_index[11].value)])
        #The images for the remaining initital tiles are calculated using the 
        #scaffolding
        else:   
            scaffolding=tiles[str(tiles_by_index[i].value)].scaffolding
            left_scaffold=image_to_tile(scaffolding[0])
            upper_scaffold=image_to_tile(scaffolding[1])
            right_scaffold=image_to_tile(scaffolding[2])
            merged_image=nw_from_scaffold(left_scaffold, upper_scaffold, right_scaffold, prime,0,lis[i-5])
            image=image_split(merged_image) # Returns images as [upper,left,right,lower]
            images=[]
            print(tiles_by_index[i].id-1, tiles_by_index[i].value[0])
            for j in range(len(image)):
                value=image[j]
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
                    
                    if(j == 0): # Upper tile
                        new_tile.scaffolding=[scaffolding[0].right_image, scaffolding[1].lower_image, scaffolding[2].left_image]
                    elif(j == 1): # Left tile
                        new_tile.scaffolding=[scaffolding[0].lower_image, scaffolding[0].right_image, images[0]]
                    elif(j == 2): # Right tile
                        new_tile.scaffolding=[images[0], scaffolding[2].left_image, scaffolding[2].lower_image]
                    elif(j == 3): # Lower tile
                        new_tile.scaffolding=[images[1], images[0], images[2]]
                    else:
                        return "ERROR"
                    unique=new_tile
                images.append(unique)
                # Update the image tiles of the current tile
            tiles[str(tiles_by_index[i].value)].update_images(images[1], images[0], images[2], images[3])
    # Loop through list of tiles (excluding input section)
    # identifying the images of each tile
    # for i in tiles:
    #     print('tile=')
    #     print(tiles[i])
    #     print('scaffolding=')
    #     for j in tiles[i].scaffolding:
    #         print(j)
    print(len(tiles))
    count = 0
    while (new_tiles != []):
        tile=new_tiles.pop(0)
        # if v3tiles.get(str(tile.value))==None:
        #     print(tiles[str(tile.value)], ' not in v3')
        #     print('scaffolding=')
        #     for j in tile.scaffolding:
        #         print(j)
        #     break
            
        if (tile.scaffolding !=-1): # REMOVE******
            scaffolding=tile.scaffolding
            # Generate full image 4-tuples from scaffold tiles
            # to allow all four image tiles of the current tile to
            # be computed in one go.
            left_scaffold=image_to_tile(scaffolding[0])
            upper_scaffold=image_to_tile(scaffolding[1])
            right_scaffold=image_to_tile(scaffolding[2])
            if count==0:
                f=open('progress_tracker_pf_F'+str(prime)+'.txt', 'w')
            if(count%10000 == 0) and count!=0:
                f=open('progress_tracker_pf_F'+str(prime)+'.txt', 'a')
                f.write("Unique tiles: "+ str(len(tiles))+ " - Processed tiles: "+ str(count*4)+  " - Remaining to process: "+ str(len(new_tiles)))
                f.write('\n')
                f.close()
                print("Unique tiles:", len(tiles), "- Processed tiles:", count*4, "- Remaining to process:", len(new_tiles))
            # print('tile=')
            # print(tile)
            # print('scaffolding=')
            # for i in tile.scaffolding:
            #     print(i)
            merged_image=nw_from_scaffold(left_scaffold, upper_scaffold, right_scaffold, prime,count)
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
def nw_from_scaffold(left_scaffold, upper_scaffold, right_scaffold, prime,count,extra=False,idd=0):
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
    complete_nw=V3.nw_from_tuple(incomplete_nw, prime,extra)
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

def four_tuples(tiles):
    maps=[]
    for i in tiles:
        maps.append([tiles[i].left_image.id,tiles[i].upper_image.id,tiles[i].right_image.id,tiles[i].lower_image.id])
   # Build dict of unique images
    unique_tuples={}
    for tup1 in maps:
        key=str(tup1)
        unique_tuples[key]=tup1
    # For each mapping, check the unknown tuple combinations for new tuples
    # Skip first entry, its all zeros
    c=0
    for tup in maps:
        c+=1
        # Take care when zero tiles are present
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

        if tup[1]>1:
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
                #print(new_tup)
    return maps

def verify_tuples(tuples_by_index, tiles, prime):#tiles_by_index, tiles, prime):
    tiles_by_index=[]
    for i in tiles:
        tiles_by_index.append(tiles[i].value)
    tile_len=len(tiles_by_index[0])+1
    index=0
    tuples_num=len(tuples_by_index)//4
    print_helper=1
    count=0
    for tup in tuples_by_index[2:]:
        count+=1
        #print(tup)
        # Add print block for progress
        if(index%1000000==0):
            print("Verification process at", 100*index/len(tuples_by_index),"% complete!")
            f=open('progress_tracker_pf_F'+str(prime)+'.txt', 'a')
            f.write("Verification process at"+ str(100*index/len(tuples_by_index))+"% complete!")
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
            #print(tup)
            #print(incomplete_nw)
            complete_nw=nw_from_tuple(incomplete_nw, prime)
            # Extract calculated lower tile
            calculated_four_tuple=[complete_nw[tile_len+tile_len//2-1][tile_len//2:tile_len+tile_len//2]]
            for i in range(tile_len//2-1):
                calculated_four_tuple.insert(0, complete_nw[tile_len+tile_len//2-i-2][tile_len//2+i+1:tile_len+tile_len//2-i-1])
                calculated_four_tuple.append(complete_nw[tile_len+tile_len//2+i][tile_len//2+i+1:tile_len+tile_len//2-i-1])
            expected_tuple=tiles_by_index[tup[3]]
            if (expected_tuple!=calculated_four_tuple):
                # Mismatch between computed four tuple and expected four tuple
                for l in incomplete_nw:
                    print(l)
                if calculated_four_tuple in tiles_by_index:
                    print('index of calculated four tuple =')
                    print(tiles_by_index.index(calculated_four_tuple))
                else:
                    print('calculated four tuple not a tile')
                    print(calculated_four_tuple)
                return [False, expected_tuple, calculated_four_tuple]
        index += 1
    return [True]
        
# Generates the 4th tile of a section of number wall
# using the three tiles above. Calls nw_entry function
# for calculation logic on each cell.
def nw_from_tuple(incomplete_nw, prime,extra=False,idd=0):
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
def nw_entry(nw, row, col, prime,idd=0):
    # Case zero - inside window
    if(nw[row-1][col]==0 and nw[row][col-1]==0):
        return 0
    # Case 1 - non-window (standard wall entry)
    elif(nw[row-2][col]!=0):
        result=(((nw[row-1][col]**2)-(nw[row-1][col-1]*nw[row-1][col+1]))*CF.div(nw[row-2][col], prime))%prime
        return result
    # Case 2 - inner window frame
    elif(nw[row-2][col]==0 and nw[row-1][col]==0):
        height=0
        current=0
        while current==0:
            height+=1
            current=nw[row-height][col]
        height-=1
        left=0
        current=0
        while current==0:
            left+=1
            current=nw[row-height][col+left]
        left-=1
        right=0
        current=0
        while current==0:
            right+=1
            current=nw[row-height][col-right]
        right-=1
        if idd==218:
            print(left,right,height)
        if left+right+1>height:
            return 0
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
    
def seconds_to_hours(tot_time):
    minutes=tot_time//60
    seconds=tot_time%60
    hours=minutes//60
    minutes=minutes%60
    return 'total time = '+str(hours)+' hours, '+str(minutes)+' minutes and '+str(seconds)+' seconds ' 
    
# Primary testing function.
def main():
    # *_sub_rules is the input substitution rules for tiles on the top row of this sequence
    #pf_sub_rules=[['1','12'],['2','32'],['3','14'],['4','34']]
    #sub_rules=pf_sub_rules # Pick the substitution rules of your desired sequence
    # *_coding is the input sequence split into the size of the input tiles
    #pf_coding=[['1','00100110'],['2','00110110'],['3','00100111'],['4','00110111']]
    #coding=pf_coding # Must match sequence used for sub_rules
    prime=5 # Currently tested with (pf) 3, 7 and (apf) N/A, and (pag) N/A
    TO.Tile.tile_length=16 # Set tile length from sequence coding
    seq=[CF.pap_f5(i) for i in range(0,2000)]
    start=time.time()
    print("Tiling Test with mod", prime, "and tile length", TO.Tile.tile_length)
    tiling_output=v4_1_up_apf(seq,prime,TO.Tile.tile_length)
    tiling_time=time.time()
    print("- Tiling time =", tiling_time-start)
    print("Total number of unique tiles:", len(tiling_output))
    tuple_start=time.time()
    unique_tuples=four_tuples(tiling_output)
    print('Number of unique four-tuples =', len(unique_tuples))
    tuple_end=time.time()
    print("- Tuple time =", tuple_end-tuple_start)
    verify_start=time.time()
    proof=verify_tuples(unique_tuples, tiling_output, prime)
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
    