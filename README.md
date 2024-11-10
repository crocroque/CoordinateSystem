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

    system.show()  # can write optional parameter (bg_color, points_color_list, axes_color, graduation_color, show_coordinate, win_title, show_ignored_error)
   
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

    system.show()  # can write optional parameter (bg_color, points_color_list, axes_color, graduation_color, show_coordinate, win_title, show_ignored_error)
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

## visualisation of a Sequence by code :
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

    system.show()  # can write optional parameter (bg_color, points_color_list, axes_color, graduation_color, show_coordinate, win_title, show_ignored_error)
```

### result :
![SequenceVisualisation](https://github.com/crocroque/FunctionVisualizer/blob/main/images/SequenceVisualisation.png)
