import pandas as pd
import numpy as np

def load_df(location):
    '''
    Load and return subset of an 'asc' file
    '''
    rows = np.arange(-95.48999786377, -95.48999786377+(140+0.5)*0.43999999761581, 0.43999999761581, dtype = float)
    cols = np.arange(-34.059998631477, -34.059998631477+126*0.43999999761581, 0.43999999761581, dtype = float)
    df = pd.read_csv(location, skiprows = 6, names = rows, sep = ' ')
    df = df.dropna(axis = 1)
    df.set_index(cols, inplace = True)
    df = df.astype(int)
    return df

def combine():
    '''
    Using the load_df function above, take multiple 'asc' files and process them
    '''
    filenames = ['bio_1.asc', 'bio_2.asc', 'bio_3.asc', 'bio_4.asc',
    'bio_5.asc', 'bio_6.asc', 'bio_7.asc', 'bio_8.asc', 'bio_9.asc',
    'bio_10.asc', 'bio_11.asc', 'bio_12.asc', 'bio_13.asc', 'bio_14.asc',
    'bio_15.asc', 'bio_16.asc', 'bio_17.asc', 'bio_18.asc', 'bio_19.asc']
    directory = 'ncep_r2_baseline_1990s_bio_25min_andes_precis_asc'
    for filename in filenames:
        path = 'climate-data/{}/{}'.format(directory, filename)
        df = load_df(path)
        df.to_csv('processed-data/baseline_{}'.format(filename))
        # exported csv file can be read into pandas with pd.read_csv('filename', index_col = 0)

if __name__ == '__main__':
    combine()
