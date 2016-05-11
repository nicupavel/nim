__author__ = "Nicu Pavel <npavel@linuxconsulting.ro>"

import math

class EvaluationOverflow(Exception):
    limit = 50000
    current = 0

    @classmethod
    def check(cls):
        cls.current += 1
        if cls.current >= cls.limit:
            raise EvaluationOverflow

class float2e(float):
    def __repr__(self):
        return "%0.2f" % self

class EvalFunc:
    def __init__(self, axes=2):
        self.evaluations = 0
        self.start = 0
        self.end = 0
        self.axes = axes
        self.decimals = 2
        self.intervals = [] # only used in GA TBD for hillclimbing

    def eval(self, l):
        self.evaluations += 1
        return l

    def fitness(self, l):
        return 1/(self.eval(l) + 0.0000001)

    def info(self):
        return "Default evaluator"

# http://www.geatbx.com/docu/fcnindex-01.html#P140_6155
# all functions accept list as parameter depending on dimensions
# rastrigin(x) = 10 * n + sum(x(i)^2 - 10*cos(2*pi*x(i))), i=1:n, -5.12 <= x(i) <= 5.12
class Rastrigin(EvalFunc):
    def __init__(self, axes=2):
        EvalFunc.__init__(self, axes)
        self.start = -5.12
        self.end = 5.12
        self.intervals = [(self.start, self.end)] * axes
        #self.intervals = [(-3, 3), (-3, 3)]

    def eval(self, l):
        self.evaluations += 1
        n = len(l)
        res = 10 * n + sum((x ** 2 - 10 * math.cos(2 * math.pi * x)) for x in l)
        return res

    def info(self):
        return "Rastrigin global minimum f(x)=0; x(i)=0, i=1:n"

# f8(x)=sum(x(i)^2/4000)-prod(cos(x(i)/sqrt(i)))+1, i=1:n -600<=x(i)<= 600.
class Griewangk(EvalFunc):
    def __init__(self, axes=2):
        EvalFunc.__init__(self, axes)
        self.start = -600
        self.end = 600
        self.intervals = [(self.start, self.end)] * axes

    def eval(self, l):
        self.evaluations += 1
        product = 1
        for i in range(0, len(l)):
            product *= math.cos(l[i] / math.sqrt(i + 1))
        res = sum((math.pow(x, 2) / 4000.0) for x in l) - product + 1
        return res

    def info(self):
        return "Griewangk global minimum f(x)=0; x(i)=0, i=1:n"


# f2(x)=sum(100*(x(i+1)-x(i)^2)^2+(1-x(i))^2) i=1:n-1; -2.048<=x(i)<=2.048.
class Rosenbrock(EvalFunc):
    def __init__(self, axes=2):
        EvalFunc.__init__(self, axes)
        self.start = -2.048
        self.end = 2.048
        self.decimals = 3
        self.intervals = [(self.start, self.end)] * axes


    def eval(self, l):
        self.evaluations += 1
        sum = 0
        for i in range(0, len(l)-1):
            sum = sum + 100 * (l[i + 1] - l[i] ** 2) ** 2 + (1 - l[i]) ** 2
        return sum

    def info(self):
        return "Rosenbrok global minimum f(x)=0; x(i)=1, i=1:n"


# fSixh(x1,x2)=(4-2.1*x1^2+x1^4/3)*x1^2+x1*x2+(-4+4*x2^2)*x2^2 -3<=x1<=3, -2<=x2<=2.
class Sixhump(EvalFunc):
    def __init__(self, axes=2):
        EvalFunc.__init__(self) # Doesn't work on more than 2 axes/dimensions
        self.start = -2
        self.end = 2
        self.decimals = 6
        self.intervals = [(-3, 3), (-2, 2)]

    def eval(self, l):
        self.evaluations += 1
        x1 = l[0]
        x2 = l[1]
        res = (4 - (2.1 * (x1 ** 2)) + math.pow(x1, 4)/3) * (x1 ** 2)
        res += x1 * x2
        res += (-4 + 4 * (x2 ** 2)) * (x2 ** 2)
        return res

    def fitness(self, l):
        return 1/(self.eval(l) + 1.05)

    def info(self):
        return "Six Hump Camel back global minimum f(x1,x2)=-1.0316; (x1,x2)=(-0.0898,0.7126), (0.0898,-0.7126)"


# f=f=x3-60x2+900x+100
class Miscfunc1(EvalFunc):
    def __init__(self):
        EvalFunc.__init__(self)
        self.start = 0
        self.end = 32
        self.decimals = 0
        self.intervals = [(0, 31)]
        self.axes = 1

    def eval(self, l):
        self.evaluations += 1
        x = l[0]
        #res = math.pow(x, 3) - 60 * math.pow(x, 2) + 900 * x + 100
        #return res
        return x ** 3 - 60 * x ** 2 + 900 * x + 100

    def fitness(self, l):
        return self.eval(l)

    def info(self):
        return "Misc function f=x3-60x2+900x+100"


if __name__ == "__main__":
    r = Rastrigin(4)
    print r.axes
    print r.intervals