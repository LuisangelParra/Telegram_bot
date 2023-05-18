import sympy as sp
from RRLNHCCC.RR import solve_homogeneous, find_particular_solution
from RRLNHCCC.Tools.latex_image import latex_image


def RR_SHOW(degree, coefficients, initial_conditions, g_n):
    #degree = int(input("Digite el grado de la funcion: "))
    #coefficients = [int(input(f"Digite el coeficiente de f(n-{i + 1}): ")) for i in range(degree)]
    #initial_conditions = [int(input(f"Digite el valor de f({i}): ")) for i in range(degree)]
    
    homogeneous_sol_unsolved, homogeneous_sol_solved = solve_homogeneous(int(degree), coefficients, initial_conditions)
    particular_sol = find_particular_solution(int(degree), coefficients, g_n)
    fn_unsolved = homogeneous_sol_unsolved + particular_sol
    fn_solved = homogeneous_sol_solved + particular_sol

    fcr = sp.latex("f(n) = ") + sp.latex(sp.simplify(fn_unsolved))
    fcnr = sp.latex("f(n) = ") + sp.latex(sp.simplify(fn_solved))

    #print("\n\n Funcion No Recurrente (con constantes no resueltas)")
    #display_result(sp.latex("f(n) = ") + sp.latex(sp.simplify(fn_unsolved)))
    #print("\n\n Funcion No Recurrente (con constantes resueltas)")
    #display_result(sp.latex("f(n) = ") + sp.latex(sp.simplify(fn_solved)))
    latex_image(fcr, fcnr)



