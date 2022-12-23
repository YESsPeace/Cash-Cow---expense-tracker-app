from matplotlib import pyplot as plt

fig, ax = plt.subplots()

size = 0.2
vals = [7, 10, 20]

colors = ['red', 'blue', 'green']

ax.pie(vals, radius=1, colors=colors,
       wedgeprops=dict(width=size, edgecolor=(0.2, 0.2, 0.2, 1)))

fig.set_facecolor((0.2, 0.2, 0.2, 1))

fig.set_size_inches(3.6, 3.6, forward=True)


fig.savefig('pie_chart_pic/pie_chart.png')