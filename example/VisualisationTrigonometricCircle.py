from CoordinateSystem import *
from math import pi, cos, sin


def get_circle_points(x):
    if -1 <= x <= 1:
        y_positive = math.sqrt(1 - x**2)
        y_negative = -y_positive
        return y_positive, y_negative
    else:
        return None


def get_circle_landmarks():
    i = -1
    circle_landmarks = Landmarks(landmarks=[])
    while i <= 1:
        circle_landmarks.landmarks.append(Landmark((i, get_circle_points(i)[0])))
        circle_landmarks.landmarks.append(Landmark((i, get_circle_points(i)[1])))
        i += 0.0001

    return circle_landmarks


def get_line_center_to_circle_point(angle):
    line = Landmarks([], draw_lines_between_points=True)
    line += Landmark(coordinate=(0, 0))
    line += Landmark(coordinate=(cos(angle), sin(angle)))

    return line


def get_info_landmarks(angle):
    cos_info = Landmark((cos(angle), 0), text=f"{round(cos(angle), 3)}", text_color=(255, 50, 0))
    sin_info = Landmark((0, sin(angle)), text=f"{round(sin(angle), 3)}", text_color=(250, 50, 0))

    return [cos_info, sin_info]


def sin_line(angle):
    if 0 <= cos(angle) <= 1:
        return Function(expression=lambda x: sin(angle) if 0 <= x <= cos(angle) else None, draw_lines_between_points=False, draw_points=True, trace_step=0.05)

    elif -1 <= cos(angle) <= 0:
        return Function(expression=lambda x: sin(angle) if cos(angle) <= x <= 0 else None, draw_lines_between_points=False, draw_points=True, trace_step=0.05)


def cos_line(angle):
    if 0 <= sin(angle) <= 1:
        return Function(expression=lambda x: cos(angle) if 0 <= x <= sin(angle) else None, draw_lines_between_points=False, draw_points=True, trace_step=0.05, swap_xy=True)

    elif -1 <= sin(angle) <= 0:
        return Function(expression=lambda x: cos(angle) if sin(angle) <= x <= 0 else None, draw_lines_between_points=False, draw_points=True, trace_step=0.05, swap_xy=True)


if __name__ == "__main__":
    x = pi/3 # change with the angle you want

    sys = CoordinateSystem([get_circle_landmarks(), get_line_center_to_circle_point(x), sin_line(x), cos_line(x), *get_info_landmarks(x)], (800, 800), -1.2, 1.2, 0.3, -1.2, 1.2, 0.5)

    sys.show(show_x_graduation_coordinate=True, show_y_graduation_coordinate=True, points_color_list=[(255, 0, 0)])
