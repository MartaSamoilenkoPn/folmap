# FOLMAP
Module represents top 10 films of the specific year, chosen by distance to the cordinates from the input.

## Short description of the module
Module uses argpars for input, where there are year of films, and cordinates.
To calculate distance between film coordinates and coordinates from the input we use haversine formula : 
![alt text](https://user-images.githubusercontent.com/2789198/27240436-e9a459da-52d4-11e7-8f84-f96d0b312859.png)

## Instalation
```bash
pip install pandas
pip install folium
```

## Libraries to import
```bash
import folium
from geopy.geocoders import Nominatim
import argparse

from math import radians, cos, sin, asin, sqrt
```

