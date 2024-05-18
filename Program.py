import folium
import Data 
import shelve
from DibMapa import BookMark
from ClusterEvaluation import ClusterEv
from Clustering import Clustering
from Methods import Methods
from matplotlib import pyplot as plt

data = Data.Data.GetMunicData()
Methods.RazonDeProp(data)

CH=[]
DB=[]
x=[]

for i in range(3, 9, 2):
    data_groups = Clustering.Agrupa(data, i, "kmeans", 5)
    CH.append(data_groups[1])
    DB.append(data_groups[2])
    x.append(i)

plt.plot(x,CH)
plt.xlabel("Cantidad de Clusters")
plt.ylabel("Calinski Harabasz")

plt.show()

plt.plot(x, DB)
plt.xlabel("Cantidad de Clusters")
plt.ylabel("Davies Bouldin")

plt.show()

m = folium.Map(location=[22.982009905727626, -80.58764508649523], zoom_start= 5)

BookMark.MarcadoresDeGrupos(m, data_groups)

