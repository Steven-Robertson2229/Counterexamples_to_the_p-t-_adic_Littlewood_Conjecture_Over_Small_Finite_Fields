#import numpy
from Sequences import pfseq1, TM
from Number_Walls import numbwall, numbwall2
import random as rn
import copy as cop
def ratio(X, Y, prime):
   return (X*div(Y, prime)) % prime

def div(num, prime):
    num=num%prime
    if prime==2:
        return 1
    elif prime==3:
        if num==1:
            return 1
        else: # num==2
            return 2
    elif prime==5:
        if num==1:
            return 1
        elif num==2:
            return 3
        elif num==3:
            return 2
        else: # num==4
            return 4
    else: # prime==7
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
        else: # num==6
            return 6
    return "ERROR"

# Note: when inputting a starting wall to wall_gen, add two additional
# 1's to row 1 to avoid a crash 
def wall_gen(prime, prev_wall, new_num):
    # only add rows if row 0 has odd length
    if (len(prev_wall[0])%2==0):
        prev_wall.append([])
    # skip '-2' row
    # row -1 rule
    prev_wall[0].append(0)
    prev_wall[1].append(1)
    # row 0 rule, apply sequence
    prev_wall[2].append(new_num)
    for row in range(3, len(prev_wall)):
        cheat=True
        if row==len(prev_wall)-1:
            cheat=False
        #assume 'row', 'col' iterators
        #add in extra if layer for row-2 being 0
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
            else: # outer frame rule - frame constraint 3
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
    
def slice_gen_test(prime, prev_slice, new_nums, full_nw):
    tile_len=len(new_nums)
    new_slice=[]
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

def slice_gen(prime, prev_slice, new_nums):
    tile_len=len(new_nums)
    new_slice=[]
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

def pap_f(n):
    # This function returns the nth element of the paper folding sequence
    n += 1
    if n == 0:
        return 0
    else:
        while n%2 == 0:
            n = n / 2
    return int(((n-1)/2)%2)

def pagoda(n):
    # This function returns the nth element of the pagoda sequence
    return pap_f(n+1) - pap_f(n-1)

# Todo:
    # - Add logic into tiling loop to only collate the tile if it is in the 
    #   new tile dict (otherwise it is simply already a tile we have!)
    # - (In progress) Add logic to generate tile->image mapping dict
def tiling(prime, seq, tile_len):
    # Generate first slice
    prev_wall=[[0,0],[1,1,1,1],[seq(0),seq(1)]]
    for i in range(2, tile_len-2):
        prev_wall=wall_gen(prime, prev_wall, seq(i)%prime)
    current_slice=prev_wall
    slice_count=1
    growth_marker=1
    tiles={}
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
    # Map structure - key=location; value=(parent tile index, image tile a index, ...)
    maps[(-1,-1)]=(tiles[key0][1],tiles[key0][1],tiles[key0][1],tiles[key0][1])
    # Hard code first tile
    tile1=cop.deepcopy(prev_wall)
    for i in range(((tile_len-2)//2)-1):
        tile1.insert(0, [0 for j in range((tile_len-4)-(2*i))])
    key1=str(tile1)
    tiles[key1]=(tile1, 1) # Add to tiles
    # Map structure - key=location; value=(parent tile index, image tile a index, ...)
    maps[(0,0)]=(tiles[key1][1],tiles[key1][1],tiles[key0][1],-1,-1) # -1 implies a missing image tile index
    new_tiles[(0,1)]=True # Value here is arbitrary, so long as it isnt set to False
    new_tiles[(1,0)]=True
    # Loop over all slices until all new tiles found
    while(slice_count<growth_marker*2):
        current_slice=slice_gen(prime, current_slice, [seq(i)%prime for i in range((slice_count*tile_len)-2, ((slice_count+1)*tile_len)-2)])
        slice_count += 1
        if(slice_count%50==0):
            print(slice_count, len(tiles))
        for i in range(slice_count):
            # Increment cow and col near here
            new_tile=[]
            # New parent 'if', does (row, col) appear in new_tiles?
            # If yes, generate tiling, find parent tile, and add index to mapping, and remove from new_tiles
            # If no, skip
            # Specific logic for the top row
            if(i==0):
                new_tile.append(current_slice[1])
                for j in range((tile_len-2)//2):
                    new_tile.insert(0, [0 for k in range(tile_len-2-2*j)])
                    new_tile.append(current_slice[2+j][-(tile_len-2-2*j):])
            # All other rows
            else:
                new_tile.append(current_slice[1+i*(tile_len//2)])
                for j in range((tile_len-2)//2):
                    new_tile.insert(0, current_slice[i*(tile_len//2)-j][:(tile_len-2-2*j)])
                    new_tile.append(current_slice[2+i*(tile_len//2)+j][-(tile_len-2-2*j):])
            # Check if tile is new/unique
            key=str(new_tile)
            unique=tiles.get(key)
            if not unique: # If tile not in tiles dict
                tiles[key]=(new_tile,len(tiles)) # Add to tiles
                newtile=True 
                growth_marker=slice_count
                # Also add (row,col) to maps dict, and record location of image tiles
    print(len(tiles)) 
    return tiles




def main():
    L=800
    p=7
    start_wall=[[0,0,0],[1,1,1],pfseq1(1,3,0,1),[0]]
    lenny=8
    #print(start_wall,pfseq1(4,8,0,1))
    for i in pfseq1(4,lenny,0,1):
        prev_slice=wall_gen(p, start_wall,i)
    full_nw = cop.deepcopy(prev_slice)
    for i in range(1,(L//lenny)):
        #print(pfseq1(lenny*i+1,lenny*(i+1),0,1))
        prev_slice,full_nw = slice_gen(p, prev_slice,pfseq1(lenny*i+1,lenny*(i+1),0,1),full_nw)
    test_nw=numbwall2(numbwall(pfseq1(1,L,0,1),p))
    print(test_nw==full_nw)

#main()

print('AHHHHHHHHHHHHHHHH')