class square:
    def __init__(self, side):
        self.area = side*side

    def __repr__(self) :
        return str(self.area)
s1 = square(90)
print(s1)