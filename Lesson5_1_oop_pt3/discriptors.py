import os

class DirectorySize:
    def __get__(self, instance, owner):
        print("Instance:", instance)
        print("Instance type:", owner)
        return len(os.listdir(instance.dirname))
        
class Direcotry:
    size = DirectorySize()
    
    def __init__(self, dirname):
        self.dirname = dirname

d = Direcotry('../.venv')
print(d.size)

d.dirname = '../lesson5_oop_pt3'
print(d.size)


class LoggedFieldAccess:
    def __get__(self, instance, owner):
        print("Call getter")
        return instance.__field
    
    def __set__(self, instance, value):
        print("Update field")
        instance.__field = value
    
    def __delete__(self, instance):
        print("call delete")

class Sample:
    field = LoggedFieldAccess()
    
    def __init__(self, field):
        self.field = field
        
s = Sample(15)
print(s.field)

s.field = 20
print(s.field)

del s.field