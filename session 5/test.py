import matplotlib.pyplot as plt
import numpy as np

x = np.arange(23)
y = 2 * x

a = np.linspace(-5, 5, 100)
b = a ** 3


fig = plt.figure(figsize=(10, 3), dpi=500)

axes1 = fig.add_axes([0, 0, 1, 1]) # left, bottom, width, height (range 0 to 1)
axes2 = fig.add_axes([0.5, 0.5, 0.4, 0.4])

# axe 1
axes1.plot(x, y)
axes1.set_xlabel("X Label") 
axes1.set_ylabel("Y Label") 
axes1.set_title("Big Figure")
# axe 2
axes2.plot(a, b)
axes2.set_xlabel("A Label") 
axes2.set_ylabel("B Label") 
axes2.set_title("Small Figure")

fig.savefig('myfig1.png', bbox_inches='tight')




plt.show();