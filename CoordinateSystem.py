from tkinter import Tk, messagebox
import pygame
import math


class Function:
    def __init__(self, expression, trace_step: float = 0.1, draw_points: bool = False,
                 draw_lines_between_points: bool = True):
        self.expression = expression

        self.trace_step = trace_step
        self.draw_points = draw_points
        self.draw_lines_between_points = draw_lines_between_points

        if trace_step < 0:
            raise ValueError("trace_step must be >= 0")

        if type(draw_points) is not bool:
            raise TypeError(f"draw_points must be True or False not {type(draw_points)}")

        if type(draw_lines_between_points) is not bool:
            raise TypeError(f"draw_lines_between_points must be True or False not {type(draw_lines_between_points)}")

    def get_images(self, start: int, stop: int, step: float, errors_dict: dict = None) -> dict[int: float]:
        images = {}
        x = start
        errors_dict.setdefault(self.expression.__name__, [])
        while x <= stop:
            try:
                image = self.expression(x)
                if type(image) is not complex:
                    images[x] = image
                elif type(errors_dict) is dict and not any(
                        "Result Is Complex Number" in values for values in errors_dict.values()):
                    errors_dict[f"{self.expression.__name__}"].append("Result Is Complex Number")


            except (ZeroDivisionError, ValueError, OverflowError) as e:
                if type(errors_dict) is dict and not any(str(e) in values for values in errors_dict.values()):
                    errors_dict[f"{self.expression.__name__}"].append(str(e))

            x += step

        return images


class Sequence:
    def __init__(self, formula, n_min: int = 0, trace_step: int = 1, draw_points: bool = True,
                 draw_lines_between_points: bool = False):
        self.formula = formula

        self.trace_step = trace_step
        self.draw_points = draw_points
        self.draw_lines_between_points = draw_lines_between_points
        self.n_min = n_min
        if n_min < 0:
            raise ValueError("n_min must be >= 0")

        if type(trace_step) is not int:
            raise TypeError(f"trace_step must be int for Sequence (not {type(trace_step)})")

        if trace_step < 0:
            raise ValueError("trace_step must be >= 0")

        if type(draw_points) is not bool:
            raise TypeError(f"draw_points must be True or False not {type(draw_points)}")

        if type(draw_lines_between_points) is not bool:
            raise TypeError(f"draw_lines_between_points must be True or False not {type(draw_lines_between_points)}")

    def get_terms(self, start: int, stop: int, step: int, errors_dict: dict = None) -> dict[int: float]:
        terms = {}
        param_for_loop = []
        errors_dict.setdefault(self.formula.__name__, [])

        for i in {start: "start", stop: "stop", step: "step"}.items():
            if type(i[0]) is int:
                param_for_loop.append(i[0])
            else:
                if type(errors_dict) is dict:
                    errors_dict[f"{self.formula.__name__}"].append(f"{i[1]} transformed in int ({i[0]} to {int(i[0])})")

                param_for_loop.append(int(i[0]))

        for x in range(*param_for_loop):
            try:
                term = self.formula(x)
                if type(term) is not complex:
                    terms[x] = term

                elif type(errors_dict) is dict and not any(
                        "Result Is Complex Number" in values for values in errors_dict.values()):
                    errors_dict[f"{self.formula.__name__}"].append("Result Is Complex Number")

            except (ZeroDivisionError, ValueError, OverflowError) as e:
                if type(errors_dict) is dict and not any(str(e) in values for values in errors_dict.values()):
                    errors_dict[f"{self.formula.__name__}"].append(str(e))

        return terms


class Vector:
    def __init__(self, coordinate: tuple, start_coordinate: tuple = (0, 0), draw_arrow: bool = True,
                 draw_points: bool = False, draw_lines_between_points: bool = False):

        if type(draw_arrow) is not bool:
            raise TypeError(f"draw_arrow must be True or False not {type(draw_arrow)}")
        if type(draw_points) is not bool:
            raise TypeError(f"draw_points must be True or False not {type(draw_points)}")
        if type(draw_lines_between_points) is not bool:
            raise TypeError(f"draw_lines_between_points must be True or False not {type(draw_lines_between_points)}")

        self.draw_arrow = draw_arrow
        self.draw_points = draw_points
        self.draw_lines_between_points = draw_lines_between_points

        self.x, self.y = coordinate

        self.start_coordinate = start_coordinate
        self.end_coordinate = coordinate

    def get_points(self):
        points = {self.start_coordinate[0]: self.start_coordinate[1],
                  self.start_coordinate[0] + self.x: self.start_coordinate[1] + self.y}

        return points


    def operation(self, sign: str, other):
        if isinstance(other, Vector):
            x = eval(f"{self.x}{sign}{other.x}")
            y = eval(f"{self.y}{sign}{other.y}")

            return Vector(coordinate=(x, y), draw_arrow=self.draw_arrow,
                          draw_points=self.draw_points, draw_lines_between_points=self.draw_lines_between_points)

    def __add__(self, other):
        return self.operation(sign="+", other=other)

    def __sub__(self, other):
        return self.operation(sign="-", other=other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(coordinate=(self.x * other, self.y * other), draw_arrow=self.draw_arrow,
                          draw_points=self.draw_points, draw_lines_between_points=self.draw_lines_between_points)

        return self.operation(sign="*", other=other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(coordinate=(self.x / other, self.y / other), start_coordinate=self.start_coordinate, draw_arrow=self.draw_arrow,
                          draw_points=self.draw_points, draw_lines_between_points=self.draw_lines_between_points)

        return self.operation(sign="/", other=other)

    def __pos__(self):
        return Vector(coordinate=(+self.x, +self.y), draw_arrow=self.draw_arrow,
                      draw_points=self.draw_points, draw_lines_between_points=self.draw_lines_between_points)

    def __neg__(self):
        return Vector(coordinate=(-self.x, -self.y), draw_arrow=self.draw_arrow,
                      draw_points=self.draw_points, draw_lines_between_points=self.draw_lines_between_points)

    def __repr__(self):
        return f"Vector(x={self.x} ; y={self.y}) starting at (x={self.start_coordinate[0]} ; y={self.start_coordinate[1]})"


class FunctionEvaluatingError(Exception):
    def __init__(self, error):
        self.message = f"Error while evaluating the function : \n {error}"


class CoordinateSystem:
    def __init__(self, graph_elements: list, screen_size: tuple, x_min: float, x_max: float, x_graduation_step: float,
                 y_min: float, y_max: float, y_graduation_step: float):
        self.width, self.height = screen_size

        if x_min >= x_max:
            raise ValueError(f"x_min ({x_min}) must be less than x_max ({x_max})")

        if y_min >= y_max:
            raise ValueError(f"y_min ({y_min}) must be less than y_max ({y_max})")

        if x_graduation_step < 0:
            raise ValueError("x_graduation_step must be >= 0 (0 for no graduation)")

        if y_graduation_step < 0:
            raise ValueError("y_graduation_step must be >= 0 (0 for no graduation)")

        if not isinstance(graph_elements, list):
            raise TypeError(f"graph_elements must be a list, not {type(graph_elements)}")

        if self.width < 0 or self.height < 0:
            raise ValueError("screen dimensions must be non-negative")

        self.graph_elements = graph_elements

        self.x_min = x_min
        self.x_max = x_max
        self.x_graduation_step = x_graduation_step

        self.y_min = y_min
        self.y_max = y_max
        self.y_graduation_step = y_graduation_step

        self.graduation_coordinate = []

        self.screen = None

        self.len_x_axis = abs(self.x_max - self.x_min)
        self.len_y_axis = abs(self.y_max - self.y_min)

        self.x_coordinate_yaxis = self.width * (-self.x_min) / self.len_x_axis
        self.y_coordinate_xaxis = self.height * (1 - (- self.y_min) / self.len_y_axis)

        self.ignored_error = {}

        print("system init")

    def get_x_axis_pos(self) -> list[tuple[float, float], tuple[float, float]]:
        start_pos = (0, self.y_coordinate_xaxis)
        end_pos = (self.width, self.y_coordinate_xaxis)

        return [start_pos, end_pos]

    def get_y_axis_pos(self) -> list[tuple[float, float], tuple[float, float]]:
        start_pos = (self.x_coordinate_yaxis, 0)
        end_pos = (self.x_coordinate_yaxis, self.height)

        return [start_pos, end_pos]

    def draw_axes(self, axes_color: tuple):
        x_axis_pos = self.get_x_axis_pos()
        y_axis_pos = self.get_y_axis_pos()

        pygame.draw.line(self.screen, axes_color, y_axis_pos[0], y_axis_pos[1])
        pygame.draw.line(self.screen, axes_color, x_axis_pos[0], x_axis_pos[1])

    def get_position_from_coordinate(self, coordinate: tuple) -> tuple:  # position = pixel | coordinate = x_min < coor < x_max
        x_coordinate, y_coordinate = coordinate

        x_position = (x_coordinate - self.x_min) / (self.x_max - self.x_min) * self.width
        y_position = self.height * (1 - (y_coordinate - self.y_min) / self.len_y_axis)

        return x_position, y_position

    def get_coordinate_from_position(self, point: tuple) -> tuple:  # position = pixel | coordinate = x_min < coor < x_max
        x_position, y_position = point

        x_coordinate = (x_position / self.width) * (self.x_max - self.x_min) + self.x_min
        y_coordinate = self.y_min + (1 - y_position / self.height) * self.len_y_axis

        return x_coordinate, y_coordinate

    def get_x_graduations(self, show_x_graduation_coordinate: bool) -> list:
        if self.x_graduation_step == 0:
            return []

        graduations = []

        x_grad = 0
        while x_grad <= self.x_max:
            x, y = self.get_position_from_coordinate((x_grad, 0))
            graduations.append((x, y))

            if show_x_graduation_coordinate:
                self.graduation_coordinate.append([(x, y + 10), x_grad])

            x_grad += self.x_graduation_step

        x_grad = 0
        while x_grad >= self.x_min:
            x, y = self.get_position_from_coordinate((x_grad, 0))
            graduations.append((x, y))

            if show_x_graduation_coordinate:
                self.graduation_coordinate.append([(x, y + 10), x_grad])

            x_grad -= self.x_graduation_step

        return graduations

    def get_y_graduations(self, show_y_graduation_coordinate: bool) -> list:
        if self.y_graduation_step == 0:
            return []

        graduations = []
        y_grad = 0
        while y_grad <= self.y_max:
            x, y = self.get_position_from_coordinate((0, y_grad))
            graduations.append((x, y))

            if show_y_graduation_coordinate:
                self.graduation_coordinate.append([(x - 10, y), y_grad])

            y_grad += self.y_graduation_step

        y_grad = 0
        while y_grad >= self.y_min:
            x, y = self.get_position_from_coordinate((0, y_grad))
            graduations.append((x, y))

            if show_y_graduation_coordinate:
                self.graduation_coordinate.append([(x - 10, y), y_grad])

            y_grad -= self.y_graduation_step

        return graduations

    def draw_graduations(self, x_graduation: list, y_graduation: list, graduation_color: tuple):
        for i in x_graduation:
            x, y = i
            pygame.draw.line(self.screen, graduation_color, (x, y - 5), (x, y + 5))

        for i in y_graduation:
            x, y = i
            pygame.draw.line(self.screen, graduation_color, (x - 5, y), (x + 5, y))

        if len(self.graduation_coordinate) > 0:
            font = pygame.font.Font(None, 20)
            for i in self.graduation_coordinate:
                coordinate = i[0]
                text = i[1]

                text_surface = font.render(str(text), True, graduation_color)
                text_rect = text_surface.get_rect(center=coordinate)

                self.screen.blit(text_surface, text_rect)

    def get_curve_points(self, element) -> list:
        try:
            if type(element) is Function:
                points_coordinate = element.get_images(start=self.x_min, stop=self.x_max, step=element.trace_step,
                                                       errors_dict=self.ignored_error)
            elif type(element) is Sequence:
                points_coordinate = element.get_terms(start=element.n_min, stop=self.x_max, step=element.trace_step,
                                                      errors_dict=self.ignored_error)
            elif type(element) is Vector:
                points_coordinate = element.get_points()

        except Exception as e:
            pygame.quit()
            raise FunctionEvaluatingError(e)

        points = []

        for x, y in points_coordinate.items():
            points.append(self.get_position_from_coordinate((x, y)))

        return points

    def draw_arrow(self, color, start_pos, end_pos, arrow_width=3, arrow_length=7):

        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])

        arrow_tip = end_pos

        left = (end_pos[0] - arrow_length * math.cos(angle - math.pi / 6),
                end_pos[1] - arrow_length * math.sin(angle - math.pi / 6))
        right = (end_pos[0] - arrow_length * math.cos(angle + math.pi / 6),
                 end_pos[1] - arrow_length * math.sin(angle + math.pi / 6))

        pygame.draw.line(self.screen, color, start_pos, end_pos, arrow_width)
        pygame.draw.polygon(self.screen, color, [arrow_tip, left, right])

    def draw_curve(self, points: list, points_color: tuple, element) -> None:
        index_counter = 0
        for point_position in points:
            if type(element) is Vector and element.draw_arrow:
                self.draw_arrow(color=points_color, start_pos=points[0], end_pos=points[1])

            if element.draw_points:
                x, y = point_position
                pygame.draw.circle(self.screen, points_color, (x, y), 2)

            if element.draw_lines_between_points and index_counter < len(points) - 1:
                pygame.draw.line(self.screen, points_color, point_position, points[index_counter + 1], 3)
                index_counter += 1

    def get_mouse_coordinate(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_coor = self.get_coordinate_from_position(mouse_pos)
        mouse_coor = round(mouse_coor[0], 1), round(mouse_coor[1], 1)

        font = pygame.font.Font(None, 20)
        text_surface = font.render(str(mouse_coor), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.width - 40, 10))

        return text_surface, text_rect

    def show_ignored_errors(self):
        list_error = ""
        for error in self.ignored_error.items():
            list_error += f"- element {error[0]} : \n"

            for i in error[1]:
                list_error += f"  - {i}\n"

        messagebox_root = Tk()
        messagebox_root.withdraw()

        messagebox.showinfo("ignored error while calculating the points",
                            f"ignored error (the associated point will not be displayed) :\n{list_error}")

        messagebox_root.destroy()

    def show(self, background_color: tuple = (255, 255, 255), points_color_list: list = None, axes_color: tuple = (0, 0, 0),
             graduation_color: tuple = (0, 0, 0), show_x_graduation_coordinate: bool = False, show_y_graduation_coordinate: bool = False, show_coordinate: bool = False, win_title: str = "",
             show_ignored_error: bool = False):

        if points_color_list is None:
            points_color_list = [(0, 0, 0), (0, 0, 255), (255, 0, 0),
                                 (0, 255, 0), (255, 192, 203), (255, 165, 0),
                                 (139, 69, 19), (0, 255, 255)
                                 ]

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(win_title)
        running = True

        print("getting x graduation ...")
        x_grad = self.get_x_graduations(show_x_graduation_coordinate)

        print("getting y graduation...")
        y_grad = self.get_y_graduations(show_y_graduation_coordinate)

        print("getting images and points")
        curves_points = []
        for element in self.graph_elements:
            curves_points.append([element, self.get_curve_points(element=element)])

        if show_ignored_error and any(len(values) > 0 for values in self.ignored_error.values()):
            self.show_ignored_errors()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(background_color)

            self.draw_axes(axes_color)
            self.draw_graduations(x_grad, y_grad, graduation_color)

            for color_index, (element, points) in enumerate(curves_points):
                self.draw_curve(points=points, points_color=points_color_list[color_index], element=element)

            if show_coordinate:
                text = self.get_mouse_coordinate()
                self.screen.blit(text[0], text[1])

            pygame.display.update()

        pygame.quit()
