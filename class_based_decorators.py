#sayHello Class decorator
def add_greeting(cls):
    cls.greeting = "Hello, world!"
    return cls

@add_greeting
class MyClass:
    def __init__(self):
        pass

# Usage
print(MyClass.greeting)  # Output: Hello, world!




#UpperCase Class based decorator
def upper_Case(cls):
    def wrapper(*args, **kwargs):
        result = cls(*args, **kwargs)
        print(result.upper())
    return wrapper

@upper_Case
class MyClass:
    def greet(self):
        return "hello"

# Usage
obj = MyClass()
print(obj.greet())  # Output: HELLO





#Repeat Class based decorator
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
class MyClass:
    def __init__(self, *args):
        self.args = args

# Usage
obj = MyClass(1, 2)
print(obj.args)  # Output: (1, 2, 1, 2, 1, 2)
