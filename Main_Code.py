import TileObject as TO
import time

"""
Set of functions to find all unique tiles and mappings/substitutions
following the Version 4 process as defined in the CHANGELOG.md
This function finds every image tile of every unique tile. Once
this process is complete, every substitution rule for the number wall
has been identified.

The various algorithm sections as defined in Section 4 of our paper
(Counterexamples to the p(t)-adic Littlewood Conjecture Over Small Finite Fields)
have been noted at the definition of each related function, as well as in the main
testing function at the bottom of the file.
"""
########################### SEQUENCE GENERATORS ###########################

"""
Function returns the nth element of the paper folding (dragon) sequence
"""
def nth_paperfolding(n):
    if n == 0:
        return 0
    else:
        while n%2 == 0:
            n = n / 2
    return int(((n-1)/2)%2)

"""
Function finds first n digits of paper folding sequence
"""
def paperfolding(start,end):
    ans=[]
    for i in range(start,end+1):
        ans.append(nth_paperfolding(i))
    return ans

"""
Function returns the nth element of the pagoda sequence
"""
def nth_pagoda(n):
    return nth_paperfolding(n+1) - nth_paperfolding(n-1)

"""
Function finds first n digits of pagoda sequence
"""
def pagoda(start,end):
    return [nth_pagoda(i) for i in range(start,end+1)]

"""
Function calculates nth digit of the second level paper folding sequence
"""
def nth_adapted_paperfolding(n):
    if n==0:
        return 0
    while n-(n//2)*2==0:
        n=n//2
    if int(n)%8==1:
        return 0
    elif int(n)%8==3:
        return 1
    elif int(n)%8==5:
        return 2
    else: 
        return 3

"""
Function finds first n digits of the second level paper folding sequence
"""
def adapted_paperfolding(start,end):
    return [nth_adapted_paperfolding(i) for i in range(start,end+1)]


########################### FIND SUBSTITUTION RULES OF GIVEN SEQUENCE ###########################

"""
Function finds 2-morphism and coding of minimal length that generates the input 
sequence. Returns the 2-morphism aftercoding has been applied
"""
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

"""
Function to generate the 2-morphism and the coding from the output of 
find_sub_rules
"""
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

"""
Function to apply the substitution rules and coding until the tiles are of desired length
"""
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

"""
Function to invoke all related helper functions and return resultant substitution rules
"""
def sub_rule_full(seq):
    maps = find_sub_rules(seq)
    sub_rules, coding = maps_to_sub_rules(maps)
    large_coding = apply_coding(sub_rules, coding)
    return sub_rules, large_coding

########################### MODULAR ARTIHMETIC ###########################

def ratio(X, Y, prime):
   return (X*div(Y, prime)) % prime

"""
Function returns the inverse of num!=0 modulo p
"""
# Note: this only works with primes 2, 3, 5, 7, 11, and 19. Furthermore,
# for larger primes, it is more efficient to hard code the inverse than to 
# calculate it 
def div(num, prime):#
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

########################### NUMBER WALL GENERATOR ###########################

"""
Function to grow an already existing Number Wall (prev_wall)
by slices - i.e. one diagonal row of tiles at a time.
I.e. Given a finite number wall generated by a sequence S, and a number (new_num),
this generates the number wall of S union new_num.
Note: when inputting a starting wall to wall_gen, add two additional
1's to prev_wall row 1 to avoid an edge case bug in the top row.
"""
def wall_gen(prime, prev_wall, new_num): 
    # only add rows if row 0 has odd length
    if (len(prev_wall[0])%2==0):
        prev_wall.append([])
    # row -2
    prev_wall[0].append(0)
    # row -1
    prev_wall[1].append(1)
    # row 0 rule, apply sequence
    prev_wall[2].append(new_num)
    for row in range(3, len(prev_wall)):
        cheat=True
        if row==len(prev_wall)-1:
            cheat=False
        # cheat rules are more efficient computations that can only
        # be used in specific scenarios
        if cheat:
            # cheat rule 1 - if entry inside a window
            if ((prev_wall[row-1][-2]==0) and (prev_wall[row][-1]==0)):
                prev_wall[row].append(0)
            # cheat rule 2 - if entry at the start of bottom row of inner frame
            elif ((prev_wall[row-2][-4]==0) and (prev_wall[row-1][-2]==0) and (prev_wall[row][-1]!=0)):
                x = prev_wall[row][-1]
                y = prev_wall[row][-2]
                output=((x*div(y,prime))*x) % prime
                prev_wall[row].append(output)
            # cheat rule 2 - if entry on bottom row of inner frame
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

"""
Generates the 4th tile (lower tile) of a section of number wall using the three tiles above.
Calls nw_entry function for calculation logic on each cell.
"""
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

"""
Calculates number wall entry for a single cell.
Doesn't currently include full cheat list for window frame constraints,
potential future improvement.
"""
def nw_entry(nw, row, col, prime):
    # Case zero - inside window
    if(nw[row-1][col]==0 and nw[row][col-1]==0):
        return 0
    # Case 1 - non-window (standard wall entry)
    elif(nw[row-2][col]!=0):
        result=(((nw[row-1][col]**2)-(nw[row-1][col-1]*nw[row-1][col+1]))*div(nw[row-2][col], prime))%prime
        return result
    # Case 2 - inner window frame
    elif(nw[row-2][col]==0 and nw[row-1][col]==0):
        current=0
        diagB=0
        while(current==0):
           diagB += 1
           current=nw[row-diagB][col-diagB]
        B=current
        if nw[row-diagB][col-diagB+1]!=0:
            return 0
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
    # Case 3 - outer window frame
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
    
########################### FIND SUBSTITUTION RULES OF NUMBER WALL ###########################

"""
***Algorithm 1.1: Initial Conditions***
Function to generate top row tiles of number wall
When it completes, this function automatically calls the tile_computation
function to begin the main tile generating process.
"""
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
    # Instantiate Tile object for the tile of all zeros (Step 1.1.1)
    tile0_value=[[0 for i in range(tile_len)]]
    for i in range(tile_len//2 -1):
        tile0_value.insert(0,([0 for i in range(tile_len-2-2*i)]))
        tile0_value.append([0 for i in range(tile_len-2-2*i)])
    tile0=TO.Tile(0, tile0_value)
    key0=str(tile0_value)
    tiles[key0]=(tile0)
    tiles_by_index.append(tile0)
    tiles[key0].update_images(tile0, tile0, tile0, tile0) # Step 1.1.4
    # Instantiate Tile object for the tile above the input row (Step 1.1.1)
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
    tile1.update_images(tile0,tile0,tile0,tile1) # Step 1.1.4
    # Generate input substitution tiles (top row tiles)
    for i in range(len(sub_rules)): #Step 1.1.2
        prev_wall=[[0],[1],[int(coding[i][1][0])]]
        for j in range(1, tile_len):
            prev_wall=wall_gen(prime, prev_wall, int(coding[i][1][j])%prime)
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
    for i in range(len(sub_rules)): #Step 1.1.3
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

"""
***Algorithm 1.2: Generating the Complete Set of Tiles***
Function to find all unique tiles and mappings/substitutions
following the Version 4 process as defined in the CHANGELOG.md
This function finds every image tile of every unique tile in a given sequence and prime.
Once this process is complete, every substitution rule for the number wall
has been identified.
"""
def tile_computation(tiles, new_tiles, write_output):
    # Loop through list of tiles (excluding input section)
    # identifying the images of each tile
    count=1
    prime=TO.Tile.tile_prime
    if write_output:
        f=open('progress_tracker_F'+str(prime)+'.txt', 'w')
    while (new_tiles != []): #Step 1.2.6 begins. 
        tile=new_tiles.pop(0) # Removes tile from the list, as well as retrieveing it
        if (tile.scaffolding != -1):
            scaffolding=tile.scaffolding
            # Generate full image 4-tuples from scaffold tiles
            # to allow all four image tiles of the current tile to
            # be computed in one go.
            left_scaffold=image_to_tile(scaffolding[0])
            upper_scaffold=image_to_tile(scaffolding[1])
            right_scaffold=image_to_tile(scaffolding[2])
            if(count%10000 == 0): #Records progress
                if write_output:
                    f=open('progress_tracker_F'+str(prime)+'.txt', 'a')
                    f.write("Unique tiles: "+ str(len(tiles))+ " - Processed tiles: "+ str(count*4)+  " - Unprocessed tile backlog: "+ str(len(new_tiles)))
                    f.write('\n')
                    f.close()
                print("Unique tiles:", len(tiles), "- Processed tiles:", count*4, "- Unprocessed tile backlog:", len(new_tiles))
            merged_image=nw_from_scaffold(left_scaffold, upper_scaffold, right_scaffold, prime)# Step 1.2.1 and Step 1.2.2
            # Split merged image tiles into constituent tiles
            # ready to be assigned as images of current tile
            image=image_split(merged_image) # Returns images as [upper, left, right, lower]
            images=[]
            for i in range(len(image)):# Steps 1.2.2 and 1.2.4
                value=image[i]
                key=str(value)
                unique=tiles.get(key)
                index=len(tiles)
                # If the image tile is unique, add to tiles dict and new_tiles
                # list ready to have its own images processed
                if unique==None:
                    new_tile=TO.Tile(index, value) #Step 1.2.3
                    tiles[key]=new_tile
                    new_tiles.append(new_tile)
                    # Construct scaffolding for new_tile
                    # Hint: scaffolding variable is a list of [left, upper, right] scaffold tiles for the parent tile
                    # Step 1.2.2 and Step 1.2.4
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
            tile.update_images(images[1], images[0], images[2], images[3])# Step 1.2.5
        count+=1
    return tiles

"""
Function to split full image of a 4 tuple into four individual tiles
"""
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

"""
Function to calculate full image (all four tiles) of a tile from input scaffolding
"""
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

"""
Function to merge 4 image tiles into a full 4-tuple
"""
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

"""
Generates the lower tile based on the three tiles above it.
This version of the function works for any row other than row 0.
This function differs from nw_from_tuple in how the tiling space is formatted.
"""
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

########################### SUBSTITUTION VERIFICATION ###########################

"""
***Algorithm 2.1: Generating all possible 4-tuples***
Function to find all 4-tuples generated by substitution rules of number wall
"""
def generate_four_tuples(tiles):
    tuples_by_index=[]
    for i in tiles: # Step 2.1.1
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
    for tup in tuples_by_index: # Step 2.1.2 and Step 1.2.4
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
        #End Step 2.1.2
        # Search for new tuples
        new_tuples=[]
        # Take care when zero tiles are present, those should not be used when forming the Upper and Right tuples
        if tup[1]>1:#Step 1.2.3: Find new tuples
            new_tuples.append([image_tuple[0][1],image_tuple[0][2],image_tuple[1][2],image_tuple[1][1]]) # Upper tuple
            new_tuples.append([image_tuple[1][2],image_tuple[1][3],image_tuple[2][3],image_tuple[2][2]]) # Right tuple
        new_tuples.append([image_tuple[1][0],image_tuple[1][1],image_tuple[2][1],image_tuple[2][0]]) # Left tuple
        new_tuples.append([image_tuple[2][1],image_tuple[2][2],image_tuple[3][2],image_tuple[3][1]]) # Lower tuple
        new_tuples.append([image_tuple[1][1],image_tuple[1][2],image_tuple[2][2],image_tuple[2][1]]) # Middle tuple
        # Check each new tuple for uniqueness
        for new_tup in new_tuples: #Step 1.2.3: Check uniqueness of new tuples
            key=str(new_tup)
            unique=tuples.get(key)
            if not unique: # If tuple not in tuples dictionary
                tuples[key]=new_tup # Add to tuples dictionary
                tuples_by_index.append(new_tup)            
    return tuples_by_index 

"""
***Algorithm 2.2: Verifying the 4-tuples***
# Function to Verify that every 4-tuples satisfies the Frame Constraints
"""
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
    #Ignore first two tuples as they are all zero
        if(count==(tuples_num*print_helper)):
            print("Verification process at", 25*print_helper,"% complete!")
            if write_output:
                f=open('progress_tracker_F'+str(prime)+'.txt', 'a')
                f.write("Verification process at"+ str(100*count/len(tuples_by_index))+"% complete!")
                f.write('\n')
                f.close()
            print_helper += 1
            #Step 2.2.1
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
        #Step 2.2.2
        calculated_four_tuple=[complete_nw[tile_len+tile_len//2-1][tile_len//2:tile_len+tile_len//2]]
        for i in range(tile_len//2-1):
            calculated_four_tuple.insert(0, complete_nw[tile_len+tile_len//2-i-2][tile_len//2+i+1:tile_len+tile_len//2-i-1])
            calculated_four_tuple.append(complete_nw[tile_len+tile_len//2+i][tile_len//2+i+1:tile_len+tile_len//2-i-1])
        expected_tuple=tiles_by_index[tup[3]]
        if (expected_tuple!=calculated_four_tuple):#Step 2.2.2
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

########################### File Output ###########################

"""
Function to output total time taken in a human readable format.
"""
def seconds_to_hours(total_time):
    minutes=total_time//60
    seconds=total_time%60
    hours=minutes//60
    minutes=minutes%60
    return 'Total time = '+str(hours)+' hours, '+str(minutes)+' minutes and '+str(seconds)+' seconds.' 

"""
Primary testing function.
"""
def main():
    prime=3 # Currently tested with (pf) 3, 7, 11 and (2nd-lv-pf) 5.
    seq=paperfolding(1,10000) # Set the exact sequence to use, can be:
    # 'paperfolding' for Paperfolding sequence  OR  'adapted_paperfolding' for Second-Level Paperfolding sequence
    TO.Tile.tile_length=8 # Set tile length from sequence coding
    TO.Tile.tile_prime=prime # Set the prime to be used in the program, to save passing the parameter to every function
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
    