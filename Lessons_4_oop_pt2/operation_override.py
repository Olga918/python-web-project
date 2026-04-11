class Fraction:
    numerator: int
    denominator: int
    
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"
    
    # __add__  Fract(1,2) + Fract(3,5) = new obj of Fract
    def __add__(self, other):
        res = Fraction(0,0)
        res.denominator = self.denominator * other.denominator
        res.numerator = (self.numerator* other.denominator) + (other.numerator * self.denominator)
        return res
    
    # __iadd__ +=
    def __iadd__(self, other):
        # res = Fraction(0,0)
        denominator = self.denominator * other.denominator
        numerator = (self.numerator* other.denominator) + (other.numerator * self.denominator)
        self.numerator = numerator
        self.denominator = denominator
    
        
    # __sub__ fract1 - fract2
    # __isub__ fract1 -= fract2
    
    # __mul__ fract1 * fract2
    # __imul__ fract1 *= fract2
    
    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator
    

print(Fraction(3,5)+Fraction(1,2))
print(Fraction(3,5) == Fraction(1,2))