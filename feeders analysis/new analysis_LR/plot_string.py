import matplotlib.pyplot as plt 
import pandas as pd

x = ["Apple", "Banana", "Cherry"]
y = ['x','000','y']

# plt.plot(x, y)

# plt.show()

d = {'col1': ["Apple", "Banana", "Cherry"], 'col2': ["Apple", "Banana", "Cherry"],}
df = pd.DataFrame(data=d)

plt.plot (df['col1'])
plt.show()