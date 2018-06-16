import matplotlib.pyplot as plt
import numpy as np

countries = ['USA', 'GB', 'China', 'Russia', 'Germany']
bronzes = np.array([38, 17, 26, 19, 15])
silvers = np.array([37, 23, 18, 18, 10])
golds = np.array([46, 27, 26, 19, 17])
ind = [x for x, _ in enumerate(countries)]

total = bronzes + silvers + golds
proportion_bronzes = np.true_divide(bronzes, total) * 100
proportion_silvers = np.true_divide(silvers, total) * 100
proportion_golds = np.true_divide(golds, total) * 100

plt.barh(ind, proportion_golds, height=0.8, label='golds', color='gold', left=proportion_bronzes+proportion_silvers)
plt.barh(ind, proportion_silvers, height=0.8, label='silvers', color='silver', left=proportion_bronzes)
plt.barh(ind, proportion_bronzes, height=0.8, label='bronzes', color='#CD853F')

plt.yticks(ind, countries)
plt.xlabel("Medals")
plt.ylabel("Countries")
plt.title("2012 Olympics Top Scorers' Medals by Proportion")
plt.xlim=1.0

# rotate axis labels
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()