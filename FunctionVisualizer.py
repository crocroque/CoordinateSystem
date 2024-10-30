import math
from tkinter import Tk, messagebox
import pygame


class Function:
    def __init__(self, expression):
        self.expression = expression

    def get_images(self, start: int, stop: int, step: float, errors_list: list = None) -> dict:
        images = {}
        x = start
        while x <= stop:
            try:
                image = self.expression(x)
                if type(image) is not complex:
                    images[x] = image

                elif type(errors_list) is list and "Result Is Complex Number" not in errors_list:
                    errors_list.append("Result Is Complex Number")

            except (ZeroDivisionError,ValueError, OverflowError) as e:
                if type(errors_list) is list:
                    if str(e) not in errors_list:
                        errors_list.append(str(e))

                else:
                    pass

            x += step

        return images


class FunctionEvaluatingError(Exception):
    def __init__(self, error):
        self.message = f"Error while evaluating the function : \n {error}"


class CoordinateSystem:
    def __init__(self, function, screen_size: tuple, x_min: float, x_max: float, x_graduation_step: float, y_min: float, y_max: float,  y_graduation_step: float, trace_step: float, draw_points: bool = True, draw_lines_between_points: bool = False):
        self.function = Function(function)
        self.width, self.height = screen_size

        if x_min >= x_max:
            raise Exception(f"x_min ({x_min}) >= x_max ({x_max})")

        if y_min >= y_max:
            raise Exception(f"y_min ({y_min}) >= y_max ({y_max})")

        if x_graduation_step < 0:
            raise Exception("x_graduation_step < 0 not allowed (x_graduation_step = 0 for no graduation)")

        if y_graduation_step < 0:
            raise Exception("y_graduation_step < 0 not allowed (y_graduation_step = 0 for no graduation)")

        if trace_step <= 0:
            raise Exception("trace_step <= 0 not allowed")

        if type(draw_points) is not bool:
            raise Exception(f"draw_points must be True or False not {type(draw_points)}")

        if type(draw_lines_between_points) is not bool:
            raise Exception(f"draw_lines_between_points must be True or False not {type(draw_lines_between_points)}")

        if self.width < 0:
            raise Exception("window_width < 0 not allowed")

        if self.height < 0:
            raise Exception("window_height < 0 not allowed")


        self.x_min = x_min
        self.x_max = x_max
        self.x_graduation_step = x_graduation_step

        self.y_min = y_min
        self.y_max = y_max
        self.y_graduation_step = y_graduation_step

        self.trace_step = trace_step

        self.screen = None

        self.len_x_axis = abs(self.x_max - self.x_min)
        self.len_y_axis = abs(self.y_max - self.y_min)

        self.x_coordinate_yaxis = self.width * (-self.x_min) / self.len_x_axis
        self.y_coordinate_xaxis = self.height * (-self.y_min) / self.len_y_axis

        self.draw_lines_between_points = draw_lines_between_points
        self.draw_points = draw_points

        self.ignored_error = []

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


    def get_position_from_coordinate(self, coordinate: tuple) -> tuple: # position = pixel | coordinate = x_min < coor < x_max
        x_coordinate, y_coordinate = coordinate

        x_position = (x_coordinate - self.x_min) / (self.x_max - self.x_min) * self.width
        y_position = self.height * (1 - (y_coordinate - self.y_min) / self.len_y_axis)

        return x_position, y_position


    def get_coordinate_from_position(self, point: tuple) -> tuple: # position = pixel | coordinate = x_min < coor < x_max
        x_position, y_position = point

        x_coordinate = (x_position / self.width) * (self.x_max - self.x_min) + self.x_min
        y_coordinate = self.y_min + (1 - y_position / self.height) * self.len_y_axis

        return x_coordinate, y_coordinate


    def get_x_graduations(self) -> list:
        if self.x_graduation_step == 0:
            return []

        graduations = []
        x_grad = 0
        while x_grad <= self.x_max:

            x, y = self.get_position_from_coordinate((x_grad, 0))
            graduations.append((x, y))

            x_grad += self.x_graduation_step

        x_grad = 0
        while x_grad >= self.x_min:
            x, y = self.get_position_from_coordinate((x_grad, 0))
            graduations.append((x, y))

            x_grad -= self.x_graduation_step

        return graduations


    def get_y_graduations(self) -> list:
        if self.y_graduation_step == 0:
            return []

        graduations = []
        y_grad = 0
        while y_grad <= self.y_max:

            x, y = self.get_position_from_coordinate((0, y_grad))
            graduations.append((x, y))

            y_grad += self.y_graduation_step

        y_grad = 0
        while y_grad >= self.y_min:
            x, y = self.get_position_from_coordinate((0, y_grad))
            graduations.append((x, y))

            y_grad -= self.y_graduation_step

        return graduations


    def draw_graduations(self, x_graduation: list, y_graduation: list, graduation_color: tuple):
        for i in x_graduation:
            x, y = i
            pygame.draw.line(self.screen, graduation_color, (x, y - 5), (x, y + 5))

        for i in y_graduation:
            x, y = i
            pygame.draw.line(self.screen, graduation_color, (x - 5, y), (x + 5, y))


    def get_curve_points(self) -> list:
        try:
            images = self.function.get_images(self.x_min, self.x_max, self.trace_step, errors_list=self.ignored_error)
        except Exception as e:
            pygame.quit()
            raise FunctionEvaluatingError(e)

        points = []

        for x, y in images.items():
            points.append(self.get_position_from_coordinate((x, y)))

        return points


    def draw_curve(self, points : list, points_color: tuple):
        index_counter = 0
        for point_position in points:
            if self.draw_points:
                x, y = point_position
                pygame.draw.circle(self.screen, points_color, (x, y), 2)

            if self.draw_lines_between_points and index_counter < len(points) - 1:
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


    def show(self, bg_color: tuple = (255, 255, 255), point_color: tuple = (0, 0, 0), axes_color: tuple = (0, 0, 0), graduation_color: tuple = (0, 0, 0), show_coordinate: bool = False, win_title: str = "function", show_ignored_error: bool = True):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(win_title)
        running = True

        print("getting x graduation ...")
        x_grad = self.get_x_graduations()

        print("getting y graduation...")
        y_grad = self.get_y_graduations()

        print(f"getting images and points ({(self.x_max - self.x_min) / self.trace_step})")
        points = self.get_curve_points()

        if len(self.ignored_error) > 0 and show_ignored_error:
            list_error = ""
            for error in self.ignored_error:
                list_error += "- " + error + "\n"
            messagebox_root = Tk()
            messagebox_root.withdraw()
            messagebox.showinfo("ignored error while calculating the points", f"ignored error (the associated point will not be displayed) :\n{list_error}")
            messagebox_root.destroy()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(bg_color)

            if show_coordinate:
                text = self.get_mouse_coordinate()
                self.screen.blit(text[0], text[1])

            self.draw_axes(axes_color)
            self.draw_graduations(x_grad, y_grad, graduation_color)
            self.draw_curve(points, point_color)
            pygame.display.update()

        pygame.quit()
