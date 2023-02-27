from matplotlib import pyplot as plt

fig, ax = plt.subplots()

size = 0.2
vals = [25, 10, 20, 30, 15]

# colors = ['red', 'blue', 'green', 'purple', 'yellow']

ax.pie(vals, radius=1,
       wedgeprops=dict(width=size, edgecolor=(0.2, 0.2, 0.2, 1)))

fig.set_facecolor((0.2, 0.2, 0.2, 1))

# fig.set_size_inches(3.6, 3.6, forward=True)


fig.savefig('pie_chart_pic/pie_chart_presentation.png')