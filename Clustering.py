from Methods import Methods
import time
import sys
from ClusterEvaluation import ClusterEv
import Structs
import random
import copy

class Clustering:
    def __init__(self):
        pass

    @staticmethod
    def Kmeans_arb_centr(data, k):
        centroids = Methods.GetRandomCentroids(data, k, 0.18)
        
        while(Methods.AsignToBestCluster(data, centroids)):
            groups = Methods.RecalculateCentroids(data, centroids)

        return groups
    
    @staticmethod
    def DBSCAN(data, min_n, eps):           #ahora mismo solo funciona para dos dimensiones
        nodes_MaxMin = Structs.Node.Organizate(data, eps)
        x_min = nodes_MaxMin[1][0].min
        x_max = nodes_MaxMin[1][0].max
        y_min = nodes_MaxMin[1][1].min
        y_max = nodes_MaxMin[1][1].max

        for data_ in data:
            data_.neighbors = []
            params_i = [(list(data_.propiedades.values())[0]-x_min)/(x_max - x_min), (list(data_.propiedades.values())[1]-y_min)/(y_max-y_min)]
            for adyacent in nodes_MaxMin[0][data_.node.position[0]][data_.node.position[1]].adyacents:
                for element in adyacent.elements:
                    params_j = [(list(element.propiedades.values())[0]-x_min)/(x_max-x_min), (list(element.propiedades.values())[1]-y_min)/(y_max-y_min)]
                    if(Methods.DistVectorial(params_i, params_j) <= eps):
                        data_.neighbors.append(element)
        
        for data_ in data:
            if (len(data_.neighbors) >= min_n):
                data_.type = 'central'

        for data_ in data:
            for neighbor in data_.neighbors:
                if (not hasattr(data_, 'type')):
                    if(hasattr(neighbor, 'type')):
                        if(neighbor.type == 'central'):
                            data_.type = 'bord'
            if (not hasattr(data_, 'type')):
                data_.type = 'out'


        groups = Methods.Search_Groups(data)
        return groups

        

        


    @staticmethod
    def Agrupa(data, cant, method: str, time_):

        if (method == "kmeans"):
            CH = -sys.maxsize
            DB = sys.maxsize

            inicio = time.time()
            actual = time.time()
            while(actual - inicio < time_):
                for data_ in data:             #reiniciamos los grupos de los datos
                    if hasattr(data_, 'group'):
                        del data_.group
                clusters = Clustering.Kmeans_arb_centr(data, cant)
                CH_ = ClusterEv.CalinskiHarabasz(clusters)
                DB_ = ClusterEv.DaviesBouldin(clusters)
                
                Silouette_res = ClusterEv.Silouette(clusters)
                
                #if(CH_ > CH):
                #    CH = CH_
                #    inicio = time.time()
                #    actual = time.time()
                if (CH_ > CH and DB_ < DB):
                    CH = CH_
                    DB = DB_
                    inicio = time.time()
                    actual = time.time()
                #if(DB_ < DB):
                #    DB = DB_
                #    inicio = time.time()
                #    actual = time.time()

                else: 
                    actual = time.time()

            return clusters, CH, DB, Silouette_res


