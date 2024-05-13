# This python file holds all of the common functions required by
# multiple versions of the tiling program.

def ratio(X, Y, prime):
   return (X*div(Y, prime)) % prime

# Lazy div function
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

# Function to grow an already existing Number Wall (prev_wall)
# by slices - i.e. one diagonal row of tiles at a time.
# Note: when inputting a starting wall to wall_gen, add two additional
# 1's to prev_wall row 1 to avoid an edge case bug in the top row
# This function has been imported from CollabVersion3.py
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
            # narrow window frame rule 1 - cheat rule
            elif ((prev_wall[row-2][-4]==0) and (prev_wall[row-1][-2]==0) and (prev_wall[row][-1]!=0)):
                x = prev_wall[row][-1]
                y = prev_wall[row][-2]
                output=((x*div(y,prime))*x) % prime
                prev_wall[row].append(output)
            # narrow window frame rule 2 - cheat rule
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


