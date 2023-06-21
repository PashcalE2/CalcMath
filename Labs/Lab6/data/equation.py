class Equation:
    def __init__(self, func, undefined_points: list, to_string: str):
        self.func = func
        self.undefined_points = undefined_points
        self.to_string = to_string

        self.derivative = None

    def get_func(self):
        return self.func

    def set_derivative(self, equation):
        self.derivative = equation
        return self

    def get_derivative(self):
        return self.derivative

    def get_undef_points(self):
        return self.undefined_points

    def __str__(self):
        return self.to_string
