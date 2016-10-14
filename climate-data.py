import pandas as pd
import numpy as np

def load_df(location):
    '''
    Load and return subset of an 'asc' file (with some additional cleaning)
    '''
    rows = np.arange(-180, -180+(2160+0.5)/6.0, 1.0/6, dtype = float)
    cols = np.arange(-60, -60+899/6.0, 1.0/6, dtype = float)
    df = pd.read_csv(location, skiprows = 6, names = rows, sep = ' ')
    df = df.dropna(axis = 1)
    df.set_index(cols, inplace = True)
    df = df.astype(int)
    return df.applymap(lambda x: [x])

def transform(lst):
    if len(lst) == 0:
        return -9999
    else:
        return sum(lst) * 1.0 / len(lst)

def combine(year):
    '''
    Combines multiple 'asc' files of 19 different bioclimatic variables \
    depending on the year into a single csv file for further processing
    '''
    filenames = ['bio_1.asc', 'bio_2.asc', 'bio_3.asc', 'bio_4.asc',
    'bio_5.asc', 'bio_6.asc', 'bio_7.asc', 'bio_8.asc', 'bio_9.asc',
    'bio_10.asc', 'bio_11.asc', 'bio_12.asc', 'bio_13.asc', 'bio_14.asc',
    'bio_15.asc', 'bio_16.asc', 'bio_17.asc', 'bio_18.asc', 'bio_19.asc']
    if year == '2030':
        directories = [
        'gfdl_esm2m_rcp2_6_2030s_bio_10min_r1i1p1_no_tile_asc',
        'gfdl_esm2m_rcp4_5_2030s_bio_10min_r1i1p1_no_tile_asc',
        'gfdl_esm2m_rcp6_0_2030s_bio_10min_r1i1p1_no_tile_asc',
        'gfdl_esm2m_rcp8_5_2030s_bio_10min_r1i1p1_no_tile_asc',
        'ipsl_cm5a_lr_rcp2_6_2030s_bio_10min_r1i1p1_no_tile_asc',
        'ipsl_cm5a_lr_rcp4_5_2030s_bio_10min_r1i1p1_no_tile_asc',
        'ipsl_cm5a_lr_rcp6_0_2030s_bio_10min_r1i1p1_no_tile_asc',
        'ipsl_cm5a_lr_rcp8_5_2030s_bio_10min_r1i1p1_no_tile_asc',
        'miroc_esm_chem_rcp2_6_2030s_bio_10min_r1i1p1_no_tile_asc',
        'miroc_esm_chem_rcp4_5_2030s_bio_10min_r1i1p1_no_tile_asc',
        'miroc_esm_chem_rcp6_0_2030s_bio_10min_r1i1p1_no_tile_asc',
        'miroc_esm_chem_rcp8_5_2030s_bio_10min_r1i1p1_no_tile_asc'
        ]
    elif year == '2050':
        directories = [
        'gfdl_esm2m_rcp2_6_2050s_bio_10min_r1i1p1_no_tile_asc',
        'gfdl_esm2m_rcp4_5_2050s_bio_10min_r1i1p1_no_tile_asc',
        'gfdl_esm2m_rcp6_0_2050s_bio_10min_r1i1p1_no_tile_asc',
        'gfdl_esm2m_rcp8_5_2050s_bio_10min_r1i1p1_no_tile_asc',
        'ipsl_cm5a_lr_rcp2_6_2050s_bio_10min_r1i1p1_no_tile_asc',
        'ipsl_cm5a_lr_rcp4_5_2050s_bio_10min_r1i1p1_no_tile_asc',
        'ipsl_cm5a_lr_rcp6_0_2050s_bio_10min_r1i1p1_no_tile_asc',
        'ipsl_cm5a_lr_rcp8_5_2050s_bio_10min_r1i1p1_no_tile_asc',
        'miroc_esm_chem_rcp2_6_2050s_bio_10min_r1i1p1_no_tile_asc',
        'miroc_esm_chem_rcp4_5_2050s_bio_10min_r1i1p1_no_tile_asc',
        'miroc_esm_chem_rcp6_0_2050s_bio_10min_r1i1p1_no_tile_asc',
        'miroc_esm_chem_rcp8_5_2050s_bio_10min_r1i1p1_no_tile_asc'
        ]
    for filename in filenames:
        df_list = []
        for directory in directories:
            path = 'climate-data/{}/{}'.format(directory, filename)
            df_list.append(load_df(path))
        if len(df_list) != 12:
            return 'df_list does not have 12 dataframes'
        final_df = df_list.pop(0)
        while len(df_list) != 0:
            final_df += df_list.pop(0)
        final_df = final_df.applymap(lambda x: filter(lambda y: y != -9999, x))
        final_df = final_df.applymap(transform)
        final_df.to_csv('processed-data/{}_{}'.format(year, filename))
        # exported csv file can be read into pandas with pd.read_csv('filename', index_col = 0)

if __name__ == '__main__':
    combine('2030')
    combine('2050')
