import pandas as pd
import numpy as np
import graphlab
from sklearn import preprocessing

def load():
    '''
    Load and clean original dataset. Cleaning steps include dropping columns and \
    rows not needed for this project, encoding and converting categorical variables.

    The majority of the data cleaning is done here, with some additional steps \
    taken depending on the need

    Each row in the resulting dataframe is a single instance of a coffee species \
    in a location.
    '''
    df = pd.read_csv('georeferenced.csv', sep = None)
    df.drop(['gbifid', 'datasetkey', 'occurrenceid', 'kingdom', 'phylum', \
            'class', 'order', 'family', 'genus', 'species', 'infraspecificepithet', \
            'locality', 'publishingorgkey', 'coordinateuncertaintyinmeters', \
            'coordinateprecision', 'elevationaccuracy', 'depth', 'depthaccuracy', \
            'eventdate', 'day', 'month', 'basisofrecord', 'institutioncode', \
            'collectioncode', 'catalognumber', 'recordnumber', 'identifiedby', \
            'license', 'rightsholder', 'recordedby', 'typestatus', 'establishmentmeans', \
            'lastinterpreted', 'mediatype', 'issue'], axis = 1, inplace = True)
    df.dropna(axis = 0, subset = ['specieskey'], how = 'any', inplace = True)
    df.dropna(axis = 0, subset = ['countrycode'], how = 'any', inplace = True)
    df['country'] = df['countrycode'].apply(country_fn)
    df.drop(df[df['country'] == 'Spain'].index, inplace = True)
    df.drop(df[df['country'] == 'Burkina Faso'].index, inplace = True)
    df.drop(df[df['country'] == 'Sweden'].index, inplace = True)
    df.drop(df[df['country'] == 'Eritrea'].index, inplace = True)
    df.drop(df[df['country'] == 'Zimbabwe'].index, inplace = True)
    df.drop(df[df['country'] == 'South Africa'].index, inplace = True)
    df.drop(df[df['country'] == 'Yemen'].index, inplace = True)
    df.drop(df[df['country'] == 'Somalia'].index, inplace = True)
    le = preprocessing.LabelEncoder()
    df['countrycode'] = le.fit_transform(df['country'])
    df['decimallatitude'] = df['decimallatitude'].apply(round_to_value)
    df['decimallongitude'] = df['decimallongitude'].apply(round_to_value)
    df['latlon'] = df['decimallatitude'] + ', ' + df['decimallongitude']
    df.to_csv('processed-data/coffee_df.csv')
    return le, df

def round_to_value(number):
    return str(round((round(number / 1) * 1), 2))

def country_fn(country):
    '''
    Converts country codes (e.g. US, PR, MX etc.) to full country names
    '''
    countries = [
        ('MG', 'Madagascar'), ('BR', 'Brazil'), ('CO', 'Colombia'),
        ('CM', 'Cameroon'), ('CD', 'Democratic Republic of the Congo'),
        ('TZ', 'Tanzania'), ('GA', 'Georgia'), ('MX', 'Mexico'), ('ET', 'Ethiopia'),
        ('AU', 'Australia'), ('KE', 'Kenya'), ('TW', 'Taiwan'), ('CR', 'Costa Rica'),
        ('CI', "Cote d'Ivoire"), ('EC', 'Ecuador'), ('GH', 'Ghana'),
        ('US', 'United States'), ('NI', 'Nicaragua'), ('MW', 'Malawi'),
        ('BO', 'Bolivia'), ('MZ', 'Mozambique'), ('PR', 'Puerto Rico'),
        ('BJ', 'Benin'), ('CN', 'China'), ('LR', 'Liberia'), ('PA', 'Panama'),
        ('AO', 'Angola'), ('GN', 'Guinea'), ('RE', 'Reunion'), ('PE', 'Peru'),
        ('HN', 'Honduras'), ('JM', 'Jamaica'), ('VE', 'Venezuela'),
        ('CF', 'Central African Republic'), ('SV', 'El Salvador'), ('PY', 'Paraguay'),
        ('NG', 'Nigeria'), ('ES', 'Spain'), ('JP', 'Japan'), ('PF', 'French Polynesia'),
        ('PG', 'Papua New Guinea'), ('NC', 'New Caledonia'), ('YE', 'Yemen'),
        ('GQ', 'Equatorial Guinea'), ('MW', 'Malawi'), ('ZM', 'Zambia'),
        ('MU', 'Mauritius'), ('ID', 'Indonesia'), ('SO', 'Somalia'), ('BZ', 'Belize'),
        ('YT', 'Mayotte'), ('CG', 'Congo'), ('TG', 'Togo'),  ('CU', 'Cuba'),
        ('TH', 'Thailand'), ('RW', 'Rwanda'), ('UG', 'Uganda'), ('GT', 'Guatemala'),
        ('TT', 'Trinidad and Tobago'), ('NF', 'Norfolk Island'), ('ER', 'Eritrea'),
        ('SL', 'Sierra Leone'), ('SR', 'Suriname'), ('BF', 'Burkina Faso'),
        ('MY', 'Malaysia'), ('ZW', 'Zimbabwe'), ('DO', 'Dominican Republic'),
        ('IN', 'India'), ('CK', 'Cook Islands'), ('NL', 'Netherlands'),
        ('FM', 'Federated States of Micronesia'), ('NZ', 'New Zealand'),
        ('SE', 'Sweden'), ('PH', 'Philippines'), ('FR', 'France'), ('DM', 'Dominica'),
        ('KM', 'Comoros'), ('FJ', 'Fiji'), ('VN', 'Vietnam'), ('GD', 'Grenada'),
        ('ZA', 'South Africa'),('GY', 'Guyana')
    ]
    countries_df = pd.DataFrame(countries, columns = ['Code', 'Country'])
    return countries_df[countries_df['Code'] == country]['Country'].values[0]

def recommender_preprocessing(df):
    '''
    Converts dataframe of individual coffee instances to a 'recommender'-style \
    dataframe consisting of only coffee species key, latitude/longitude and \
    occurrence (quantity).
    '''
    recommender_df = pd.DataFrame(columns=['specieskey', 'latlon', 'occurrence'], dtype = int)
    for species in df['specieskey'].unique():
        latlon = df[df['specieskey'] == species]['latlon'].value_counts()
        latlon = latlon.rename('occurrence')
        latlon = latlon.to_frame()
        latlon['latlon'] = latlon.index
        latlon['specieskey'] = species
        latlon = latlon[['specieskey', 'latlon', 'occurrence']]
        recommender_df = pd.concat([recommender_df, latlon], ignore_index = True)
    recommender_df['specieskey'] = recommender_df['specieskey'].astype(str)
    recommender_df.to_csv('processed-data/recommmender_df.csv')
    return recommender_df

def recommender(df):
    sf = graphlab.SFrame(df)
    rec = graphlab.recommender.factorization_recommender.create(sf, user_id = 'specieskey', item_id = 'latlon', target = 'occurrence', side_data_factorization=False, max_iterations = 250, random_seed = 0)
    rec.save('recommendations/recommendation')
    return rec

if __name__ == '__main__':
    le, df = load()
    recommender_df = recommender_preprocessing(df)
    recommender(recommender_df)
