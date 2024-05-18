import Data 
from ClusterEvaluation import ClusterEv
from Clustering import Clustering
from Methods import Methods
from matplotlib import pyplot as plt

y = []
x = []
colors = []
grosor = []

data = Data.Data.GetMunicData()
data_groups = Clustering.Agrupa(data, 9, "kmeans", 5)

for g in range(0, len(data_groups[0][0]), 1):
    Silouette = data_groups[3]
    color = Methods.GetRandomColor()
    for i in range(0, len(data_groups[0][0][g]), 1):
        y.append(data_groups[0][0][g][i].nombre)
        x.append(Silouette[g][i])
        colors.append(color)
        grosor.append(0.2)

fig, ax = plt.subplots()
ax.barh(y, x, color = colors, height = 0.4)
plt.xlim(-1, 1)
plt.show()
print("hello")