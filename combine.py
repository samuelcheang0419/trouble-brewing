import pandas as pd
import numpy as np

'''For predicted future data'''

def read(location):
    df = pd.read_csv(location, index_col = 0).applymap(lambda x: [x])
    return df

def combine(year):
    '''
    Combines multiple 'asc' files ((similar to csv files, but for cilmate data) \
    of 19 different bioclimatic variables from the same time period range into \
    a single file
    '''
    df_list = []
    for i in xrange(1, 20):
        path = 'processed-data/{}_bio_{}.asc'.format(year, i)
        df_list.append(read(path))
    final_df = df_list.pop(0)
    while len(df_list) != 0:
        final_df += df_list.pop(0)
    final_df = transform(final_df)
    final_df.to_csv('combined-data/{}_combined.asc'.format(year))

def transform(df):
    '''
    Takes a dataframe and panda-stacks it based on latitude and longitude

    latitude range: -90~90
    longitude range: -180~180
    format: (latitude, longitude)
    '''
    columns = [
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
    df = df.stack().reset_index().rename(columns = {'level_0': 'Latitude', 'level_1': 'Longitude'})
    for i, col in enumerate(columns):
        df[col] = df[0].apply(lambda x: x[i])
    df.drop(labels = 0, axis = 1, inplace = True)
    df = df[df[columns].apply(lambda row: True if set(row) != {-9999.0} else False, axis = 1)]
    df.drop(df[df['Annual Mean Temperature'] == -9999.0].index, inplace = True)
    return df

if __name__ == '__main__':
    combine('2030')
    combine('2050')
