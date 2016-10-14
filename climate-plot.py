import pandas as pd
import numpy as np
import folium
import sys
import common

def round_to_value(number):
    return round((round(number / 0.5) * 0.5), 2)

def plot(species, year):
    coffee_df = common.load_coffee_df(restriction = 'southamerica')
    if species not in coffee_df['scientificname'].unique():
        return 'Species does not exist'
    key = coffee_df[coffee_df['scientificname'] == species].iloc[0]['specieskey']
    coffee_df = coffee_df[coffee_df['specieskey'] == key]
    m = folium.Map(location = [-7.5, -67.5], zoom_start = 3)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    df = pd.read_csv('prediction-data/final_predictions_{}_{}.csv'.format(year, key), header = None)
    df.columns = ['Index', 'Similarity']
    df['Year'] = df['Index'].apply(lambda x: int(x.split()[0][1:1+4]))
    df['Latitude'] = df['Index'].apply(lambda x: float(x.split()[1][:-2]))
    df['Longitude'] = df['Index'].apply(lambda x: float(x.split()[2][:-1]))
    one = df[df['Similarity'] <= 1.3]
    two = df[(df['Similarity'] > 1.3) & (df['Similarity'] <= 3)]
    three = df[(df['Similarity'] > 3) & (df['Similarity'] <= 4.5)]
    for row in coffee_df.iterrows():
        marker = common.Marker(row, 'green', 0.4)
        m.add_children(marker.create())
    for row in three.iterrows():
        marker = common.Marker(row, '#ffeda0', 0.2)
        m.add_children(marker.create())
    for row in two.iterrows():
        marker = common.Marker(row, '#feb24c', 0.4)
        m.add_children(marker.create())
    for row in one.iterrows():
        marker = common.Marker(row, '#f03b20', 0.4)
        m.add_children(marker.create())
    m.add_children(folium.LatLngPopup())
    m.save('recommendations/{}/{}_{}.html'.format(year, species, year))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Input incorrect'
        print sys.argv
        sys.exit()
    species = sys.argv[1]
    '''
    Possible species:
    array(['Coffea arabica L.', 'Coffea robusta L.Linden',
       'Coffea canephora Pierre ex A.Froehner',
       'Coffea dewevrei De Wild. & T.Durand',
       'Psilanthus ebracteolatus Hiern',
       'Coffea kapakata (A.Chev.) Bridson', 'Coffea eugenioides S.Moore',
       'Coffea liberica Hiern', 'Coffea stenophylla G.Don',
       'Coffea arabica Benth.', 'Coffea congensis A.Froehner',
       'Coffea salvatrix Swynn. & Philipson', 'Coffea racemosa Lour.',
       'Coffea excelsa A.Chev.', 'Coffea laurentii De Wild.',
       'Coffea klainii Pierre ex De Wild.', 'Coffea humilis A.Chev.',
       'Coffea kapakata Hort.', 'Coffea brevipes Hiern',
       'Coffea liberica var. dewevrei (De Wild. & T.Durand) Lebrun',
       'Psilanthus travancorensis (Wight & Arn.) J.-F.Leroy',
       'Coffea rigida Miq.']
       '''
    year = int(sys.argv[2])
    plot(species, year)
