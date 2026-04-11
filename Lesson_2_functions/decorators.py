# *args, **kwargs

def sample(*args, **kwargs):
    print(type(args))
    print(type(kwargs)) # key-word arguments
    
    if len(args) > 0:
        print("args:",args)
        print()
    
    if len(kwargs) > 0:
        print("kwargs:",kwargs)
        print()

sample(1,2,3,4,*(), name='user', surname='Due', **{"key1":"value1"}, **{})

def decorator(func):
    # def wrapper(): # якщи не вказувати параметрів то декоратор буде доступний для тих функцій які не приймають жодного параметру
    # *args, **kwargs - забезпечують можливість декорувати будь яку функцію з будь-якою кількістю параметрів, або взагалі без параметрів.
    # якщо нічого не передавати то пусті *args **kwargs означатимуть нічого, повна відсутність параметрів
    def wrapper(*args, **kwargs):
        print("-"*20)
        func(*args, **kwargs)
        print("-"*20)
    return wrapper

# Декорування функцій вручну
# create function
greeting = lambda: print("Hello")

# decorate function
greeting = decorator(greeting)
greeting()

print('\n')
# create function
greet_user = lambda username: print(f"Hello, {username}")
greet_user("William")

#decorate function
greet_user = decorator(greet_user)
greet_user("Will")

print("-"*10, "Автоматичне декорування функцій", "-"*10)

# Автоматичне декорування функцій:
@decorator # Python автоматично декорує функцію нижче
def sample_text():
    print("Hello")
    
sample_text()

@decorator
def user_text(text:str):
    print(text)
    
user_text("Text")

# decorator with parameters

from functools import wraps
print("-"*10, "Decorator with params", "-"*10)

def decorator_param(symbol:str = '-'):
    def decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(symbol*10)
            r = func(*args, **kwargs)
            print(symbol*10)
            return r
        # wrapper.__name__ = func.__name__
        # wrapper.__doc__ = func.__doc__
        return wrapper
    return decor

def s(param:str = ""):
    """
    This a test function for decorator.
    
    Args:
        param(str): test parameter(optional)
    """
    print("Test,", param)

s = decorator_param("$")(s)
print(s.__name__)
help(s)

@decorator_param("^")
def a():
    print("a function")

a()
print(a.__name__)

@decorator_param()
def b(): return 12

print(b())