from Labs.Lab3.data.table import Table
from Labs.Lab3.integrals.AnyCompIntegrate import AnyCompIntegrate


class TrapezesMethod(AnyCompIntegrate):
    def __init__(self):
        super().__init__("Интегрирование методом трапеций")

    def integrate(self, f, a, b, n, epsilon):
        result = Table(head=["Номер шага", "n", "S_n", "|S_n*2 - S|"])
        if a > b:
            a, b = b, a

        steps = 1
        h = (b - a) / n
        x = [(a + h * i) for i in range(n + 1)]
        y = [f(x[i + 1]) for i in range(n - 1)]
        s_n = (sum(y) + (f(x[0]) + f(x[-1])) / 2) * h
        runge_num = epsilon + 1
        result.add_row(row=[steps, n, s_n, "-"])

        while (runge_num > epsilon) and (not self.is_n_too_big(n)):
            steps += 1

            new_x = []
            for i in range(n):
                new_x.append(x[i])
                new_x.append((x[i] + x[i + 1]) / 2)
            new_x.append(x[-1])
            x = new_x

            n = len(x) - 1
            h = (b - a) / n
            y = [f(x[i]) for i in range(1, n - 1)]

            s_half_n = s_n
            s_n = (sum(y) + (f(x[0]) + f(x[-1])) / 2) * h
            runge_num = self.runge_rule(s_n, s_half_n, p=2)
            result.set_cell(-1, 3, runge_num)
            result.add_row(row=[steps, n, s_n, "-"])

        return result
