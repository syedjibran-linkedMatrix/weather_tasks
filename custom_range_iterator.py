class MyRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start

    def __iter__(self):
        return self  # The iterator object itself

    def __next__(self):
        if self.current < self.end:
            value = self.current
            self.current += 1
            return value
        else:
            raise StopIteration  # Indicate that the iteration is complete

# Example usage
my_range = MyRange(1, 5)
for num in my_range:
    print(num)
