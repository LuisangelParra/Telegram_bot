import sympy as sp
from RRLNHCCC.RR import solve_homogeneous, find_particular_solution
from RRLNHCCC.Tools.latex_image import latex_image
import pylab


def RR_SHOW(degree, coefficients, initial_conditions, g_n):
    #degree = int(input("Digite el grado de la funcion: "))
    #coefficients = [int(input(f"Digite el coeficiente de f(n-{i + 1}): ")) for i in range(degree)]
    #initial_conditions = [int(input(f"Digite el valor de f({i}): ")) for i in range(degree)]
    
    homogeneous_sol_unsolved, homogeneous_sol_solved = solve_homogeneous(int(degree), coefficients, initial_conditions)
    particular_sol = find_particular_solution(int(degree), coefficients, g_n)
    fn_unsolved = homogeneous_sol_unsolved + particular_sol
    fn_solved = homogeneous_sol_solved + particular_sol

    
    

    fcr = "f(n) = " + sp.latex(sp.simplify(fn_unsolved))
    fcnr = "f(n) = " + sp.latex(sp.simplify(fn_solved))

    formula = r'$ %s $' % (fcr)

    fig = pylab.figure()
    text = fig.text(0, 0, formula)

    # Saving the figure will render the text.
    dpi = 100
    fig.savefig('generated_images/formula1.png', dpi=dpi)

    # Now we can work with text's bounding box.
    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.005
    height = height*3
    # Adjust the figure size so it can hold the entire text.
    fig.set_size_inches((width, height))

    # Adjust text's vertical position.
    dy = (height/2)

    text.set_position((0, dy))

    # Save the adjusted text.
    fig.savefig('generated_images/formula1.png', dpi=dpi)



    formula2 = r'$ %s $' % (fcnr)

    fig2 = pylab.figure()
    text2 = fig2.text(0, 0, formula2)

    # Saving the figure will render the text.
    fig2.savefig('generated_images/formula2.png', dpi=dpi)

    # Now we can work with text's bounding box.
    fig2.set_size_inches((width, height))

    # Adjust text's vertical position.
    text2.set_position((0, dy))

    # Save the adjusted text.
    fig2.savefig('generated_images/formula2.png', dpi=dpi)


