import math
import matplotlib.pyplot as plt
import numpy as np

def xe(x):
    if x < 0 or x > 1:
        return 0
    if x < .13:
        return x ** 2 * 5
    if x >= .13 and x < .45:
        return (x - .3) ** 2 * -5 + .23
    if x >= .45:
        return (-math.sqrt(x - .4) + .8)/5

data_x = [ i for i in range(0, 3201) ]
data_y = [ xe(i / 3200) / .23 for i in data_x ]



fig, ax = plt.subplots()
ax.plot(data_x, data_y)
plt.show()