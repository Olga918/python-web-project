# __magic__()

# __len__

class Collection:
    __start = 0
    def __init__(self, *args):
        self.collect = list(args)
    
    def __len__(self):
        return len(self.collect)
    
    def __getitem__(self, key):
        if(key < 0):
            raise IndexError("Index out of range")
        return self.collect[key]

    def __setitem__(self, key, value):
        if(key < 0):
            raise IndexError("Index out of range")
        self.collect[key] = value
    
    def __iter__(self):
        return self
    
    def __contains__(self, item):
        print("Contains")
        return item in self.collect
    
    def __next__(self):
        if self.__start >= len(self):
            self.__start = 0
            raise StopIteration
        self.__start+=1
        return self[self.__start-1]
    

c = Collection(1,2,3,4,'Hello')

print(c)
print(len(c))
c[1]= 'Changed'
print(c[1])

for i in c:
    print(i)
    
print(1 in [1,2])
print(10 in c)