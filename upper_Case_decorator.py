def upper_Case(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result.upper())
    return wrapper

@upper_Case
def sayHello(name):
    return f"Hello {name}!"

sayHello("Jibran")