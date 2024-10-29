# FunctionVisualizer

## by code
```python
from FunctionVisualizer import CoordinateSystem

if __name__ == '__main__':
    def f(x):
        return x**2 + 3 * x - 5

    system = CoordinateSystem(function=f,
                              screen_size=(500, 500),
                              x_min=-10, x_max=10, x_graduation_step=1,
                              y_min=-10, y_max=10, y_graduation_step=1,
                              trace_step=0.1,
                              draw_points=False,
                              draw_lines_between_points=True
                              )

    system.show() # can write optional parameter (bg_color, point_color, axes_color, graduation_color, show_coordinate, win_title, show_ignored_error)
   
```

### result : 
![WithCode](https://github.com/crocroque/FunctionVisualizer/blob/main/images/WithCode.png)

## using FunctionMaker.py
![FunctionMakerMenu](https://github.com/crocroque/FunctionVisualizer/blob/main/images/FunctionMakerMenu.png)

just enter the settings that you want and click "show"
for more settings click "more settings"

## usage example
![FunctionMakerFilled](https://github.com/crocroque/FunctionVisualizer/blob/main/images/FunctionMakerFilled.png)

### result :
![FunctionMakerFilledResult](https://github.com/crocroque/FunctionVisualizer/blob/main/images/FunctionMakerFilledResult.png)
