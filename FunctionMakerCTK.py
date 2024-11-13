import customtkinter as ctk
from tkinter import messagebox, colorchooser
from CoordinateSystem import CoordinateSystem, FunctionEvaluatingError, Function
import math


def show_function():
    def f(x: float) -> float:
        return eval(function_entry.get(), {"x": x, "math": math})

    try:
        system = CoordinateSystem(
            graph_elements=[
                Function(f, trace_step=float(trace_step_entry.get()),
                         draw_points=draw_points_param[1].get(),
                         draw_lines_between_points=draw_lines_between_points_param[1].get())],
            screen_size=(float(win_width_entry.get()), float(win_height_entry.get())),
            x_min=float(x_min_entry.get()),
            x_max=float(x_max_entry.get()),
            x_graduation_step=float(x_graduation_step_entry.get()),
            y_min=float(y_min_entry.get()),
            y_max=float(y_max_entry.get()),
            y_graduation_step=float(y_graduation_step_entry.get())
        )

        if more_option:
            system.show(
                background_color=eval(bg_color_entry.get()),
                points_color_list=[eval(point_color_entry.get())],
                axes_color=eval(axes_color_entry.get()),
                graduation_color=eval(graduation_color_entry.get()),
                show_coordinate=show_coordinate_param[1].get(),
                win_title=win_title_entry.get(),
                show_ignored_error=show_ignored_error_param[1].get()
            )
        else:
            system.show()

    except FunctionEvaluatingError as error:
        messagebox.showerror(title="Function Error", message=error.message)
        return

    except Exception as error:
        messagebox.showerror(title="Setting Error", message=error)
        return


def make_param_entry(win: ctk.CTk, param_name: str, row, description: str, default_value: str) -> ctk.CTkEntry:
    ctk.CTkLabel(win, text=param_name).grid(row=row, column=0)
    ctk.CTkLabel(win, text=description).grid(row=row, column=2)

    e = ctk.CTkEntry(win)
    e.insert(0, default_value)
    e.grid(row=row, column=1)
    return e


def ask_color(entry: ctk.CTkEntry):
    color_code = colorchooser.askcolor(title="Choose Color")
    entry.delete(0, ctk.END)
    entry.insert(0, str(color_code[0]))


def make_param_color_entry(win: ctk.CTk, param_name: str, row, default_value: str) -> ctk.CTkEntry:
    ctk.CTkLabel(win, text=param_name).grid(row=row, column=0)

    e = ctk.CTkEntry(win)
    e.grid(row=row, column=1)
    e.insert(0, default_value)

    ctk.CTkButton(win, text="Choose Color", command=lambda: ask_color(e)).grid(row=row, column=2)
    return e


def make_param_check_box(win: ctk.CTk, param_name: str, row, description: str) -> (ctk.CTkCheckBox, ctk.BooleanVar):
    ctk.CTkLabel(win, text=param_name).grid(row=row, column=0)
    ctk.CTkLabel(win, text=description).grid(row=row, column=2)

    var = ctk.BooleanVar()
    check_btn = ctk.CTkCheckBox(win, variable=var, onvalue=True, offvalue=False, text="")
    check_btn.grid(row=row, column=1)
    return check_btn, var


def automatic_tracestep():
    try:
        points_number = (float(x_max_entry.get()) - float(x_min_entry.get())) / float(trace_step_entry.get())
        text = f"{round(points_number)} points"
        if points_number > 100000:
            text += " (may be long; try to increase the trace step)"

        automatic_tracestep_label.configure(text=text)

    except:
        pass

    root.after(100, automatic_tracestep)


def make_win_title():
    title = f"Visualization of f(x) = {function_entry.get()} ∀ x ∈ [{x_min_entry.get()} ; {x_max_entry.get()}]"
    win_title_entry.delete(0, ctk.END)
    win_title_entry.insert(0, title)


def show_more_option():
    global more_option, bg_color_entry, point_color_entry, axes_color_entry, graduation_color_entry, show_coordinate_param, win_title_entry, show_ignored_error_param

    more_option_btn.destroy()
    show_function_btn.grid(row=20, column=1)

    more_option = True
    bg_color_entry = make_param_color_entry(root, "Background Color", 13, "(255, 255, 255)")
    point_color_entry = make_param_color_entry(root, "Points Color", 14, "(0, 0, 0)")
    axes_color_entry = make_param_color_entry(root, "Axes Color", 15, "(0, 0, 0)")
    graduation_color_entry = make_param_color_entry(root, "Graduation Color", 16, "(0, 0, 0)")
    show_coordinate_param = make_param_check_box(root, "Show Coordinates?", 17, "Display the mouse coordinates at the top left")
    win_title_entry = make_param_entry(root, "Window Title", 18, "", "Function")
    ctk.CTkButton(root, text="Automatic Title", command=make_win_title).grid(row=18, column=2)
    show_ignored_error_param = make_param_check_box(root, "Show Ignored Errors?", 19, "Display ignored errors during calculations")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Function Maker")
root.resizable(False, False)

win_width_entry = make_param_entry(root, "Window Width", 0, "float > 0", "500")
win_height_entry = make_param_entry(root, "Window Height", 1, "float > 0", "500")

function_entry = make_param_entry(root, "f(x) =", 2, "Python syntax (math library can be used)", "")
x_min_entry = make_param_entry(root, "x_min", 3, "float", "-10")
x_max_entry = make_param_entry(root, "x_max", 4, "float", "10")
x_graduation_step_entry = make_param_entry(root, "x Graduation Step", 5, "float > 0 | 0 for no graduation", "1")

y_min_entry = make_param_entry(root, "y_min", 6, "float", "-10")
y_max_entry = make_param_entry(root, "y_max", 7, "float", "10")
y_graduation_step_entry = make_param_entry(root, "y Graduation Step", 8, "float > 0 | 0 for no graduation", "1")

trace_step_entry = make_param_entry(root, "Trace Step", 9, "", "0.1")
automatic_tracestep_label = ctk.CTkLabel(root, text="")
automatic_tracestep_label.grid(row=9, column=2)
automatic_tracestep()

draw_points_param = make_param_check_box(root, "Draw Points?", 10, "Might need lower trace step | accurate")
draw_points_check_box = draw_points_param[0]
draw_points_check_box.select()  # Check the box

draw_lines_between_points_param = make_param_check_box(root, "Draw Lines Between Points?", 11, "Less accurate | might be faster")
draw_lines_between_points_check_box = draw_lines_between_points_param[0]

more_option = False

show_function_btn = ctk.CTkButton(root, text="Show", command=show_function)
show_function_btn.grid(row=12, column=1)

more_option_btn = ctk.CTkButton(root, text="More Settings", command=show_more_option)
more_option_btn.grid(row=12, column=2)

bg_color_entry = make_param_color_entry
point_color_entry = make_param_color_entry
axes_color_entry = make_param_color_entry
graduation_color_entry = make_param_color_entry

show_coordinate_param = make_param_check_box
win_title_entry = make_param_entry
show_ignored_error_param = make_param_check_box

root.mainloop()
