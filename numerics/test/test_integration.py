from unittest import TestCase

from math import exp

from numerics.integration import SimpsonIntegrator, TrapezoidalIntegrator


class SimpsonIntegratorTest(TestCase):
    integrator = SimpsonIntegrator()

    def test_integrate_simple(self):
        f = lambda x: x ** 2

        integrated = self.integrator.integrate(f, -1, 2, 100)

        self.assertEqual(3.0, round(integrated, 5))

    def test_integrates_with_rounding_to_9_digits(self):
        f = lambda x: exp((-1) * (x ** 2))

        integrated = self.integrator.integrate(f, -1, 2, 238)

        # Correct to 9  _significant_ digits
        self.assertEqual(1.62890552, round(integrated, 8))


class TrapezoidalIntegratorTest(TestCase):
    integrator = TrapezoidalIntegrator()

    def test_integrate_simple(self):
        f = lambda x: x ** 2

        integrated = self.integrator.integrate(f, -1, 2, 100)

        self.assertEqual(3.000, round(integrated, 3))

    def test_integrates_with_rounding_to_9_digits(self):
        f = lambda x: exp((-1) * (x ** 2))

        integrated = self.integrator.integrate(f, -1, 2, 31687)

        # Correct to 9 _significant_ digits
        self.assertEqual(1.62890552, round(integrated, 8))
