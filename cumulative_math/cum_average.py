import math


class CumulativeMovingAverage:
    '''
    CMA(n-1) = (a(1) + ... + a(n-1))/(n-1)
    CMA(n) = (a(1) + ... + a(n-1) + a(n))/(n-1) * (n-1)/n =
           = (CMA(n-1) + a(n)/(n-1)) * (n-1)/n =
           = ( a(n) + (n-1) * CMA(n-1) ) / n
    '''

    def __init__(self):
        self.cma = 0.0
        self.n = 0

    def update(self, v):
        self.cma = (v + self.n * self.cma) / (self.n + 1)
        self.n += 1

    def average(self):
        if self.n == 0:
            raise ValueError('No data')
        return self.cma

    def len(self):
        return self.n


class CumulativeMovingStandardDeviation:
    '''
    X — set of data
    E[X] = μ — average or expected value
    σ² = E[(X-μ)²] = E[X²]-2μE[X]+μ² = E[X²]-μ²
    Uncorrected sample standard deviation = √(σ²)
    Corrected sample standard deviation = √((N/(N-1))σ²) = √(N/(N-1) √(σ²)
    '''

    def __init__(self):
        self.cma = CumulativeMovingAverage()
        self.cma2 = CumulativeMovingAverage()  # mean of squares

    def update(self, v):
        self.cma.update(v)
        self.cma2.update(v * v)

    def average(self):
        return self.cma.average()

    def len(self):
        return self.cma.len()

    def std_deviation_square(self):
        m = self.average()
        return self.cma2.average() - m * m

    def std_deviation(self):
        return math.sqrt(self.std_deviation_square())

    def corrected_std_deviation(self):
        n = self.len()
        if n < 2:
            raise ValueError('Not enough data')
        return self.std_deviation() * math.sqrt(float(n) / (n - 1))


if __name__ == '__main__':
    a = CumulativeMovingStandardDeviation()
    for x in range(0, 5):
        a.update(x)
    for x in range(4, -1, -1):
        a.update(x)

    print(a.average())  # 2.0
    print(a.std_deviation())  # 1.41421356237 (√2)
    print(a.corrected_std_deviation())  # 1.490711985 (√(20/9))
