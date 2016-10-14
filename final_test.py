import pandas as pd
import numpy as np
import sys
from collections import Counter
import cPickle as pickle

def round_to_value(number):
    return round((round(number / 0.5) * 0.5), 2)

def load_coffee_df():
    coffee_df = pd.read_csv('processed-data/coffee_df.csv', index_col = 0)
    coffee_df = coffee_df[coffee_df['decimallatitude'] >= -34]
    coffee_df = coffee_df[coffee_df['decimallatitude'] <= 21]
    coffee_df = coffee_df[coffee_df['decimallongitude'] >= -95]
    coffee_df = coffee_df[coffee_df['decimallongitude'] <= -34]
    coffee_df['latitude*100'] = (coffee_df['decimallatitude'].apply(round_to_value) * 100).apply(int)
    coffee_df['longitude*100'] = (coffee_df['decimallongitude'].apply(round_to_value) * 100).apply(int)
    return coffee_df

def load_labels_df():
    labels_df = pd.read_csv('combined-data/labels.csv', index_col = 0)
    labels_df['latitude*100'] = (labels_df['Latitude'].apply(round_to_value) * 100).apply(int)
    labels_df['longitude*100'] = (labels_df['Longitude'].apply(round_to_value) * 100).apply(int)
    return labels_df

def predict(similarity_df, labels_df, baseline_df, coffee_df):
    recommendations = list()
    for row in coffee_df.iterrows():
        lat = row[1]['latitude*100']
        lon = row[1]['longitude*100']
        temp = labels_df[labels_df['latitude*100'] == lat]
        temp = temp[temp['longitude*100'] == lon]
        index = temp['Index'].values[0]
        best_locations = similarity_df.loc[index].sort_values()[:10].index.tolist()
        recommendations.extend(best_locations)
    c = Counter(recommendations)
    return map(lambda x: x[0], c.most_common(10))

def run_final():
    d = dict()
    species = [ 2895345.,  2895528.,  2895393.,  2907301.,  2895473.,  2895439.,
        2895488.,  2895563.,  2895338.,  2895464.,  2895475.,  2895342.,
        2907296.,  7389152.]
    labels_df = load_labels_df()
    baseline_df = labels_df[labels_df['Year'] == 'Baseline']
    y = '2030'
    usecols = xrange(13653, 13653 + 5235)
    similarity_df = pd.read_csv('combined-data/similarity_array.csv', index_col = 0, usecols = usecols)
    similarity_df.set_index(labels_df['Index'], inplace = True)
    for s in species:
        print s
        print d
        coffee_df = load_coffee_df()
        coffee_df = coffee_df[coffee_df['specieskey'] == s]
        d[(s, y)] = predict(similarity_df, labels_df, baseline_df, coffee_df)
    y = '2050'
    usecols = xrange(13653 + 5235, 13653 + 5235 + 4890)
    similarity_df = pd.read_csv('combined-data/similarity_array.csv', index_col = 0, usecols = usecols)
    similarity_df.set_index(labels_df['Index'], inplace = True)
    for s in species:
        print s
        print d
        coffee_df = load_coffee_df()
        coffee_df = coffee_df[coffee_df['specieskey'] == s]
        d[(s, y)] = predict(similarity_df, labels_df, baseline_df, coffee_df)
    with open('final_predictions.pickle', 'wb') as f:
        pickle.dump(d, f)

if __name__ == '__main__':
    run_final()
