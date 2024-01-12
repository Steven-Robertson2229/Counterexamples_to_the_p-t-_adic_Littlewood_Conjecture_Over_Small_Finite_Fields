import TileObject as TO
import CommonFunctions as CF
import CollabVersion3 as V3
import TileRefObject as TR
import CollabVersion3Plus as V3P
sub_rules=[['1','12'],['2','32'],['3','14'],['4','34']]
coding=[['1','00100110'],['2','00110110'],['3','00100111'],['4','00110111']]
def v4(sub_rules,coding,prime):
    tile_len=TO.Tile.tile_length
    tiles={}
    tiles_by_index=[]
    scaff=[]
    for i in range(len(sub_rules)+1):
        scaff.append("Filler offset")
    # Hard code zero'th tile
    # Instantiate zero'th Tile object
    tile0=TO.Tile(0, []) # The list and tuple are ignored here
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
            tiles_by_index.append(new_tile)
            scaff.append([left_tile,tile0,right_tile]) # Add scaffolding to the scaffolding list
            unique=new_tile
        current_tile=tiles_by_index[i+1]
        current_tile.left_image=left_tile
        current_tile.upper_image=tile0
        current_tile.right_image=right_tile
        current_tile.lower_image=unique
    # Loop through list of tiles (excluding input section)
    # identifying the images of each tile
    count =5
    #for tile in tiles_by_index[len(sub_rules)+1:]: 
    tile_count=len(tiles_by_index)
    while count<tile_count:
        tile=tiles_by_index[count]
        count+=1
        tile_count=len(tiles_by_index)
        print(count)
        scaffolding=scaff[tile.id]
        print('scaffolding[0]=')
        print(scaffolding[0].upper_image)
        print('done')
        left_scaffold=image_to_tile(scaffolding[0])
        upper_scaffold=image_to_tile(scaffolding[1])
        right_scaffold=image_to_tile(scaffolding[2])
        image=nw_from_scaffold(left_scaffold, upper_scaffold, right_scaffold, prime)
        image=image_split(image)
        tiles_to_scaff=[]
        positions_to_scaff=[]
        new_tile_ind=[]
        for i in image:
            key=str(i)
            print('key=')
            print(key)
            unique=tiles.get(key)
            ind=len(tiles)
            if unique==None:
                new_tile=TO.Tile(ind,i)
                tiles_by_index.append(new_tile)
                tiles[key]=new_tile
                tiles_to_scaff.append(ind)
                new_tile_ind.append(ind)
                positions_to_scaff.append(image.index(i))
            else:
                new_tile_ind.append(unique.id)
        tile.upper_image=tiles_by_index[new_tile_ind[0]]
        tile.left_image=tiles_by_index[new_tile_ind[1]]
        tile.right_image=tiles_by_index[new_tile_ind[2]]
        tile.lower_image=tiles_by_index[new_tile_ind[3]]
        if tiles_to_scaff!=[]:
            grid=[]
            grid.append([scaffolding[1].upper_image])
            grid.append([scaffolding[1].left_image,scaffolding[1].right_image])
            grid.append([scaffolding[0].upper_image, scaffolding[1].lower_image,scaffolding[2].upper_image])
            grid.append([scaffolding[0].left_image,scaffolding[0].right_image,scaffolding[2].left_image,scaffolding[2].right_image])
            grid.append([scaffolding[0].lower_image,new_tile_ind[0],scaffolding[2].lower_image])
            grid.append([new_tile_ind[1],new_tile_ind[2]])
            grid.append([new_tile_ind[3]])
            # grid.append([upper_scaffold.upper_image])
            # grid.append([upper_scaffold.left_image,upper_scaffold.right_image])
            # grid.append([left_scaffold.upper_image, upper_scaffold.lower_image,right_scaffold.upper_image])
            # grid.append([left_scaffold.left_image,left_scaffold.right_image,right_scaffold.left_image,right_scaffold.right_image])
            # grid.append([left_scaffold.lower_image,new_tile_ind[0],right_scaffold.upper_image])
            # grid.append([new_tile_ind[1],new_tile_ind[2]])
            # grid.append([new_tile_ind[3]])
            for i in range(len(tiles_to_scaff)):
                if positions_to_scaff[i]==0: # Upper tile
                    scaff.append([grid[3][1],grid[2][1],grid[3][2]])
                elif positions_to_scaff[i]==1: # Left tile
                    scaff.append([grid[4][0],grid[3][1],grid[4][1]])
                elif positions_to_scaff[i]==2: # Right tile
                    scaff.append([grid[4][2],grid[3][2],grid[4][2]])
                else: # ==3 # Lower tile
                    scaff.append([grid[5][0],grid[4][1],grid[5][1]])
    return len(tiles)
        

# Function to split full image 4 tuple into constituent parts    
def image_split(image):
    tile_len=TO.Tile.tile_length
    TO2=tile_len//2
    TO2M1=TO2-1
    # Upper tile
    upper=[]
    for i in range(TO2):
        upper.append(image[i])
    for i in range(TO2M1):
        #upper.insert(0, image[TO2-1-i][2+2*i:-2-2*i])
        upper.append(image[TO2+i][2+2*i:-2-2*i])
    # Lower tile
    lower=[]
    for i in range(TO2):
        lower.append(image[-i-1])
    for i in range(TO2M1):
        lower.insert(0, image[-TO2-1-i][2+2*i:-2-2*i])
        #lower.append(image[TO2+i][2+2*i:-2-2*i])
    # Left tile
    left=[]
    middle=tile_len-1
    left.append(image[middle][:-tile_len])
    for i in range(TO2M1):
        left.insert(0, image[middle-1-i][:tile_len-2*i-2])
        left.append(image[middle+1+i][:tile_len-2*i-2])
    # Right tile
    right=[]
    right.append(image[middle][tile_len:])
    for i in range(TO2M1):
        right.insert(0, image[middle-1-i][tile_len-2*i-2:])
        right.append(image[middle+1+i][tile_len-2*i-2:])
    return [upper,left,right,lower]

# Function to calculate full image (all four tiles) from input scaffolding  
def nw_from_scaffold(left_scaffold, upper_scaffold, right_scaffold, prime):
    tile_len=TO.Tile.tile_length*2
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
    #for p in incomplete_nw:
     #   print(p)
    complete_nw=V3.nw_from_tuple(incomplete_nw, prime)
    # Extract calculated lower tile
    calculated_four_tuple=[complete_nw[tile_len+tile_len//2-1][tile_len//2:tile_len+tile_len//2]]
    for i in range(tile_len//2-1):
        calculated_four_tuple.insert(0, complete_nw[tile_len+tile_len//2-i-2][tile_len//2+i+1:tile_len+tile_len//2-i-1])
        calculated_four_tuple.append(complete_nw[tile_len+tile_len//2+i][tile_len//2+i+1:tile_len+tile_len//2-i-1])
    return calculated_four_tuple
        
# Function to merge 4 images of a tile into a full 4 tuple
def image_to_tile(tile: TO.Tile):
    left_tile=tile.left_image
    upper_tile=tile.upper_image
    right_tile=tile.right_image
    lower_tile=tile.lower_image
    length=TO.Tile.tile_length*2
    tile_len=TO.Tile.tile_length
    TO2=tile_len//2
    TO2M1=TO2-1
    output=[['*' for i in range(length)]]
    for i in range(length//2-1):
        output.insert(0, ['*' for i in range(length-2*i-2)])
        output.append(['*' for i in range(length-2*i-2)])
    # Upper tile
    for i in range(TO2):
        print(upper_tile.value)
        output[i]=upper_tile.value[i]
    for i in range(TO2M1):
        for j in range(tile_len-2-2*i):
            output[TO2+i][2+j+2*i]=upper_tile.value[TO2+i][j]
    # Lower tile
    for i in range(TO2):
        output[-i-1]=lower_tile.value[-i-1]
    for i in range(TO2M1):
        for j in range(tile_len-2-2*i):
            output[-(TO2+i)-1][2+j+2*i]=lower_tile.value[-(TO2+i)-1][j]
    middle=length//2-1
    tile_middle=tile_len//2-1
    # Left tile
    for i in range(tile_len):
        output[middle][i]=left_tile.value[tile_middle][i]
    for i in range(TO2M1):
        for j in range(tile_len-2-2*i):
            output[middle-1-i][j]=left_tile.value[tile_middle-1-i][j]
            output[middle+1+i][j]=left_tile.value[tile_middle+1+i][j]
    # Right tile
    for i in range(tile_len):
        output[middle][i+tile_len]=right_tile.value[tile_middle][i]
    for i in range(TO2M1):
        for j in range(tile_len-2-2*i):
            output[middle-1-i][j+tile_len]=right_tile.value[tile_middle-1-i][j]
            output[middle+1+i][j+tile_len]=right_tile.value[tile_middle+1+i][j]
    return output

def main():
    TO.Tile.tile_length=len(coding[0][1])
    v4(sub_rules,coding,3)
main()
#abc=[0,1,2,3,4,5,6,7,8,9]
#print(abc[:-2])    
    