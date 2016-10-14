import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
import itertools
import cPickle as pickle

def read(location):
    columns = [
    'Latitude',
    'Longitude',
    'Annual Mean Temperature',
    'Mean Diurnal Range (Mean of monthly (max temp - min temp)',
    'Isothermality (BIO2/BIO7) (* 100)',
    'Temperature Seasonality (standard deviation *100)',
    'Max Temperature of Warmest Month',
    'Min Temperature of Coldest Month',
    'Temperature Annual Range (BIO5-BIO6)',
    'Mean Temperature of Wettest Quarter',
    'Mean Temperature of Driest Quarter',
    'Mean Temperature of Warmest Quarter',
    'Mean Temperature of Coldest Quarter',
    'Annual Precipitation',
    'Precipitation of Wettest Month',
    'Precipitation of Driest Month',
    'Precipitation Seasonality (Coefficient of Variation)',
    'Precipitation of Wettest Quarter',
    'Precipitation of Driest Quarter',
    'Precipitation of Warmest Quarter',
    'Precipitation of Coldest Quarter'
    ]
    df = pd.read_csv(location, usecols = columns)
    return df

def round_to_value(number):
    return round((round(number / 0.5) * 0.5), 2)

def build_df():
    '''
    Combine all processed dataframes of bioclimatic variables from all time \
    periods into a single dataframe to compute similarities between locations
    '''
    df_baseline = read('combined-data/baseline_combined.asc')
    df_baseline['Latitude'] = df_baseline['Latitude'].apply(round_to_value)
    df_baseline['Longitude'] = df_baseline['Longitude'].apply(round_to_value)
    df_baseline.drop_duplicates(subset = ['Latitude', 'Longitude'], inplace = True)
    df_2030 = read('combined-data/2030_combined.asc')
    df_2050 = read('combined-data/2050_combined.asc')
    for col in df_baseline.columns:
        max_baseline = df_baseline[col].max()
        min_baseline = df_baseline[col].min()
        df_2030 = df_2030[df_2030[col] <= max_baseline]
        df_2030 = df_2030[df_2030[col] >= min_baseline]
        df_2050 = df_2050[df_2050[col] <= max_baseline]
        df_2050 = df_2050[df_2050[col] >= min_baseline]
    df_baseline['Year'] = 'Baseline'
    df_2030['Year'] = '2030'
    df_2050['Year'] = '2050'
    df = pd.concat([df_baseline, df_2030, df_2050])
    df['Latitude'] = df['Latitude'].astype(str)
    df['Longitude'] = df['Longitude'].astype(str)
    df['Index'] = '(' + df['Year'] + ', ' + df['Latitude'] + ', ' + df['Longitude'] + ')'
    return df

def compute():
    '''
    Build similarity matrix of all latitude/longitude (accurate to the nearest \
    0.5) locations around South America based on 19 bioclimatic variables that \
    describe each location
    '''
    df = build_df()
    labels = pd.concat([df.pop('Index').to_frame(), df.pop('Year').to_frame(), df.pop('Latitude').to_frame(), df.pop('Longitude').to_frame()], axis = 1)
    df = df.astype(int)
    similarity_array = pdist(df, 'seuclidean')
    combinations = list(itertools.combinations(labels['Index'], 2))
    shape = labels.shape[0]
    tri = np.zeros((shape, shape))
    tri[np.triu_indices(shape, 1)] = similarity_array
    tri[np.tril_indices(shape, -1)] = similarity_array
    similarity_df = pd.DataFrame(data = tri, index = labels['Index'], columns = labels['Index'])
    baseline_shape = labels[labels['Year'] == 'Baseline'].shape[0]
    similarity_df.iloc[:baseline_shape-1, :baseline_shape-1] = 99999
    np.fill_diagonal(similarity_df.values, 99999)
    labels.to_csv('combined-data/labels.csv')
    similarity_df.to_csv('combined-data/similarity_array.csv')

if __name__ == '__main__':
    compute()
