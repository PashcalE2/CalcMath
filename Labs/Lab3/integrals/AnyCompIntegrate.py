
class AnyCompIntegrate:
    def __init__(self, name):
        self.name = name
        self.n_max = 2 ** 20

    def integrate(self, f, a, b, n, epsilon):
        pass

    def __str__(self):
        return self.name

    def runge_rule(self, s_n, s_half_n, p=2):
        return abs(s_n - s_half_n) / (2 ** p - 1)

    def set_n_max(self, n):
        self.n_max = n

    def get_n_max(self):
        return self.n_max

    def is_n_too_big(self, n):
        return n >= self.n_max
