from sympy import symbols, diff
from CoordinateSystem import *


var = symbols('x')
f_representation = var**2 + 2 * var - 1 # replace this by your function (replace x by 'var')
a = 1                                   # replace this by the wanted a


f_prime = diff(f_representation, var)

f_prime_of_a = f_prime.evalf(subs={var: a})
f_of_a = eval(str(f_representation), {"x": a})


def tang(x: float) -> float:
    return f_prime_of_a * (x - a) + f_of_a


def f(x: float) -> float:
    return eval(str(f_representation), {"x": x})

f_x = Function(expression=f, trace_step=0.01)
tangent = Function(expression=tang, trace_step=0.01)

system = CoordinateSystem([tangent, f_x], (650, 650), -10, 10, 2, -10, 10, 2)

system.show(show_x_graduation_coordinate=True, show_y_graduation_coordinate=True, win_title=f"visualisation of {str(f_representation)} and his tangent with a={a}")
