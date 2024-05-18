import sys
class EmptyClass:
    pass

class Point:
    def __init__(self, propiedades_):
        self.propiedades = {}
        for i in range(len(propiedades_)):
            self.propiedades[propiedades_[i][0]] = propiedades_[i][1]
        

class Node:
    def __init__(self, position):
        self.position = position
        self.elements = []
        self.adyacents = []

    @staticmethod
    def Organizate(data, eps):
        MaxMin = SearchMaxMin(data)
        k = DefineDeph(eps)
        nodes = [[None for _ in range(2**k)] for _ in range(2**k)]
        for fila in range(2**k):
            for col in range(2**k):    
                nodes[fila][col] = Node((fila, col))
        Adyacents(nodes)

        for data_ in data:
            Ubicate(data_, nodes, MaxMin, k)

        return nodes,MaxMin #nodes son los nodos creados con los elementos ya agregados y MaxMin es un array donde cada elemento corresponde con una dimension y tiene prop max y min




def SearchMaxMin(data):
    min = sys.maxsize
    max = -sys.maxsize
    x = EmptyClass()
    y = EmptyClass()
    z = EmptyClass()

    x.min = min
    x.max = max

    y.min = min
    y.max = max

    z.min = min
    z.max = max

    k = len(data[0].propiedades.values())
    if (k == 2):
        result = [x, y]
    else:
        result = [x, y, z]

    for data_ in data:
        data_values = list(data_.propiedades.values())
        for i in range(len(data_values)):
            val = data_values[i]
            if (val < result[i].min):
                result[i].min = val
            if (val > result[i].max):
                result[i].max = val

    return result

def DefineDeph(eps):
    k = 0
    while(eps < (1 / float(2**k))):
        k += 1
    return k - 1

def Adyacents(nodes):
    n = len(nodes)
    m = len(nodes[0])
    for i in range(n):
        for j in range(m):
            if (i + 1 < n):
                nodes[i][j].adyacents.append(nodes[i+1][j]) #derecha
                if (j + 1 < m):
                    nodes[i][j].adyacents.append(nodes[i+1][j+1]) #diagonal superior
                if (j - 1 >= 0):
                    nodes[i][j].adyacents.append(nodes[i+1][j-1]) #diagonal inferior
            if (i - 1 >= 0):
                nodes[i][j].adyacents.append(nodes[i-1][j]) #izquierda
                if (j + 1 < m):
                    nodes[i][j].adyacents.append(nodes[i-1][j+1]) #diagonal superior
                if (j - 1 >= 0):
                    nodes[i][j].adyacents.append(nodes[i-1][j-1]) #diagonal inferior
            if (j + 1 < m):
                nodes[i][j].adyacents.append(nodes[i][j+1]) #arriba
            if (j-1 >= 0):
                nodes[i][j].adyacents.append(nodes[i][j-1]) #abajo


def Ubicate(data_, nodes, MaxMin, k):
    params = list(data_.propiedades.values())
    if(len(params) == 2):
        Ubicate_2(nodes, data_, MaxMin[0].min, MaxMin[0].max, MaxMin[1].min, MaxMin[1].max, k-1, 0, 2**k, 0, 2**k)

def Ubicate_2(nodes, data_, x_min, x_max, y_min, y_max, k, kx_min, kx_max, ky_min, ky_max):
    if(k == 0):
        if(list(data_.propiedades.values())[0]<(x_max + x_min)/2 and list(data_.propiedades.values())[1]<(y_max+y_min)/2):
            data_.node = nodes[kx_min][ky_min]
            nodes[kx_min][ky_min].elements.append(data_)
            return True
        if(list(data_.propiedades.values())[0]>(x_max + x_min)/2 and list(data_.propiedades.values())[1]<(y_max+y_min)/2):
            data_.node = nodes[kx_min+1][ky_min]
            nodes[kx_min+1][ky_min].elements.append(data_)
            return True
        if(list(data_.propiedades.values())[0]<(x_max + x_min)/2 and list(data_.propiedades.values())[1]>(y_max+y_min)/2):
            data_.node = nodes[kx_min][ky_min+1]
            nodes[kx_min][ky_min+1].elements.append(data_)
            return True
        if(list(data_.propiedades.values())[0]>(x_max + x_min)/2 and list(data_.propiedades.values())[1]>(y_max+y_min)/2):
            data_.node = nodes[kx_min+1][ky_min+1]
            nodes[kx_min+1][ky_min+1].elements.append(data_)
            return True
    else:
        if(list(data_.propiedades.values())[0]<(x_max+x_min)/2 and list(data_.propiedades.values())[1]<(y_max+y_min)/2):
            return Ubicate_2(nodes,data_, x_min,(x_max + x_min)/2,y_min,(y_max+y_min)/2, k-1, kx_min,(kx_max+kx_min)//2,ky_min,(ky_max+ky_min)//2)
        if(list(data_.propiedades.values())[0]>(x_max + x_min)/2 and list(data_.propiedades.values())[1]<(y_max+y_min)/2):
            return Ubicate_2(nodes,data_, (x_max + x_min)/2,x_max,y_min,(y_max+y_min)/2, k-1, (kx_max+kx_min)//2,kx_max,ky_min,(ky_max+ky_min)//2)
        if(list(data_.propiedades.values())[0]<(x_max + x_min)/2 and list(data_.propiedades.values())[1]>(y_max+y_min)/2):
            return Ubicate_2(nodes,data_, x_min,(x_max + x_min)/2,(y_max+y_min)/2,y_max, k-1, kx_min,(kx_max+kx_min)//2,(ky_max+ky_min)//2,kx_max)
        if(list(data_.propiedades.values())[0]>(x_max + x_min)/2 and list(data_.propiedades.values())[1]>(y_max+y_min)/2):
            return Ubicate_2(nodes,data_, (x_max + x_min)/2,x_max,(y_max+y_min)/2,y_max, k-1, (kx_max+kx_min)//2,kx_max,(ky_max+ky_min)//2,ky_max)
