import pygame
import math


class Element:
    def __init__(self, trace_step: float = 0.0, draw_points: bool = True, draw_lines_between_points: bool = False, swap_xy: bool = False):
        self.trace_step = trace_step
        self.draw_points = draw_points
        self.draw_lines_between_points = draw_lines_between_points
        self.swap_xy = swap_xy

        if trace_step < 0:
            raise ValueError("trace_step must be >= 0")

        if type(draw_points) is not bool:
            raise TypeError(f"draw_points must be True or False not {type(draw_points)}")

        if type(draw_lines_between_points) is not bool:
            raise TypeError(f"draw_lines_between_points must be True or False not {type(draw_lines_between_points)}")

        if type(swap_xy) is not bool:
            raise TypeError(f"swap_xy must be True or False not {type(swap_xy)}")


class Function(Element):
    def __init__(self, expression, trace_step: float = 0.1, draw_points: bool = False,
                 draw_lines_between_points: bool = True, swap_xy: bool = False):
        super().__init__(trace_step=trace_step, draw_points=draw_points,
                         draw_lines_between_points=draw_lines_between_points, swap_xy=swap_xy)

        self.expression = expression
        self.expression_name = expression.__name__

    def get_images(self, start: int, stop: int, step: float, errors_dict: dict = None) -> list[float, float, ...]:
        images = []
        x = start
        errors_dict.setdefault(self.expression_name, [])
        while x <= stop:
            try:
                image = self.expression(x)
                if image is None:
                    raise ValueError("Result Is None")

                if isinstance(image, complex):
                    raise ValueError("Result Is Complex Number")

                if not self.swap_xy:
                    images.append((x, image))
                else:
                    images.append((image, x))

            except (ZeroDivisionError, ValueError, OverflowError, TypeError) as e:
                if isinstance(errors_dict, dict) and not any(str(e) in values for values in errors_dict.values()):
                    errors_dict[f"{self.expression_name}"].append(str(e))

            x += step

        return images

    def __repr__(self):
        return f"Function(expression_name={self.expression_name})"



class Sequence(Element):
    def __init__(self, formula, n_min: int = 0, trace_step: int = 1, draw_points: bool = True,
                 draw_lines_between_points: bool = False):

        super().__init__(trace_step=trace_step, draw_points=draw_points,
                         draw_lines_between_points=draw_lines_between_points)

        self.formula = formula
        self.formula_name = formula.__name__

        self.n_min = n_min
        if n_min < 0:
            raise ValueError("n_min must be >= 0")

        if type(trace_step) is not int:
            raise TypeError(f"trace_step must be int for Sequence (not {type(trace_step)})")

    def get_terms(self, start: int, stop: int, step: int, errors_dict: dict = None) -> list:
        terms = []
        param_for_loop = []
        errors_dict.setdefault(self.formula_name, [])
        stop += 1 # for the for loop
        for i in {start: "start", stop: "stop", step: "step"}.items():
            if type(i[0]) is int:
                param_for_loop.append(i[0])
            else:
                if type(errors_dict) is dict:
                    errors_dict[f"{self.formula_name}"].append(f"{i[1]} transformed in int ({i[0]} to {int(i[0])})")

                param_for_loop.append(int(i[0]))

        for x in range(*param_for_loop):
            try:
                term = self.formula(x)
                if isinstance(term, complex):
                    raise ValueError("Result Is Complex Number")

                if term is None:
                    raise ValueError("Result Is None")

                terms.append((x, term))
            except (ZeroDivisionError, ValueError, OverflowError) as e:
                if type(errors_dict) is dict and not any(str(e) in values for values in errors_dict.values()):
                    errors_dict[f"{self.formula_name}"].append(str(e))

        return terms

    def __repr__(self):
        return f"Sequence(formula_name={self.formula_name})"


class Vector(Element):
    def __init__(self, coordinate: tuple, start_coordinate: tuple = (0, 0), draw_arrow: bool = True,
                 draw_points: bool = False, draw_lines_between_points: bool = False):
        super().__init__(draw_points=draw_points, draw_lines_between_points=draw_lines_between_points, trace_step=0)

        if type(draw_arrow) is not bool:
            raise TypeError(f"draw_arrow must be True or False not {type(draw_arrow)}")

        self.draw_arrow = draw_arrow

        self.x, self.y = coordinate

        self.start_coordinate = start_coordinate
        self.end_coordinate = coordinate

    def get_points(self) -> list:
        points = [(self.start_coordinate[0], self.start_coordinate[1]),
                  (self.start_coordinate[0] + self.x, self.start_coordinate[1] + self.y)]

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
            return Vector(coordinate=(self.x / other, self.y / other), start_coordinate=self.start_coordinate,
                          draw_arrow=self.draw_arrow,
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


class Landmark(Element):
    def __init__(self, coordinate: tuple, text: str = None, text_color: tuple = (0, 0, 0),
                 text_placement: str = "bottomright"):
        super().__init__()

        if not isinstance(coordinate, (tuple, list)):
            raise TypeError(f"coordinate must be tuple or list not {type(coordinate)}")

        if not isinstance(text, (str, type(None))):
            raise TypeError(f"text must be str or None not {type(text)}")

        if not isinstance(text_color, (tuple, list)):
            raise TypeError(f"text_color must be tuple or list not {type(text_color)}")

        possible_placement = {"bottomright": "topleft", "midbottom": "midtop", "midtop": "midbottom",
                              "topleft": "bottomright", "bottomleft": "topright", "topright": "bottomleft"}
        if text_placement not in possible_placement.keys():
            raise ValueError(
                f"text_placement must be 'topleft', 'midtop', 'midbottom', 'bottomright', 'topright' or 'bottomleft' not {text_placement}")

        for item in possible_placement.items():
            if text_placement == item[1]:
                self.rect_placement = item[0]

        self.coordinate = coordinate
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.text = text
        self.text_color = text_color
        self.placement = text_placement

    def get_mark_coordinate(self, x_min: float, x_max: float) -> list:
        if x_min <= self.x <= x_max:
            return [(self.x, self.y)]

    def __add__(self, other):
        if isinstance(other, Landmark):
            return Landmarks([self, other])

        elif isinstance(other, Landmarks):
            other.landmarks.append(self)
            return other

    def __repr__(self):
        return f"Landmark(x={self.x} ; y={self.y} ; text='{self.text}' ; placement='{self.placement}')"


class Landmarks(Element):
    def __init__(self, landmarks: list, draw_lines_between_points=False):
        super().__init__(draw_lines_between_points=draw_lines_between_points)
        for landmark in landmarks:
            if not isinstance(landmark, Landmark):
                raise TypeError(f"landmark in landmarks must be Landmark not {type(landmark)}")

        self.landmarks = landmarks

    def get_mark_coordinate(self, x_min: float, x_max: float) -> list:
        marks = []
        for landmark in self.landmarks:
            if x_min <= landmark.x <= x_max:
                marks.append((landmark.x, landmark.y))

        return marks

    def __add__(self, other):
        if isinstance(other, Landmark):
            self.landmarks.append(other)
            return self

        elif isinstance(other, Landmarks):
            self.landmarks += other.landmarks
            return self


class ElementEvaluatingError(Exception):
    def __init__(self, error):
        self.message = f"Error while evaluating the Element : \n {error}"


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

        for element in graph_elements:
            if not isinstance(element, Element):
                raise TypeError(
                    f"element in graph_elements must be Function, Vector, Sequence or Landmark(s). Not {type(element)}")

        self.graph_elements = graph_elements

        self.x_min = x_min
        self.x_max = x_max
        self.x_graduation_step = x_graduation_step

        self.y_min = y_min
        self.y_max = y_max
        self.y_graduation_step = y_graduation_step

        self.initial_limit = [x_min, x_max, y_min, y_max]

        self.graduation_coordinate = []

        self.screen = pygame.Surface(screen_size)

        self.len_x_axis = abs(self.x_max - self.x_min)
        self.len_y_axis = abs(self.y_max - self.y_min)

        self.x_coordinate_yaxis = self.width * (-self.x_min) / self.len_x_axis
        self.y_coordinate_xaxis = self.height * (1 - (- self.y_min) / self.len_y_axis)

        self.ignored_error = {}

        self.getting_points = bool

        self.zoom_mode = bool

        self.zoom_x1 = float
        self.zoom_x2 = float

        self.zoom_y1 = float
        self.zoom_y2 = float

        self.first_point = bool
        self.first_point_position = tuple

        self.curves_points = list

        self.x_grad = list
        self.y_grad = list

        self.mouse_pos = tuple
        self.actual_cursor = int

        pygame.font.init()
        self.font = pygame.font.Font(None, 20)

        print("system init")

    def set_axes_info(self) -> None:
        self.len_x_axis = abs(self.x_max - self.x_min)
        self.len_y_axis = abs(self.y_max - self.y_min)

        self.x_coordinate_yaxis = self.width * (-self.x_min) / self.len_x_axis
        self.y_coordinate_xaxis = self.height * (1 - (- self.y_min) / self.len_y_axis)

    def get_x_axis_position(self) -> list[tuple[float, float], tuple[float, float]]:
        start_pos = (0, self.y_coordinate_xaxis)
        end_pos = (self.width, self.y_coordinate_xaxis)

        return [start_pos, end_pos]

    def get_y_axis_position(self) -> list[tuple[float, float], tuple[float, float]]:
        start_pos = (self.x_coordinate_yaxis, 0)
        end_pos = (self.x_coordinate_yaxis, self.height)

        return [start_pos, end_pos]

    def draw_axes(self, axes_color: tuple, show_x_axis: bool, show_y_axis: bool) -> None:
        if show_x_axis:
            x_axis_pos = self.get_x_axis_position()
            pygame.draw.line(self.screen, axes_color, x_axis_pos[0], x_axis_pos[1])
        if show_y_axis:
            y_axis_pos = self.get_y_axis_position()
            pygame.draw.line(self.screen, axes_color, y_axis_pos[0], y_axis_pos[1])

    def get_position_from_coordinate(self,
                                     coordinate: tuple) -> tuple:  # position = pixel | coordinate = x_min < coordinate < x_max
        x_coordinate, y_coordinate = coordinate

        x_position = (x_coordinate - self.x_min) / (self.x_max - self.x_min) * self.width
        y_position = self.height * (1 - (y_coordinate - self.y_min) / self.len_y_axis)

        return x_position, y_position

    def get_coordinate_from_position(self,
                                     point: tuple) -> tuple:  # position = pixel | coordinate = x_min < coordinate < x_max
        x_position, y_position = point

        x_coordinate = (x_position / self.width) * (self.x_max - self.x_min) + self.x_min
        y_coordinate = self.y_min + (1 - y_position / self.height) * self.len_y_axis

        return x_coordinate, y_coordinate

    def get_x_graduations(self, show_x_graduation_coordinate: bool) -> list:
        if self.x_graduation_step == 0:
            return []

        graduations = []
        x_grad = math.ceil(self.x_min / self.x_graduation_step) * self.x_graduation_step

        while x_grad <= self.x_max:
            x, y = self.get_position_from_coordinate((x_grad, 0))
            graduations.append((x, y))

            if show_x_graduation_coordinate:
                self.graduation_coordinate.append([(x, y + 10), x_grad])

            x_grad += self.x_graduation_step

        return graduations

    def get_y_graduations(self, show_y_graduation_coordinate: bool) -> list:
        if self.y_graduation_step == 0:
            return []

        graduations = []
        y_grad = math.ceil(self.y_min / self.y_graduation_step) * self.y_graduation_step

        while y_grad <= self.y_max:
            x, y = self.get_position_from_coordinate((0, y_grad))
            graduations.append((x, y))

            if show_y_graduation_coordinate:
                self.graduation_coordinate.append([(x - 10, y), y_grad])

            y_grad += self.y_graduation_step

        return graduations

    def draw_graduations(self, x_graduation: list, y_graduation: list, graduation_color: tuple) -> None:
        for i in x_graduation:
            x, y = i
            pygame.draw.line(self.screen, graduation_color, (x, y - 5), (x, y + 5))

        for i in y_graduation:
            x, y = i
            pygame.draw.line(self.screen, graduation_color, (x - 5, y), (x + 5, y))

        for i in self.graduation_coordinate:
            coordinate = i[0]
            text = i[1]

            text_surface = self.font.render(str(round(text, 2)), True, graduation_color)
            text_rect = text_surface.get_rect(center=coordinate)

            self.screen.blit(source=text_surface, dest=text_rect)

    def get_curve_points(self, element) -> list:
        try:
            if type(element) is Function:
                if element.swap_xy:
                    points_coordinate = element.get_images(start=self.y_min, stop=self.y_max, step=element.trace_step,
                                                           errors_dict=self.ignored_error)
                else:
                    points_coordinate = element.get_images(start=self.x_min, stop=self.x_max, step=element.trace_step,
                                                           errors_dict=self.ignored_error)
            elif type(element) is Sequence:
                points_coordinate = element.get_terms(start=element.n_min, stop=self.x_max, step=element.trace_step,
                                                      errors_dict=self.ignored_error)
            elif type(element) is Vector:
                points_coordinate = element.get_points()

            elif isinstance(element, (Landmarks, Landmark)):
                points_coordinate = element.get_mark_coordinate(x_min=self.x_min, x_max=self.x_max)



        except Exception as e:
            pygame.quit()
            raise ElementEvaluatingError(e)

        points = []
        for x, y in points_coordinate:
            points.append(self.get_position_from_coordinate((x, y)))

        return points

    def draw_arrow(self, color, start_pos, end_pos, arrow_width=3, arrow_length=7) -> None:

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
            if element.draw_points:
                x, y = point_position
                point = pygame.draw.circle(self.screen, points_color, (x, y), 2)

            if element.draw_lines_between_points and index_counter < len(points) - 1:
                pygame.draw.line(self.screen, points_color, point_position, points[index_counter + 1], 3)
                index_counter += 1

            if type(element) is Vector and element.draw_arrow:
                self.draw_arrow(color=points_color, start_pos=points[0], end_pos=points[1])

            if type(element) is Landmark and type(element.text) is not None:
                self.draw_landmark_text(landmark=element, point=point)


    def draw_text(self, text_position, text: str) -> None:
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(bottomright=text_position)

        self.screen.blit(text_surface, text_rect)

    def draw_landmark_text(self, landmark: Landmark, point: pygame.Rect) -> None:
        text_surface = self.font.render(landmark.text, True, landmark.text_color)

        param = {landmark.rect_placement: point.__getattribute__(landmark.placement)}
        text_rect = text_surface.get_rect(**param)

        self.screen.blit(text_surface, text_rect)

    def show_ignored_errors(self) -> None:
        from tkinter import Tk, messagebox

        list_error = ""
        for error in self.ignored_error.items():
            if not error[1] == []:
                list_error += f"- element {error[0]} : \n"

                for i in error[1]:
                    list_error += f"  - {i}\n"

        messagebox_root = Tk()
        messagebox_root.withdraw()

        messagebox.showinfo("ignored error while calculating the points",
                            f"ignored error (the associated point will not be displayed) :\n{list_error}")

        messagebox_root.destroy()

    def get_graduation_and_points(self, show_x_graduation_coordinate: bool, show_y_graduation_coordinate: bool):
        self.graduation_coordinate = []

        self.x_grad = self.get_x_graduations(show_x_graduation_coordinate)

        self.y_grad = self.get_y_graduations(show_y_graduation_coordinate)

        self.curves_points = []
        for element in self.graph_elements:
            if type(element) == Landmark and not self.x_min <= element.x <= self.x_max:
                continue
            self.curves_points.append([element, self.get_curve_points(element=element)])

    def show_grid_lines(self, grad_color: tuple):
        for grad in self.x_grad:
            pygame.draw.line(self.screen, color=grad_color, start_pos=(grad[0], 0), end_pos=(grad[0], self.height))

        for grad in self.y_grad:
            pygame.draw.line(self.screen, color=grad_color, start_pos=(0, grad[1]), end_pos=(self.width, grad[1]))

    def move(self, x_velocity: float, y_velocity: float):
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            self.initial_xy()
        if pygame.time.get_ticks() % 10 == 0:
            if key[pygame.K_RIGHT]:
                self.x_max += x_velocity
                self.x_min += x_velocity
                self.getting_points = True

            if key[pygame.K_LEFT]:
                self.x_min -= x_velocity
                self.x_max -= x_velocity
                self.getting_points = True

            if key[pygame.K_UP]:
                self.y_min += y_velocity
                self.y_max += y_velocity
                self.getting_points = True

            if key[pygame.K_DOWN]:
                self.y_min -= y_velocity
                self.y_max -= y_velocity
                self.getting_points = True

    def zoom(self, x_min, x_max, y_min, y_max):
        self.x_min, self.x_max = x_min, x_max

        self.y_min, self.y_max = y_min, y_max

        self.zoom_mode = False
        self.getting_points = True

    def draw_zoom_rect(self):
        self.actual_cursor = pygame.SYSTEM_CURSOR_CROSSHAIR
        if self.first_point:
            pygame.draw.circle(self.screen, (0, 0, 0), self.mouse_pos, 3)
        else:
            self.zoom_x1, self.zoom_y1 = self.first_point_position
            self.zoom_x2, self.zoom_y2 = self.mouse_pos

            if self.zoom_x2 < self.zoom_x1:
                self.zoom_x1, self.zoom_x2 = self.zoom_x2, self.zoom_x1
            if self.zoom_y2 < self.zoom_y1:
                self.zoom_y1, self.zoom_y2 = self.zoom_y2, self.zoom_y1

            rect = (self.zoom_x1, self.zoom_y1, self.zoom_x2 - self.zoom_x1, self.zoom_y2 - self.zoom_y1)

            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

    def initial_xy(self):
        self.zoom(*self.initial_limit)

    def show(self, background_color: tuple = (255, 255, 255), points_color_list: list = None,
             axes_color: tuple = (0, 0, 0),
             graduation_color: tuple = (0, 0, 0), show_x_axis: bool = True, show_x_graduation_coordinate: bool = False,
             show_y_axis: bool = True, show_y_graduation_coordinate: bool = False, show_grid_lines: bool = False, show_coordinate: bool = False,
             win_title: str = "", win_icon_path: str = None,
             show_ignored_error: bool = False, x_step_movement: float = 0.5, y_step_movement: float = 0.5):

        if points_color_list is None:
            points_color_list = [(0, 0, 0), (0, 0, 255), (255, 0, 0),
                                 (0, 255, 0), (255, 192, 203), (255, 165, 0),
                                 (139, 69, 19), (0, 255, 255)
                                 ]

        if win_icon_path is not None:
            icon = pygame.image.load(win_icon_path)
            pygame.display.set_icon(icon)

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        pygame.display.set_caption(win_title)
        running = True

        self.zoom_mode = False
        self.first_point = True
        self.getting_points = True

        while running:
            self.actual_cursor = pygame.SYSTEM_CURSOR_ARROW
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    running = False

                if event.type == pygame.KEYUP and event.key == pygame.K_s:
                    self.screenshot()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # right click
                    self.zoom_mode = not self.zoom_mode
                    self.first_point = True

                if self.zoom_mode:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                        if self.first_point:
                            self.first_point = False
                            self.first_point_position = self.mouse_pos

                        else:
                            x_min, y_max = self.get_coordinate_from_position((self.zoom_x1, self.zoom_y1))
                            x_max, y_min = self.get_coordinate_from_position((self.zoom_x2, self.zoom_y2))

                            self.zoom(x_min, x_max, y_min, y_max)
                            self.first_point = True

            self.screen.fill(background_color)
            self.mouse_pos = pygame.mouse.get_pos()

            if self.zoom_mode:
                self.draw_zoom_rect()

            if self.getting_points:
                self.set_axes_info()

                self.get_graduation_and_points(show_x_graduation_coordinate, show_y_graduation_coordinate)

                if show_ignored_error and any(len(values) > 0 for values in self.ignored_error.values()):
                    self.show_ignored_errors()

                self.getting_points = False

            if show_coordinate:
                mouse_coordinate = self.get_coordinate_from_position(self.mouse_pos)
                mouse_coordinate = round(mouse_coordinate[0], 1), round(mouse_coordinate[1], 1)

                self.draw_text(text=str(mouse_coordinate), text_position=(self.width - 5, 20))

            if show_grid_lines:
                self.show_grid_lines(graduation_color)

            self.move(x_step_movement, y_step_movement)

            for color_index, (element, points) in enumerate(self.curves_points):
                color = (0, 0, 0)
                if len(points_color_list) > color_index:
                    color = points_color_list[color_index]

                self.draw_curve(points=points, points_color=color, element=element)

            self.draw_axes(axes_color, show_x_axis, show_y_axis)
            self.draw_graduations(self.x_grad, self.y_grad, graduation_color)

            pygame.mouse.set_cursor(pygame.cursors.Cursor(self.actual_cursor))
            pygame.display.update()

        pygame.quit()

    def screenshot(self, filename: str = "screenshot.png") -> None:
        pygame.image.save(self.screen, filename)

    def __repr__(self) -> str:
        return f"CoordinateSystem(graph_elements: {self.graph_elements}, x_min={self.x_min}, x_max={self.x_max}, y_min={self.y_min}, y_max={self.y_max})"
