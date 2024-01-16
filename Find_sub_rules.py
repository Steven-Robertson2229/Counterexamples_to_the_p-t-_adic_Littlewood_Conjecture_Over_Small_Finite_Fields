import TileObject as TO
TO.Tile.tile_len=16
def Dragon(n):
    """
    This function returns the nth element of the dragon sequence
    """
    if n == 0:
        return 0
    else:
        while n%2 == 0:
        #while n%2 == 0:
            n = n / 2
    return int(((n-1)/2)%2)

def pfseq1(start,end,a,b): #Finds first n digits of paper folding sequence
    ans=[]
    for i in range(start,end+1):
        x=Dragon(i)
        #print(x)
        if x==0:
            ans.append(a)
        if x==1:
            ans.append(b)
    return ans

def Pagoda(n):
    """
    This function returns the nth element of the pagoda sequence
    """
    return Dragon(n+1) - Dragon(n-1)

def pagseq(start,end,a,b):
    return [Pagoda(i) for i in range(start,end+1)]

def pf5(n): #calculates nth digit of the paper folding sequence
    if n==0:
        return 0
    while n-(n//2)*2==0:
        n=n//2
    #print(n/2**k)
    #print(int(n))
    if int(n)%8==1:
        return 0
    elif int(n)%8==3:
        return 1
    elif int(n)%8==5:
        return 2
    else: 
        return 3

def pfseq5(start,end,a,b):
    return [pf5(i) for i in range(start,end+1)]


def find_sub_rules(seq):
    l=0 #2**l is the length of the tile
    while l>=0:
        maps=[] #these are the sub_stitution rules
        for i in range(len(seq)//(2**(l+1))):
            #generate new map
            new_map=[[seq[i* 2**l + j] for j in range(2**l)]\
                     ,[seq[i* 2**(l+1) + j] for j in range(2**(l+1))]]
            if new_map not in maps:
                check=False
                for j in maps:
                    #check if new_map is inconsistant with existing maps
                    if j[0]==new_map[0]:
                        check=True
                        break
                if check==False:
                    maps.append(new_map)
                else:#if new_map was inconsistant, increase l by 1 and restart
                    l+=1
                    break
        if check==False:
            return maps
        
#Generates the sub_rules and the coding that govens the sequence
def maps_to_sub_rules(maps):
    sub_rules=[]
    tiles=[i[0] for i in maps]
    coding=[]
    for i in range(1,len(maps)+1):
        rule=[i,[]]
        l=len(maps[i-1][1])//2
        left_image=maps[i-1][1][:l]
        right_image=maps[i-1][1][l:]
        rule[1].append(tiles.index(left_image)+1)
        rule[1].append(tiles.index(right_image)+1)
        sub_rules.append(rule)
        coding.append([i,tiles[i-1]])
    return sub_rules,coding

#Applies the sub_rules and coding until the tiles are of desired length
def apply_coding(sub_rules,coding):
    large_coding=[]
    for i in range(len(sub_rules)):#for each sub_rule
        rule=[i+1]
        image=sub_rules[i][1]
        while len(image)<TO.Tile.tile_length//(len(coding[0][1])):
            #apply sub_rules and coding until the image is long enough
            new_image=[]
            for k in image:
                new_image.append(sub_rules[k-1][1][0])
                new_image.append(sub_rules[k-1][1][1])
            image=new_image
        cod=[]
        for j in image:
            for k in range(len(coding[0][1])):
                cod.append(coding[j-1][1][k])
        rule.append(cod)
        large_coding.append(rule)
    return large_coding

#Combines all above functions into one
def sub_rule_full(seq):
    maps=find_sub_rules(seq)
    sub_rules,coding=maps_to_sub_rules(maps)
    large_coding=apply_coding(sub_rules, coding)
    return sub_rules, large_coding
sub_rules,coding=sub_rule_full(pfseq1(1,10000,0,1))
print('sub_rules')
for i in sub_rules:
    print(i)
print('coding')
for i in coding:
    print(i)

