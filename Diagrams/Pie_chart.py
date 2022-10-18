import matplotlib.pyplot as plt

fig, ax = plt.subplots()

size = 0.2
vals = [90, 5, 5]

colors = ['red', 'blue', 'green']

ax.pie(vals, radius=1, colors=colors,
       wedgeprops=dict(width=size, edgecolor=(0.2, 0.2, 0.2, 1)))

fig.set_facecolor((0.2, 0.2, 0.2, 1))

plt.savefig('pie_chart_pic/pie_chart.png')