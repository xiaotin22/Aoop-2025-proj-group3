class point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "Point(%s, %s)" % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return point(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        return point(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        return point(self.x // other.x, self.y // other.y)

    def __mod__(self, other):
        return point(self.x % other.x, self.y % other.y)

    def __pow__(self, other):
        return point(self.x ** other.x, self.y ** other.y)

    def __lshift__(self, other):
        return point(self.x << other.x, self.y << other.y)

    def __rshift__(self, other):
        return point(self.x >> other.x, self.y >> other.y)

    def __and__(self, other):
        return point(self.x & other.x, self.y & other.y)

    def __xor__(self, other):
        return point(self.x ^ other.x, self.y ^ other.y)

    def __or__(self, other):
        return point(self.x | other.x, self.y | other.y)

    def __neg__(self):
        return point(-self.x, -self.y)

    def __pos__(self):
        return point(+self.x, +self.y)

    def __abs__(self):
        return point(abs(self.x), abs(self.y))

    def __invert__(self):
        return point(~self.x, ~self.y)

    def __complex__(self):
        return complex(self.x, self.y)
    
if __name__ == "__main__":
    a = point(1, 2)
    b = point(3, 4)
    print(a + b)
    print(a - b)
    print(a * b)
    print(a / b)
    print(a // b)
    print(a % b)
    print(a ** b)
    print(a << b)
    print(a >> b)
    print(a & b)
    print(a | b)
    print(a ^ b)
    print(-a)
    print(+a)
    print(abs(a))
    print(~a)
    print(complex(a))
