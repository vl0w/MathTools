from unittest import TestCase
from numerics.derivation import ForwardDifferentiator, BackwardDifferentiator, CenteredDifferentiator


class TestDerivation(TestCase):
    centered = CenteredDifferentiator()
    forward = ForwardDifferentiator()
    backward = BackwardDifferentiator()

    def test_derive_linear_function(self):
        f = lambda x: 2 * x

        for i in range(20):
            roundedCentered = round(self.centered.differentiate(f, i), 5)
            roundedForward = round(self.forward.differentiate(f, i), 5)
            roundedBackward = round(self.backward.differentiate(f, i), 5)
            self.assertEqual(2, roundedCentered)
            self.assertEqual(2, roundedForward)
            self.assertEqual(2, roundedBackward)