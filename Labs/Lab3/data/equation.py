class Equation:
    def __init__(self, f_x, undefined_points: list, to_string: str):
        self.f_x = f_x
        self.undefined_points = undefined_points
        self.to_string = to_string

        self.derivative = None

    def get_f_x(self):
        return self.f_x

    def set_derivative(self, equation):
        self.derivative = equation
        return self

    def get_derivative(self):
        return self.derivative

    def get_undef_points(self):
        return self.undefined_points

    def __str__(self):
        return self.to_string
