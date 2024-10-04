from functools import partial

#partial function is to fix the number of arugments of a function
#it returns a new function

def add(n1,n2,n3,n4):
    return n1+n2+n3+n4


add = partial(add, 3,2) #fixing the values of n1 and n2

print(add(5,4)) #giving the values of n3 and n4 only