import folium
import random

class BookMark:
    def __init__(self):
        pass

    @staticmethod
    def MarcadoresDeGrupos(map: folium.Map, groups):

        for i,group in enumerate(groups[0][0]):
            for j, ent in enumerate(group):
                coordinate_x = ent.coords[0]
                coordinate_y = ent.coords[1]
                CH = round(groups[1], 2)
                DB = round(groups[2], 2)
                color = BookMark.GetColor(ent.group)
                icon = folium.Icon(color=color)
                folium.Marker(location=[coordinate_x, coordinate_y],
                              popup=f"Municipio: {ent.nombre} \nProvincia: {ent.provincia} \n E_AdM / E_Ped: {ent.propiedades['E_Ped']}\n E_AdM / A_AdJ: {ent.propiedades['E_AdM']} \n E_AdJ / E_Ped: {ent.propiedades['E_AdJ']} CH: {CH} \n DB: {DB}",
                              icon=icon).add_to(map)
        
        map.save("mi_mapa.html")
    
    @staticmethod
    def GetColor(n):
        colors =['red', 'blue', 'green', 'purple', 'orange',
                 'gray', 'black', 'darkred', 'lightblue',
                 'darkgreen', 'lightgreen', 'pink',
                 'cadetblue', 'lightgray']
        
        if (n < len(colors)):
            return colors[n]
        else: 
            random_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255),
                                                        random.randint(0, 255),
                                                        random.randint(0, 255))
            return random_color