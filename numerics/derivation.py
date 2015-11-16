class Differentiator:
    def differentiate(self, f, x, h=10 ** -5):
        raise NotImplementedError("Choose a proper implementation")

    def extrapolate(self, f, x, h=10 ** -5):
        d_h = self.differentiate(f, x, h / 2)
        d_2h = self.differentiate(f, x, h)

        return d_h + ((d_h - d_2h) / (2 ** 2 - 1))


class ForwardDifferentiator(Differentiator):
    def differentiate(self, f, x, h=10 ** -5):
        return (f(x + h) - f(x)) / h


class BackwardDifferentiator(Differentiator):
    def differentiate(self, f, x, h=10 ** -5):
        return (f(x) - f(x - h)) / h


class CenteredDifferentiator(Differentiator):
    def differentiate(self, f, x, h=10 ** -5):
        return (f(x + h) - f(x - h)) / (2 * h)
