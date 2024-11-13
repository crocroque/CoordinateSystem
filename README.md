# CoordinateSystem

## visualisation of one function by code :
```python
from CoordinateSystem import CoordinateSystem, Function

if __name__ == '__main__':
    def f(x):
        return x ** 2 + 3 * x - 5

    my_function = Function(f, trace_step=0.01, draw_points=False, draw_lines_between_points=True)

    system = CoordinateSystem(graph_elements=[my_function], # <- have to be a list
                              screen_size=(500, 500),
                              x_min=-10, x_max=10, x_graduation_step=1,
                              y_min=-10, y_max=10, y_graduation_step=1,

                              )

    system.show()  # can write optional parameter (background_color, points_color_list, axes_color, graduation_color, show_coordinate,
                   # win_title, show_ignored_error, show_x_graduation_coordinate, show_y_graduation_coordinate)
   
```

### result : 
![WithCode](https://github.com/crocroque/FunctionVisualizer/blob/main/images/WithCode.png)

## visualisation of multiple functions by code :
```python
import math
from CoordinateSystem import CoordinateSystem, Function

if __name__ == '__main__':
    def f(x):
        return x ** 2 + 3 * x - 5

    def g(x):
        return math.exp(x)

    def h(x):
        return x

    my_functions = [Function(f, trace_step=0.01, draw_points=False, draw_lines_between_points=True),
                    Function(g, trace_step=0.01, draw_points=False, draw_lines_between_points=True),
                    Function(h, trace_step=0.01, draw_points=False, draw_lines_between_points=True)] # <- have to be a list

    system = CoordinateSystem(graph_elements=my_functions,
                              screen_size=(500, 500),
                              x_min=-10, x_max=10, x_graduation_step=1,
                              y_min=-10, y_max=10, y_graduation_step=1,

                              )

    system.show()  # can write optional parameter (background_color, points_color_list, axes_color, graduation_color, show_coordinate,
                   # win_title, show_ignored_error, show_x_graduation_coordinate, show_y_graduation_coordinate)
```

### result :
![WithCodeMultipleFunctions](https://github.com/crocroque/FunctionVisualizer/blob/main/images/WithCodeMultipleFunction.png)

## using FunctionMaker.py
![FunctionMakerMenu](https://github.com/crocroque/FunctionVisualizer/blob/main/images/FunctionMakerMenu.png)

Just enter the settings that you want and click "show".
For more settings click "more settings"

## usage example
![FunctionMakerFilled](https://github.com/crocroque/FunctionVisualizer/blob/main/images/FunctionMakerFilled.png)

### result :
![FunctionMakerFilledResult](https://github.com/crocroque/FunctionVisualizer/blob/main/images/FunctionMakerFilledResult.png)

## visualisation of a Sequence :
```python
from CoordinateSystem import CoordinateSystem, Sequence

if __name__ == '__main__':
    def fibonacci_sequence(n):
        if n == 0:
            return 0
        elif n == 1 or n == 2:
            return 1

        return fibonacci_sequence(n - 1) + fibonacci_sequence(n - 2)

    my_sequence = Sequence(fibonacci_sequence, n_min=0, trace_step=1, draw_points=True, draw_lines_between_points=False)

    system = CoordinateSystem(graph_elements=[my_sequence], # <- have to be a list
                              screen_size=(500, 500),
                              x_min=-10, x_max=30, x_graduation_step=1,
                              y_min=-100, y_max=1000, y_graduation_step=50,

                              )

    system.show()  # can write optional parameter (background_color, points_color_list, axes_color, graduation_color, show_coordinate,
                   # win_title, show_ignored_error, show_x_graduation_coordinate, show_y_graduation_coordinate)
```

### result :
![SequenceVisualisation](https://github.com/crocroque/FunctionVisualizer/blob/main/images/SequenceVisualisation.png)

## visualisation of a Vector :
```python
if __name__ == '__main__':
    AB = Vector(coordinate=(10, 5), draw_lines_between_points=False, draw_points=False, draw_arrow=True)
    BC = Vector(coordinate=(5, -6), start_coordinate=AB.end_coordinate)

    AC = AB + BC

    minus_demi_AB = 0.5 * -AB

    system = CoordinateSystem(graph_elements=[AB, BC, AC, minus_demi_AB],  # <- have to be a list
                              screen_size=(500, 500),
                              x_min=-20, x_max=20, x_graduation_step=2,
                              y_min=-10, y_max=10, y_graduation_step=1,

                              )

    system.show()  # can write optional parameter (background_color, points_color_list, axes_color, graduation_color, show_coordinate,
                   # win_title, show_ignored_error, show_x_graduation_coordinate, show_y_graduation_coordinate)
```

### result :
![VectorVisualisation](https://github.com/crocroque/CoordinateSystem/blob/main/images/VectorVisualisation.png)
