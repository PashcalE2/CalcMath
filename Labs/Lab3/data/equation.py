class Equation:
    def __init__(self, derivatives: list, to_string: str):
        self.derivatives = derivatives
        self.to_string = to_string

    def derivative(self, derivative_n):
        return self.derivatives[derivative_n]

    def __str__(self):
        return self.to_string
