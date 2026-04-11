from functools import wraps, update_wrapper, partial
from types import MethodType

def f_decorator(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        print("f_decorator")
        return orig_func(*args, **kwargs)
    return wrapper


class obj_decorator:
    def __init__(self, orig_func):
        self.orig_func = orig_func
        self.__counter = 0
        update_wrapper(self, orig_func)
        
    @property
    def call_count(self):
        return self.__counter
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return MethodType(self, instance)
    
    def __call__(self, *args, **kwds):
        print("obj_decorator")
        self.__counter += 1
        return self.orig_func(*args, **kwds)
    

    
class sample_class:
    @f_decorator
    def sample_method(self):
        print("sample_method")
    
    @obj_decorator   
    def method2(self):
        print("method2")
        return 'Test'
        
# print(sample_class().sample_method.__name__)

s = sample_class()

# s.method2 = obj_decorator(s.method2)
s.method2()
s.method2()
s.method2()
s.method2()
print(s.method2.call_count)
print(s.method2.__name__)
help(s.method2)
# s.method2.call_count
# print(s.method2.call_count)


@obj_decorator
def sample_function():
    print("sample_function")
    
sample_function()
sample_function()
print(sample_function.__name__)
print(sample_function.call_count)

print('-'*10,'Class decorator', '-'*10)

def cls_decor(target):
    # target - це є сам клас
    target.sum = lambda self, x,y: x + y
    return target

@cls_decor
class sample_cls:
    pass

print(sample_cls().sum(1,2))

print(sample_cls.__dict__)