class Sample:
    __counter:int
    
    def __init__(self):
        self.__counter = 0
        
    def release(self): self.__counter = 0
    
    @property
    def counter(self): return self.__counter
    
    def __call__(self, *args, **kwds):
        self.__counter += 1
        print(f"count_of:", self.counter)
        return self.counter
    
f = Sample()
f()
f()
f()
f.release()
print(f.counter)