import sympy as sp

def solve_homogeneous(deg, coeffs, init_conds):
    n = sp.symbols("n")
    x = sp.symbols("x")

    char_poly = x**deg
    for i in range(deg):
        char_poly -= x**(deg - i - 1) * coeffs[i]

    roots = sp.solve(char_poly, x)
    terms = []
    undetermined_coeffs = [sp.symbols(f"c{i}") for i in range(deg)]

    for i, root in enumerate(roots):
        terms.append(root**n * undetermined_coeffs[i])

    sol = sum(terms)
    eqs = [sol.subs(n, i) - init_conds[i] for i in range(deg)]
    coeffs_solution = sp.solve(eqs, undetermined_coeffs)

    return sol, sol.subs(coeffs_solution)

def find_particular_solution(deg, coeffs, g_n):
    n = sp.symbols("n")
    a_n = sp.Function('a')(n)
    recurrence_rel = a_n - sum(coeffs[i] * a_n.subs(n, n - i - 1) for i in range(deg)) - g_n
    return sp.rsolve(recurrence_rel, a_n)