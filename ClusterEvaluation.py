from Methods import Methods
import sys

class ClusterEv:
    def __init__(self):
        pass

    @staticmethod
    def DaviesBouldin(groups):
        centroids = []
        for group in groups:
            centroid = []
            Methods.InitializateCentroid(groups, centroid)
            centroids.append(Methods.GetMedia_vect(group, centroid))

        dist_to_centroid = []
        for i in range(len(groups)):
            dist_to_centroid.append(Methods.GetMediaDist_to_Centroid(groups[i], centroids[i]))
        
        result = 0

        for i in range(len(groups)):
            min = -sys.maxsize
            for j in range(len(groups)):
                if (i == j): continue
                value = (dist_to_centroid[i] + dist_to_centroid[j])/Methods.DistVectorial(centroids[i], centroids[j])
                if (value > min): min = value
            
            result += min

        return result/len(groups) 
    
    @staticmethod
    def CalinskiHarabasz(groups):
        centroids = []
        for group in groups:
            centroid = []
            Methods.InitializateCentroid(groups, centroid)
            centroids.append(Methods.GetMedia_vect(group, centroid))
                
        global_variance = Methods.GetGlobalVariance(groups, centroids)
        inner_variance = Methods.GetInnerVariance(groups, centroids)

        return global_variance / inner_variance
    
    @staticmethod
    def Silouette(groups):
        a_i = [] #distancia promedio de elemento i con respecto a elementos de su mismo grupo
        b_i = [] #distancia promedio de elemento i con respecto al grupo más cercano distinto del suyo
        s_i = [] #resultado final para cada elemento i del conjunto de datos

        for k in range(0, len(groups), 1):
            a_i_ = []
            b_i_ = []
            s_i_ = []

            if(len(groups[k]) > 1):
                for i in range(0, len(groups[k]), 1):
                    sum_d_i_j = 0
                    for j in range(0, len(groups[k]), 1):
                        if(i != j):
                            sum_d_i_j += Methods.DistVectorial(list(groups[k][i].propiedades.values()), list(groups[k][j].propiedades.values()))
                    a_i_value = sum_d_i_j / (len(groups[k]) - 1)
                    a_i_.append(a_i_value)

                    b_i_min_value = sys.maxsize
                    for k_ in range(0, len(groups), 1):
                        if(k != k_):
                            sum_C_k = 0
                            for j in range(0, len(groups[k_]), 1):
                                sum_C_k += Methods.DistVectorial(list(groups[k][i].propiedades.values()), list(groups[k_][j].propiedades.values()))
                            b_i_value = sum_C_k / len(groups[k_])

                            if(b_i_min_value > b_i_value):
                                b_i_min_value = b_i_value
                     
                    b_i_.append(b_i_min_value)

                    s_i_value = (b_i_value - a_i_value) / max(b_i_value, a_i_value)
                    s_i_.append(s_i_value)

                a_i.append(a_i_)
                b_i.append(b_i_)
                s_i.append(s_i_)

            else:
                s_i.append([0])

        s_result = []
        for col in s_i:
            for element in col:
                s_result.append(element)
        
        s_result = Methods.Average(s_result)
         
        return s_result
            
                         
                 


            
