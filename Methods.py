import random
import copy
import queue
import math
from Structs import Point
import Structs

class Methods:
    def __init__(self) -> None:
        pass

    
    @staticmethod
    def Search_Groups(data):
        data_copy = []
        for data_ in data:
            data_copy.append(data_)

        groups = []
        outlier_group = []
        while(len(data_copy) != 0):
            element = random.choice(data_copy)
            if(element.type == 'central'):
                group = Methods.Construye_Grupo(data_copy, element)
                groups.append(group)

            else:
                if(element.type == 'bord'):
                    for neighbor in element.neighbors:
                        if(neighbor.type == 'central' and not neighbor in data):
                            group = Methods.Construye_Grupo(data_copy, neighbor)
                            groups.append(group)
                else:
                    outlier_group.append(element)
                    data_copy.remove(element)
            
        groups.append(outlier_group)
        return groups

    @staticmethod
    def Construye_Grupo(data, central_element):
        group = []
        cola = queue.Queue()
        cola.put(central_element)
        data.remove(central_element)
        
        while(not cola.empty()):                 
            element = cola.get()
            if (element.type == 'central'):
                group.append(element)
                for neighbor in element.neighbors:
                    if(neighbor in data):
                        data.remove(neighbor)
                        cola.put(neighbor)
            else:
                group.append(element)   #sabemos que los únicos vecinos de los centrales son los bordes, no podemos alcanzar nodos 'out' en este método
                for neighbor in element.neighbors:
                    if(neighbor in data and neighbor.type == 'central'):
                        data.remove(neighbor)
                        cola.put(neighbor)
                    else:
                        if(neighbor in data and neighbor.type == 'bord'):
                            data.remove(neighbor)
                            cola.put(neighbor)
                        else:
                            if(neighbor in data):
                                data.remove(neighbor)
        
        return group


    @staticmethod
    def GetRandomCentroids(data: list, k, eps=0):

        emergency = []
        if (eps != 0):
            result = []
            data_ = copy.deepcopy(data)
            masc = False
            i = 0
            while( i < k):#revisa los centroides obtenidos buscando que el centroide aleatorio actual este 'lejos' de los ya encontrados
                if(len(data_) == 0):
                    break
                             
                r = random.randint(0, len(data_) - 1)
                centroid = list(data_[r].propiedades.values())
                for result_ in result:                             
                    dist = Methods.DistVectorial(centroid, result_)
                    if (dist < eps):
                        masc = True
                        emergency.append(centroid)
                        data_.remove(data_[r])
                        break
                if(not masc):
                    result.append(centroid)
                    data_.remove(data_[r])
                    i = i+1
                else:
                    masc = False

        else:
            result = []
            data_ = copy.deepcopy(data)

            for i in range(k):
                r = random.randint(0, len(data_) - 1)
                result.append(list(data_[r].propiedades.values()))
            
                data_.remove(data_[r])
        
        return result if (len(result) == k) else Methods.Concatenate(result, emergency, k)
    
   
    @staticmethod
    def Concatenate(result, emergency, k):
        len_res = len(result)
        for i in range(k - len_res):
            r = random.randint(0, len(emergency) - 1)
            result.append(emergency[r])
            return result


    @staticmethod
    def AsignToBestCluster(data: list, centroids: list):
        hubo_cambio = False

        for data_ in data:
            if hasattr(data_, "group"):
                dist_t = Methods.DistVectorial(list(data_.propiedades.values()), centroids[data_.group])
            else: dist_t = float('inf')
            for centroid in centroids:
                dist_a = Methods.DistVectorial(list(data_.propiedades.values()), centroid)
                if (dist_a < dist_t): 
                    data_.group = centroids.index(centroid)
                    dist_t = dist_a
                    hubo_cambio = True

        return hubo_cambio

    

    @staticmethod
    def GetMedia_dict(propiedades: dict):
        result = 0
        for key in propiedades.keys():
            result += key
        return result / len(propiedades.keys())
    
    @staticmethod
    def DistVectorial(vect1: list, vect2: list):
        result = 0
        for i in range(len(vect1)):
            if(vect1[i] < 1 and vect2[i] < 1):
                result += ((vect1[i] - vect2[i])**2)
            else:
                result += (vect1[i] - vect2[i]) ** 2
        result = pow(result, 1/2)
        
        return result
    
    @staticmethod
    def RecalculateCentroids(data, centroids):
        groups = []
        for i in range(len(centroids)):
            groups.append([])

        for data_ in data:
            groups[data_.group].append(data_)

        for i in range(len(centroids)):
            centroids[i] = Methods.GetMedia_vect(groups[i], centroids[i])
        
        for i in range(len(groups)):
            actual_dist = float('inf')
            for element in groups[i]:
                dist = Methods.DistVectorial(list(element.propiedades.values()), centroids[i])
                if (dist < actual_dist):
                    actual_dist = dist
                    new_centroid = element
            for k in range(len(centroids[i])):
                props = list(element.propiedades.values())
                centroids[i][k] = props[k]


        return groups
        
    @staticmethod
    def GetMedia_vect(group, centroid):
        group_size = len(group)
        if (len(group) != 0):
            result = []
            cen_size = len(centroid)
            for i in range(cen_size):
                result.append(0)

            for data_ in group:
                props = list(data_.propiedades.values())
                for i in range(len(props)):
                    result[i] += props[i]
            
            for i in range(cen_size):
                result[i] = result[i] / group_size

            return result
        
        else: return centroid

    @staticmethod
    def RazonDeProp(data):
        for data_ in data:
            E_Ped = data_.propiedades["E_Ped"]
            E_AdM = data_.propiedades["E_AdM"]
            E_AdJ = data_.propiedades["E_AdJ"]

            data_.propiedades["E_Ped"] = E_AdM / E_Ped
            data_.propiedades["E_AdM"] = E_AdM / E_AdJ
            data_.propiedades["E_AdJ"] = E_AdJ / E_Ped

    @staticmethod
    def GetMediaDist_to_Centroid(group, centroid):
        result = 0
        for ent in group:
            result += Methods.DistVectorial(list(ent.propiedades.values()), centroid)
        
        result = result/len(group) if len(group) != 0 else result
        return result

    @staticmethod
    def GetGlobalVariance(groups, centroids):
        entities = []
        for group in groups:
            for ent in group:
                entities.append(ent)
        global_centroid = Methods.GetMedia_vect(entities, centroids[0])

        result = 0
        for i, group in enumerate(groups):
            result += len(group) * Methods.DistVectorial(centroids[i], global_centroid)

        return result / (len(groups) - 1)
    
    @staticmethod
    def GetInnerVariance(groups, centroids):
        cant_of_entities = 0
        result = 0
        for i, group in enumerate(groups):
            cant_of_entities += len(group)
            for j,ent in enumerate(group):
                result += Methods.DistVectorial(list(ent.propiedades.values()), centroids[i])
        
        return result / (cant_of_entities - len(centroids)) 

    @staticmethod
    def GetRandomColor():
        return  "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
    @staticmethod
    def GeneratePointsAroundTo(coords, n, eps, eps_=0):   #se espera que coord tenga valores entre 0 y 1, qu seria la proporcion de lo que se quiere en cuanto a valor max menos valor min
        result = []
        if(eps_ == 0):
            for i in range(n):
                new_coord = []
                for coord in coords:
                    key = coord[0]
                    val = random.uniform(coord[1] - eps, coord[1] + eps)
                    new_coord.append((key,val))
                point = Point(new_coord)
                result.append(point)
                new_coord = []
        
        else:
            for i in range(n):
                new_coord = []
                for coord in coords:
                    key = coord[0]
                    ratio = random.uniform(eps, eps_)
                    angle = random.uniform(0, 2*math.pi)
                    val = coord[1] + ratio * math.cos(angle) if i == 0 else coord[1] + ratio * math.sin(angle)
                    new_coord.append((key,val))
                point = Point(new_coord)
                result.append(point)
                new_coord = []

        return result

    @staticmethod
    def InitializateCentroid(groups, centroid):
        for i in range(len(groups)):
            if (len(groups[i]) != 0):
                for propiedad in list(groups[i][0].propiedades.values()):
                    centroid.append(0)
                return
    
    @staticmethod
    def Average(list: list):
        result = 0
        for element in list:
            result += element
        len_ = len(list)
        return result / len_