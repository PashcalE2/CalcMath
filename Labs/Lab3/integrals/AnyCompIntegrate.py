
class AnyCompIntegrate:
    def __init__(self, name):
        self.name = name

    def integrate(self, f, a, b, n, epsilon):
        pass

    def __str__(self):
        return self.name

    def runge_rule(self, s_n, s_half_n, p=2):
        return abs(s_n - s_half_n) / (2 ** p - 1)
