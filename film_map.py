"""
Film map Module

Link: https://github.com/MartaSamoilenkoPn/folmap.git
"""
import argparse
from math import radians, cos, sin, asin, sqrt
import folium
from geopy.geocoders import Nominatim

def calculate_distance(lontitude1, latitude1, lontitude2, latitude2) -> int:
    """
    Calculate distance using haversine formula
    """
    radius = 6371
    lontitude1, latitude1, lontitude2, latitude2 = map(radians, \
                                                    [lontitude1, latitude1, lontitude2, latitude2])

    dlon = lontitude2 - lontitude1
    dlat = latitude2 - latitude1
    return 2 * asin(sqrt(sin(dlat/2)**2 + cos(latitude1)\
                          * cos(latitude2) * sin(dlon/2)**2)) * radius

def read_file(file_name : str, year : int) -> dict():
    """
    Read file and return dictionary with name of film as key,
    year and cordinates as value
    """
    with open(file_name) as file:
        geo_dict = {}
        list_lines = file.readlines()
        for _ in range(15):
            list_lines.pop(0)
        for line in list_lines:
            line.replace('\t', '')
        for line_index in range(15,20000):
            line = list_lines[line_index]
            line = line.split('\t')
            line = [element for element in line if element != '']
            line[0] = line[0].split('" ')
            line[0][0] = line[0][0].replace('"', '')
            line[-1] = line[-1].replace('\n', '')
            line[0][1] = line[0][1].replace('(', '')
            line[0][1] = line[0][1].replace(')', '')
            line[0][1] = line[0][1].split(" ")[0]
            line[-1] = line[-1].replace('(', '')
            line[-1] = line[-1].replace(')', '')
            try:
                if int(line[0][1]) == year:
                    geo_dict[line[0][0]] = [line[0][1], line[-1]]
            except ValueError:
                continue
        return geo_dict




def create_map(geo_dict : dict, year : int, lat2 : int, lon2 : int):
    """
    Create map
    """
    map = folium.Map(tiles="Stamen Terrain")
    geolocator = Nominatim(user_agent="Marta")
    fg = folium.FeatureGroup(name="films")
    fg1 = folium.FeatureGroup(name="lines")
    map.add_child(folium.Marker(location=[lat2, lon2], popup="Your point", icon = folium.Icon(color="red")))
    for key in geo_dict:
        try:
            location = geolocator.geocode(geo_dict[key][1])
            geo_dict[key].append(calculate_distance(location.latitude,\
                                                     location.longitude, lat2, lon2))
        except AttributeError:
            geo_dict[key].append(float('inf'))
            continue
    geo_dict = dict(sorted(geo_dict.items(), key = lambda item : item[1][2]))
    for index, key in enumerate(geo_dict):
            if index < 20:
                try:
                    location = geolocator.geocode(geo_dict[key][1])
                    fg.add_child(folium.Marker(location=[location.latitude, location.longitude],
                                                popup=key + '\n' + str(year),
                                                icon=folium.Icon(color="black")))
                    fg1.add_child(folium.PolyLine([[lat2, lon2], [location.latitude, location.longitude]]))
                except AttributeError:
                    continue
            else:
                break
    map.add_child(fg)
    map.add_child(fg1)
    map.add_child(folium.LayerControl())
    map.save('Marked_Map.html')

parser = argparse.ArgumentParser()
parser.add_argument("year", type = int, help = "path to dir")
parser.add_argument("cordinate1", type= int, help= "cordinate 1")
parser.add_argument("cordinate2", type= int, help= "cordinate 2")
parser.add_argument("path", type= str, help= "path to dataset")
args = parser.parse_args()

path = args.path
year = args.year
cordinate1 = args.cordinate1
cordinate2 = args.cordinate2
geo_dict = read_file(path, year)
create_map(geo_dict, year, cordinate1, cordinate2)
