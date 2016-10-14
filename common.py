import folium
import pandas as pd
import numpy as np
import graphlab

class Marker(object):

    def __init__(self, row, color, opacity):
        row = row[1]
        self.color = color
        self.opacity = opacity
        if 'decimallatitude' in row.index:
            self.lat = row['decimallatitude']
            self.lon = row['decimallongitude']
        else:
            self.lat = row['Latitude']
            self.lon = row['Longitude']

    def create(self):
        marker = folium.RegularPolygonMarker(location = [self.lat, self.lon],
                                            color = self.color,
                                            fill_color = self.color,
                                            opacity = self.opacity,
                                            fill_opacity = self.opacity,
                                            number_of_sides = 4,
                                            rotation = 45,
                                            radius = 5)
        return marker

def load_coffee_df(restriction = None):
    coffee_df = pd.read_csv('processed-data/coffee_df.csv', index_col = 0)
    if restriction == None:
        return coffee_df
    coffee_df = coffee_df[coffee_df['decimallatitude'] >= -34]
    coffee_df = coffee_df[coffee_df['decimallatitude'] <= 21]
    coffee_df = coffee_df[coffee_df['decimallongitude'] >= -95]
    coffee_df = coffee_df[coffee_df['decimallongitude'] <= -34]
    coffee_df['latitude*100'] = (coffee_df['decimallatitude'].apply(round_to_value) * 100).apply(int)
    coffee_df['longitude*100'] = (coffee_df['decimallongitude'].apply(round_to_value) * 100).apply(int)
    return coffee_df
    
def round_to_value(number):
    return round((round(number / 0.5) * 0.5), 2)
