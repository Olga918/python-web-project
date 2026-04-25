print(type(1))

class T:
    pass

print(type(T()))

print(type(T))

# type(name_of_new_class:str, base_classes:tuple, **kwds)

def method_a(self):
    return "MethodA"

class Base:
    def derived_method(self):
        print("derived method")

Sample = type("Sample",(Base,),{
    "field_a": None,
    "field_b": 'hello',
    "method_a": method_a,
    "method_b": lambda self: "MethodB"
})

s = Sample()

print(s.method_a())
print(s.method_b())
print(s.field_a)
print(s.field_b)
s.derived_method()

print('-'*10,'Own metaclasses','-'*10)

class BaseClass:
    pass

class MyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        print("Metaclass:",cls)
        print("New class name:", name)
        print("Base classes:", bases)
        print("Namespace:", attrs)
        new_class = super().__new__(cls, name, bases, attrs)
        new_class.load_data = lambda self, model: print(f"Get records from {model}: {("id","c10c88e9-ed07-534f-90f5-a6cb2bdbe98e")}")
        return new_class
    
    def __call__(self, *args, **kwds):
        print("Call")
        return super().__call__(*args, **kwds)
    
class Class(BaseClass, metaclass=MyMetaClass):
    attr1 = "Attribute of Class"
    
c = Class()

c.load_data("MyModel")

OwnClass = MyMetaClass("OwnClass", (BaseClass,),{
    "field": 12,
    "method_1": lambda self:  print("method_1")
})


OwnClass().method_1()