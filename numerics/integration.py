from math import ceil


class Integrator:
    def __init__(self, extrapolation_power=1):
        self.extrapolation_power = extrapolation_power

    def integrate(self, f, a, b, n):
        raise NotImplementedError("Choose a proper implementation")

    def extrapolate(self, f, a, b, n):
        """
        Extrapolation des Integrators
        :param f: Die zu integrierende Funktion in der Form y=f(x)
        :param a: Untere Schranke
        :param b: Obere Schranke
        :param n: Anzahl Intervalle
        :return: Der integrierte Wert
        """

        i_2h = self.integrate(f, a, b, n / 2)
        i_h = self.integrate(f, a, b, n)

        return i_h - ((i_h - i_2h) / (2 ** self.extrapolation_power - 1))


class SimpsonIntegrator(Integrator):
    def __init__(self):
        super().__init__(4)

    def integrate(self, f, a, b, n):
        n = ceil(n)
        h = (b - a) / n
        integrated = f(a) + f(b)

        for i in range(1, n):
            factor = 2 if i % 2 == 0 else 4
            integrated += factor * f(a + i * h)

        return (h * integrated) / 3


class TrapezoidalIntegrator(Integrator):
    def __init__(self):
        super().__init__(2)

    def integrate(self, f, a, b, n):
        n = ceil(n)
        h = (b - a) / n

        integrated = f(a) + f(b)
        for i in range(1, n): integrated += 2 * f(a + i * h)

        return 0.5 * h * integrated
