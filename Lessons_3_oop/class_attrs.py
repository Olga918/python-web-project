class Sample:
    field1 = 'str'
    field2 = []
    
    # def __init__(self):
    #     # self.field1 = ''
    #     # self.field2 = []
    

s = Sample()

print(s.__dict__)

print(s.field1)

s.field1 = 'Hello'
print(s.field1)
print(Sample.field1)
print(s.__dict__)

s.field2.append(1)

print(Sample.field2)
print(s.__dict__)

s2 = Sample()
s2.field2.append(2)

print(Sample.field2)

class A:
    __private_field:str = 'private'
    _protected_field: str = 'protected'
    
    def __init__(self, private, protected):
        self.__private_field = private
        self._protected_field = protected
    
# a = A()

# print(a.__private_field)
# print(a._protected_field)

class B(A):
    def __init__(self, private, protected):
        super().__init__(private, protected)
    def do_smth(self):
        # print("Private:", self.__private_field)
        print("Protected:", self._protected_field)

B("1", "2").do_smth()