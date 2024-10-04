class square:
    def __init__(self, side):
        self.area = side*side

    def __repr__(self) :
        return str(self.area)
    def __add__(self,other):
        return str(self.area + other.area)

s1 = square(90)
s2 = square(12)
print(s1)
print(s1+s2)

