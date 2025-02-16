import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser, filedialog, Toplevel
from PIL import Image, ImageTk
import CoordinateSystem as cs
import math


def rgb_to_hex(rgb: tuple):
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}".upper()


class FunctionMaker(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Element Maker")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.home_page_param = {
            "win_sep": {"type": "SEPARATOR", "DefaultValue": "WINDOW"},
            "WINDOW WIDTH": {"type": "FLOAT", "DefaultValue": 800},
            "WINDOW HEIGHT": {"type": "FLOAT", "DefaultValue": 800},
            "win_icon_path": {"type": "FILE", "DefaultValue": None},
            "win_title": {"type": "STRING", "DefaultValue": ""},
            "axes_sep": {"type": "SEPARATOR", "DefaultValue": "AXES"},
            "MIN X": {"type": "FLOAT", "DefaultValue": -10},
            "MAX X": {"type": "FLOAT", "DefaultValue": 10},
            "X GRADUATION STEP": {"type": "FLOAT", "DefaultValue": 1},
            "MIN Y": {"type": "FLOAT", "DefaultValue": -10},
            "MAX Y": {"type": "FLOAT", "DefaultValue": 10},
            "Y GRADUATION STEP": {"type": "FLOAT", "DefaultValue": 1},
            "color_sep": {"type": "SEPARATOR", "DefaultValue": "COLOR"},
            "background_color": {"type": "COLOR", "DefaultValue": (255, 255, 255)},
            "axes_color": {"type": "COLOR", "DefaultValue": (0, 0, 0)},
            "graduation_color": {"type": "COLOR", "DefaultValue": (0, 0, 0)},
            "misc_sep": {"type": "SEPARATOR", "DefaultValue": "MISC"},
            "show_x_axis": {"type": "BOOL", "DefaultValue": True},
            "show_x_graduation_coordinate": {"type": "BOOL", "DefaultValue": False},
            "show_y_axis": {"type": "BOOL", "DefaultValue": True},
            "show_y_graduation_coordinate": {"type": "BOOL", "DefaultValue": False},
            "show_coordinate": {"type": "BOOL", "DefaultValue": False},
            "show_ignored_error": {"type": "BOOL", "DefaultValue": False},
            "x_step_movement": {"type": "FLOAT", "DefaultValue": 1},
            "y_step_movement": {"type": "FLOAT", "DefaultValue": 1}
        }

        self.function_page_param = {
            "expression": {"type": "STRING", "DefaultValue": "x"},
            "trace_step": {"type": "FLOAT", "DefaultValue": 0.1},
            "draw_points": {"type": "BOOL", "DefaultValue": False},
            "draw_lines_between_points": {"type": "BOOL", "DefaultValue": True},
            "swap_xy": {"type": "BOOL", "DefaultValue": False}
        }

        self.sequence_page_param = {
            "formula": {"type": "STRING", "DefaultValue": "n"},
            "n_min": {"type": "INT", "DefaultValue": 0},
            "trace_step": {"type": "INT", "DefaultValue": 1},
            "draw_points": {"type": "BOOL", "DefaultValue": True},
            "draw_lines_between_points": {"type": "BOOL", "DefaultValue": False}
        }

        self.Vector_page_param = {
            "Vector X": {"type": "FLOAT", "DefaultValue": 1},
            "Vector Y": {"type": "FLOAT", "DefaultValue": 1},

            "Starting X": {"type": "FLOAT", "DefaultValue": 0},
            "Starting Y": {"type": "FLOAT", "DefaultValue": 0},

            "Draw arrow ?": {"type": "BOOL", "DefaultValue": True},
            "draw_points": {"type": "BOOL", "DefaultValue": False},
            "draw_lines_between_points": {"type": "BOOL", "DefaultValue": False}
        }

        self.Landmark_page_param = {
            "X": {"type": "FLOAT", "DefaultValue": 1},
            "Y": {"type": "FLOAT", "DefaultValue": 1},
            "text": {"type": "STRING", "DefaultValue": ""},
            "text_color": {"type": "COLOR", "DefaultValue": (0, 0, 0)},
            "text_placement": {"type": "COMBOBOX", "DefaultValue": "bottomright", "list": ['topleft', 'midtop', 'midbottom', 'bottomright', 'topright', 'bottomleft']}
        }

        self.graph_elements_list = [cs.Function, cs.Sequence, cs.Vector, cs.Landmark]
        self.graph_elements = {}

        self.asking_window = None
        self.add_element_tab = None

        self.create_home_page()
        self.create_add_element_tab()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

    def create_add_element_tab(self):
        self.add_element_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_element_tab, text="+")

    def ask_element(self):
        self.asking_window = Toplevel(self.notebook)
        self.asking_window.title("Choose an element")
        self.asking_window.grab_set()

        for index, element in enumerate(self.graph_elements_list):
            tk.Button(self.asking_window, text=element.__name__, width=10, height=5, font=("", 20),
                      command=lambda name=element.__name__: self.create_element_tab(name)).grid(column=index, row=0)

    def create_element_tab(self, element_name: str):
        element_tab = ttk.Frame(self.notebook)
        self.notebook.add(element_tab, text=element_name)

        self.asking_window.destroy()
        self.add_element_tab.destroy()
        self.create_add_element_tab()

        tk.Label(element_tab, text="------------------------", font=("", 20)).grid(row=0, column=0)
        tk.Label(element_tab, text=element_name, font=("", 20)).grid(row=0, column=1)
        tk.Label(element_tab, text="------------------------", font=("", 20)).grid(row=0, column=2)

        if element_name == "Function":
            self.create_param(tab=element_tab, dictName=self.function_page_param)
            tk.Label(element_tab, text="PYTHON SYNTAX (MATH LIB CAN BE USED)").grid(column=2, row=1)

        elif element_name == "Sequence":
            self.create_param(tab=element_tab, dictName=self.sequence_page_param)
            tk.Label(element_tab, text="PYTHON SYNTAX (MATH LIB CAN BE USED)").grid(column=2, row=1)

        elif element_name == "Vector":
            self.create_param(tab=element_tab, dictName=self.Vector_page_param)

        elif element_name == "Landmark":
            self.create_param(tab=element_tab, dictName=self.Landmark_page_param)

        element_tab.update_idletasks()
        self.geometry(f"{element_tab.winfo_reqwidth()}x{element_tab.winfo_reqheight()}")


    def on_tab_selected(self, event: tk.Event):
        tab_frame = self.notebook.winfo_children()[self.notebook.index((self.notebook.select()))]
        tab_frame.update_idletasks()
        self.geometry(f"{tab_frame.winfo_reqwidth()}x{tab_frame.winfo_reqheight() + 50}")

        tab_text = self.notebook.tab(self.notebook.select(), "text")
        if tab_text == "+":
            self.ask_element()


    @staticmethod
    def ask_file(dictName: dict, paramName: str):
        icon_filename = filedialog.askopenfilename(title="Choose an .ico file",
                                                   filetypes=[("png files", "*.png"), ("ico files", "*.ico"),
                                                              ("all files", "*.*")])
        canvas = dictName[paramName]["file_canvas"]
        label = dictName[paramName]["file_lbl"]
        if icon_filename == "":
            label.configure(text=None)
            canvas.delete("all")
            dictName[paramName]["icon_filename"] = None

        else:
            image = Image.open(icon_filename)
            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)

            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo

            dictName[paramName]["icon_filename"] = icon_filename

            label.configure(text="")

    @staticmethod
    def ask_color(dictName: dict, paramName: str):
        color = colorchooser.askcolor()
        if color != (None, None):
            dictName[paramName]["color_block_lbl"].configure(foreground=color[1])
            dictName[paramName]["color_lbl"].configure(text=str(color[0]) + ' > ')

    def add_elements(self, system: cs.CoordinateSystem):
        for tab in self.graph_elements:
            tab_name = self.notebook.tab(tab, "text")
            tab_widget = self.graph_elements.get(tab)
            if tab_name == "Home":
                continue

            trace_step = tab_widget.get("trace_step", None)

            if trace_step is None:
                trace_step = 0.0
            else:
                trace_step = trace_step.get()


            draw_points = tab_widget.get("draw_points", None)
            draw_lines_between_points = tab_widget.get("draw_lines_between_points", None)

            if tab_name == "Function":
                expression = tab_widget["expression"].get()

                def f(x, expr=expression):
                    return eval(expr, {"x": x, "math": math})

                swap_xy = tab_widget["swap_xy"].get()

                func = cs.Function(expression=f, trace_step=float(trace_step), draw_points=draw_points.get(),
                                   draw_lines_between_points=draw_lines_between_points.get(), swap_xy=swap_xy)

                system.graph_elements.append(func)

            elif tab_name == "Sequence":
                formula = tab_widget["formula"].get()

                def u(n, form=formula):
                    return eval(form, {"n": n, "math": math})

                n_min = float(tab_widget["n_min"].get())

                seq = cs.Sequence(formula=u, n_min=n_min, trace_step=int(trace_step), draw_points=draw_points.get(),
                                  draw_lines_between_points=draw_lines_between_points.get())

                system.graph_elements.append(seq)

            elif tab_name == "Vector":
                coordinate = (float(tab_widget["Vector X"].get()), float(tab_widget["Vector Y"].get()))
                start_coor = (float(tab_widget["Starting X"].get()), float(tab_widget["Starting Y"].get()))

                draw_arrow = tab_widget["Draw arrow ?"].get()

                vector = cs.Vector(coordinate=coordinate, start_coordinate=start_coor, draw_arrow=draw_arrow,
                                   draw_points=draw_points.get(), draw_lines_between_points=draw_lines_between_points.get())

                system.graph_elements.append(vector)

            elif tab_name == "Landmark":
                coordinate = (float(tab_widget["X"].get()), float(tab_widget["Y"].get()))

                text = tab_widget["text"].get()
                text_color = eval(tab_widget["text_color"].cget("text").split(">")[0]) # eval = str to tuple
                text_placement = tab_widget["text_placement"].get()

                landmark = cs.Landmark(coordinate=coordinate, text=text, text_color=text_color, text_placement=text_placement)

                system.graph_elements.append(landmark)

    def show(self):
        def get_text_color_lbl(param: str) -> tuple:
            return eval(self.home_page_param[param]["color_lbl"].cget("text").split(">")[0])  # eval = str to tuple

        def get_check_btn(param: str) -> bool:
            return self.home_page_param[param]["CheckButtonVar"].get()

        def get_entry(param: str) -> str:
            return self.home_page_param[param]["Entry"].get()

        screen_size = (float(get_entry("WINDOW WIDTH")), float(get_entry("WINDOW HEIGHT")))

        x_min = float(get_entry("MIN X"))
        x_max = float(get_entry("MAX X"))
        x_grad_step = float(get_entry("X GRADUATION STEP"))

        y_min = float(get_entry("MIN Y"))
        y_max = float(get_entry("MAX Y"))
        y_grad_step = float(get_entry("Y GRADUATION STEP"))

        bg_color = get_text_color_lbl("background_color")
        axes_color = get_text_color_lbl("axes_color")
        graduation_color = get_text_color_lbl("graduation_color")
        show_x_axis = get_check_btn("show_x_axis")
        show_x_graduation_coordinate = get_check_btn("show_x_graduation_coordinate")
        show_y_axis = get_check_btn("show_y_axis")
        show_y_graduation_coordinate = get_check_btn("show_y_graduation_coordinate")
        show_coordinate = get_check_btn("show_coordinate")
        win_title = get_entry("win_title")
        win_icon_path = self.home_page_param["win_icon_path"]["icon_filename"]
        show_ignored_error = get_check_btn("show_ignored_error")
        x_step_movement = float(get_entry("x_step_movement"))
        y_step_movement = float(get_entry("y_step_movement"))

        system = cs.CoordinateSystem(graph_elements=[], screen_size=screen_size,
                                     x_min=x_min, x_max=x_max, x_graduation_step=x_grad_step,
                                     y_min=y_min, y_max=y_max, y_graduation_step=y_grad_step)

        self.add_elements(system=system)

        system.show(background_color=bg_color, points_color_list=None, axes_color=axes_color,
                    graduation_color=graduation_color,
                    show_x_axis=show_x_axis, show_x_graduation_coordinate=show_x_graduation_coordinate,
                    show_y_axis=show_y_axis,
                    show_y_graduation_coordinate=show_y_graduation_coordinate, show_coordinate=show_coordinate,
                    win_title=win_title,
                    win_icon_path=win_icon_path, show_ignored_error=show_ignored_error, x_step_movement=x_step_movement,
                    y_step_movement=y_step_movement)

    def create_param(self, tab: ttk.Frame, dictName: dict):
        self.graph_elements[tab] = {}
        for (index, (param, paramDict)) in enumerate(dictName.items(), start=1):
            type_param = paramDict["type"]
            default_value = paramDict["DefaultValue"]

            param_name_label = tk.Label(tab, text=param, font=("", 10))
            param_name_label.grid(column=0, row=index)

            if type_param == "BOOL":
                cb_var = tk.BooleanVar()

                cb = tk.Checkbutton(tab, variable=cb_var)
                cb.grid(column=1, row=index)
                cb.select() if default_value else None

                dictName[param]["CheckButtonVar"] = cb_var

                self.graph_elements[tab][param] = cb_var

            elif type_param in ["FLOAT", "INT", "STRING"]:
                entry = tk.Entry(tab)
                entry.insert(0, default_value)
                entry.grid(column=1, row=index)

                dictName[param]["Entry"] = entry

                self.graph_elements[tab][param] = entry

            elif type_param == "FILE":
                file_canvas = tk.Canvas(tab, width=100, height=100)
                file_canvas.grid(column=2, row=index)

                file_lbl = tk.Label(tab, text=f"{default_value}", font=("", 15))
                file_lbl.grid(column=2, row=index)

                dictName[param]["icon_filename"] = None

                dictName[param]["file_lbl"] = file_lbl
                dictName[param]["file_canvas"] = file_canvas

                btn = tk.Button(tab, text="Choose File",
                                command=lambda p=param: self.ask_file(dictName=dictName, paramName=p))
                btn.grid(column=1, row=index)

            elif type_param == "COLOR":

                color_block_lbl = tk.Label(tab, text=f"{25 * ' '}      █", font=("", 15),
                                           foreground=rgb_to_hex(default_value))
                color_block_lbl.grid(column=2, row=index)

                color_lbl = tk.Label(tab, text=f"{default_value} > ", font=("", 15))
                color_lbl.grid(column=2, row=index)

                dictName[param]["color_block_lbl"] = color_block_lbl
                dictName[param]["color_lbl"] = color_lbl

                self.graph_elements[tab][param] = color_lbl

                btn = tk.Button(tab, text="Choose Color",
                                command=lambda p=param: self.ask_color(dictName=dictName, paramName=p))
                btn.grid(column=1, row=index)

            elif type_param == "COMBOBOX":
                combo = ttk.Combobox(tab, values=paramDict["list"], state="readonly")
                combo.set(default_value)
                combo.grid(column=1, row=index)

                self.graph_elements[tab][param] = combo

            elif type_param == "SEPARATOR":
                param_name_label.configure(text="")
                tk.Label(tab, text=f"{'-' * 10 + default_value + '-' * 10}", font=("", 10)).grid(column=1, row=index)

    def create_home_page(self):

        home_page = ttk.Frame(self.notebook)
        self.notebook.add(home_page, text="Home")

        tk.Label(home_page, text="------------------------", font=("", 20)).grid(row=0, column=0)
        tk.Label(home_page, text="Home Page", font=("", 20)).grid(row=0, column=1)
        tk.Label(home_page, text="------------------------", font=("", 20)).grid(row=0, column=2)

        self.create_param(tab=home_page, dictName=self.home_page_param)

        show_btn = tk.Button(home_page, text="SHOW", command=self.show, width=10, height=3)
        show_btn.grid(column=1, row=len(self.home_page_param.items()) + 1)


if __name__ == '__main__':
    app = FunctionMaker()

    app.mainloop()
