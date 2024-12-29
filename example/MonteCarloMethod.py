import random
from CoordinateSystem import *
import math


def quarter_circle(x: float) -> float:
    """
    Return y for a given value of x
    on the circle defined by x^2 + y^2 = 1, considering only y > 0.

    :param x: The x-coordinate (must be in [0, 1])
    :return: y for the given x
    """
    if 0 <= x <= 1:
        y = math.sqrt(1 - x ** 2)
        return y


def is_point_in_circle(x: float, y: float) -> bool:
    """
    Check if a point (x, y) is inside a circle with a radius of 1 centered at the origin.
    :param x: x
    :param y: y
    :return: True or False
    """

    return x**2 + y**2 <= 1


def get_random_points(loop: int) -> list:
    """
    generate random a list of CoordinateSystem.Landmark
    :param loop: number of random points
    :return: a list of random Landmark
    """

    return [Landmark((random.uniform(0, 1), random.uniform(0, 1))) for _ in range(loop)]


def get_points_in_circle(points: list) -> int:
    """.
    number of Landmark in the circle in the list
    :param points: list of random Landmark
    :return: number of Landmark in the circle in the list
    """
    number_of_points_in_circle = []
    for landmark in points:
        number_of_points_in_circle.append(is_point_in_circle(landmark.x, landmark.y))

    return number_of_points_in_circle.count(True)


def pi_by_montecarlo_method(len_points_in_circle: int, len_points: int) -> float:
    """
    approximated pi by the formula of montecarlo
    :param len_points_in_circle: number of points in the circle
    :param len_points: number total of points in the square
    :return: approximated pi by the formula of montecarlo
    """
    return 4 * (len_points_in_circle/len_points)


nbr_points = 2
random_points = get_random_points(nbr_points)
points_in_circle = get_points_in_circle(random_points)
approximated_pi = pi_by_montecarlo_method(len_points_in_circle=points_in_circle, len_points=len(random_points))
print(approximated_pi)

circle = Function(quarter_circle, trace_step=0.001)
square_delimiter = Vector((0, 1), (1, 0), draw_arrow=False, draw_lines_between_points=True)
square_delimiter2 = Vector((1, 0), (0, 1), draw_arrow=False, draw_lines_between_points=True)

system = CoordinateSystem([*random_points, square_delimiter, square_delimiter2, circle], (700, 700), -0.1, 1.1, 1, -0.1, 1.1, 1)
points_color = []
for i in range(nbr_points):
    points_color.append([0, 0, 0])

points_color += [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

system.show(show_x_graduation_coordinate=True, show_y_graduation_coordinate=True, points_color_list=points_color)
