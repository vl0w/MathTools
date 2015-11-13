from math import exp
from math import sqrt
from numerics.integration import SimpsonIntegrator
from numerics.derivation import *

f = lambda x: exp((-1) * (x ** 2))
integrator = SimpsonIntegrator()

print("SAM: " + str(integrator.integrate(f, -1, 2, 238)))

print("EXERCISE 1")
f = lambda x: exp((-1) * (x ** 2))
integrator = SimpsonIntegrator()
print("n\t\t\tsimpson integration\t\t\t\twith extrapolation")
print("-----------------------------------------------------------------------------------------------------")
for i in range(5, 11):
    n = 2 ** i

    integrated = integrator.integrate(f, -1, 2, n)
    integrated_extrapolation = integrator.extrapolate(f, -1, 2, n)
    print(str(n) + "\t\t\t" + str(integrated) + "\t\t\t" + str(integrated_extrapolation))

print()
print()

print("EXERCISE 2")
f = lambda x: exp(x)
forwardDifferentiator = ForwardDifferentiator()
backwardDifferentiator = BackwardDifferentiator()
centeredDifferentiator = CenteredDifferentiator()
print("n\t\tforward\t\t\t\t\tbackward\t\t\t\tcentered\t\t\t\trel. error (rounded)")
print("-----------------------------------------------------------------------------------------------------")
for i in range(0, 5):
    n = 2 ** i
    forw = forwardDifferentiator.differentiate(f, 0, h=10 ** -n)
    back = backwardDifferentiator.differentiate(f, 0, h=10 ** -n)
    cent = centeredDifferentiator.differentiate(f, 0, h=10 ** -n)
    relative_error_percent = round(abs((f(0) - cent) / f(0)) * 100, 10)
    print(str(n) + "\t\t" + str(forw) + "\t\t" + str(back) + "\t\t" + str(cent) + "\t\t" + str(
        relative_error_percent) + "%")

print()
print()

print("COMPARE: Normal vs. Extrapolation")
f = lambda x: exp(sqrt(x))
print("Normal\t\t\t\t\t\tExtrapolated\t\t\t\tdifference")
print("-------------------------------------------------------------------------------")
for i in range(1, 20):
    h = 10 ** -i
    d = centeredDifferentiator.differentiate(f, 1, h)
    d_e = centeredDifferentiator.extrapolate(f, 1, h)
    diff = abs(d_e - d)
    print(str(d) + "\t\t\t" + str(d_e) + "\t\t\t" + str(diff))
