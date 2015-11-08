from numerics.solvers import *

###
### EXERCISE 5
###
c = parse_matrix("12 7 3;1 5 1;2 7 -11")
b = parse_matrix("2 -5 6").transpose()

print("EXERCISE 5")
print("-----------")
print("(all results are transposed)")
print("Gaussian elimination       : " + str(gaussian_elimination(c, b).transpose()))
print("Gauss-Seidel               : " + str(gauss_seidel_iteration(c, b).transpose()))
print("Jacobi                     : " + str(jacobi_iteration(c, b).transpose()))

print("")

###
### EXERCISE 6
###
### c is already adjusted (derivation on papers)
### here is the proof that gauss-seidel converges with the adjusted equations
c = parse_matrix("5 1 1;3 6 3;0 3 -13")
b = parse_matrix("27 -15 16").transpose()

print("EXERCISE 6")
print("-----------")
print("(all results are transposed)")
print("Gauss-Seidel               : " + str(gauss_seidel_iteration(c, b).transpose()))
