# This python file holds all of the common functions required by
# multiple versions of the tiling program.

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
