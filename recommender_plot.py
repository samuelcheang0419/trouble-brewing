import pandas as pd
import numpy as np
import folium
import graphlab
import common

def plot(species):

    '''
    Using the graphlab NMF recommender model (recommender_df), plot existing \
    locations of a coffee species on a world map, along with current recommended \
    locations based on current conditions.

    Color code:
    Green - Locations that are currently growing the coffee species
    Light yellow - Locations recommended as suitable for growth of coffee species \
                    (expected to grow as well as or better than the typical \
                    locations currently growing coffee)
    Red/orange - Locations HIGHLY recommended as suitable for growth of coffee \
                species (expected to grow as well as or better than even the best \
                location currently growing coffee)

    Input: species scientific name (datatype: string)
    Output: map with current and recommendation markers saved as 'maps/{}_current.html'
    '''

    coffee_df = common.load_coffee_df()
    if species not in coffee_df['scientificname'].unique():
        return 'Species does not exist'
    key = coffee_df[coffee_df['scientificname'] == species].iloc[0]['specieskey']
    coffee_df = coffee_df[coffee_df['specieskey'] == key]
    recommender_df = pd.read_csv('processed-data/recommender_df.csv', index_col = 0)
    total = recommender_df.shape[0]
    recommender_df = recommender_df[recommender_df['specieskey'] == key]
    max_occurrence = recommender_df['occurrence'].max()
    mean_occurrence = recommender_df['occurrence'].mean()
    m = folium.Map(location = [6, -27], zoom_start = 3)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    r = graphlab.load_model('recommendations/recommendation')
    r_df = r.recommend(users = [str(species)], k = total).to_dataframe()
    r_df['Latitude'] = r_df['latlon'].apply(lambda x: float(x.split()[0][:-1]))
    r_df['Longitude'] = r_df['latlon'].apply(lambda x: float(x.split()[1]))
    one = r_df[r_df['score'] - max_occurrence >= 0]
    two = r_df[r_df['score'] - mean_occurrence >= 0]
    for row in coffee_df.iterrows():
        marker = common.Marker(row, '#26c10b', 0.4)
        m.add_children(marker.create())
    for row in two.iterrows():
        marker = common.Marker(row, '#ffeda0', 0.4)
        m.add_children(marker.create())
    for row in one.iterrows():
        marker = common.Marker(row, '#f03b20', 1)
        m.add_children(marker.create())
    m.add_children(folium.LatLngPopup())
    m.save('recommendations/current/{}_current.html'.format(species))

if __name__ == '__main__':
    species = ['Coffea arabica L.',
 'Coffea liberica Hiern',
 'Coffea canephora Pierre ex A.Froehner',
 'Psilanthus mannii Hook.f.',
 'Coffea mayombensis A.Chev.',
 'Coffea pseudozanguebariae Bridson',
 'Coffea brevipes Hiern',
 'Coffea mufindiensis subsp. mufindiensis',
 'Coffea congensis A.Froehner',
 'Coffea mannii (Hook.f.) A.P.Davis',
 'Coffea resinosa (Hook.f.) Radlk.',
 'Coffea montekupensis Stoff.',
 'Coffea mangoroensis Port\xc3\xa8res',
 'Coffea humilis A.Chev.',
 'Coffea millotii J.-F.Leroy',
 'Coffea dewevrei De Wild. & T.Durand',
 'Coffea mongensis Bridson',
 'Coffea commersoniana (Baill.) A.Chev.',
 'Psilanthus lebrunianus (Germ. & Kesler) J.-F.Leroy ex Bridson',
 'Coffea humbertii J.-F.Leroy',
 'Coffea sessiliflora subsp. sessiliflora',
 'Coffea mufindiensis subsp. australis Bridson',
 'Coffea eugenioides S.Moore',
 'Coffea dubardii Jum.',
 'Coffea lulandoensis Bridson',
 'Psilanthus ebracteolatus Hiern',
 'Coffea sambavensis J.-F.Leroy ex A.P.Davis & Rakotonas.',
 'Coffea perrieri Drake ex Jum. & H.Perrier',
 'Coffea togoensis A.Chev.',
 'Coffea brassii (J.-F.Leroy) A.P.Davis',
 'Coffea richardii J.-F.Leroy',
 'Coffea zanguebariae Lour.',
 'Coffea ebracteolata (Hiern) Brenan',
 'Coffea mogenetii Dubard',
 'Coffea leroyi A.P.Davis',
 'Coffea fadenii Bridson',
 'Coffea pervilleana (Baill.) Drake',
 'Coffea coursiana J.-F.Leroy',
 'Coffea stenophylla G.Don',
 'Coffea magnistipula Stoff. & Robbr.',
 'Coffea tricalysioides J.-F.Leroy',
 'Coffea sakarahae J.-F.Leroy',
 'Coffea racemosa Lour.',
 'Coffea grevei Drake ex A.Chev.',
 'Coffea ankaranensis J.-F.Leroy ex A.P.Davis & Rakotonas.',
 'Coffea ratsimamangae J.-F.Leroy ex A.P.Davis & Rakotonas.',
 'Coffea homollei J.-F.Leroy',
 'Coffea boiviniana (Baill.) Drake',
 'Coffea buxifolia A.Chev.',
 'Coffea robusta L.Linden',
 'Coffea tsirananae J.-F.Leroy',
 'Coffea kimbozensis Bridson',
 'Coffea mcphersonii A.P.Davis & Rakotonas.',
 'Coffea mufindiensis subsp. lundaziensis Bridson',
 'Coffea pocsii Bridson',
 'Coffea leonimontana Stoff.',
 'Coffea tetragona Jum. & H.Perrier',
 'Coffea moratii J.-F.Leroy ex A.P.Davis & Rakotonas.',
 'Coffea rakotonasoloi A.P.Davis',
 'Coffea ambongensis J.-F.Leroy ex A.P.Davis & Rakotonas.',
 'Coffea liaudii J.-F.Leroy ex A.P.Davis',
 'Coffea abbayesii J.-F.Leroy',
 'Coffea bonnieri Dubard',
 'Coffea sessiliflora subsp. mwasumbii Bridson',
 'Coffea mufindiensis Hutch. ex Bridson',
 'Coffea lancifolia A.Chev.',
 'Coffea mapiana Sonk\xc3\xa9, Nguembou & A.P.Davis',
 'Coffea boinensis A.P.Davis & Rakotonas.',
 'Coffea vatovavyensis J.-F.Leroy',
 'Coffea kianjavatensis J.-F.Leroy',
 'Coffea kivuensis Lebrun',
 'Coffea montis-sacri A.P.Davis',
 'Coffea heimii J.-F.Leroy',
 'Coffea rhamnifolia (Chiov.) Bridson',
 'Coffea dactylifera Robbr. & Stoff.',
 'Coffea vianneyi J.-F.Leroy',
 'Coffea farafanganensis J.-F.Leroy',
 'Coffea grevei subsp. grevei',
 'Coffea kihansiensis A.P.Davis & Mvungi',
 'Coffea arenesiana J.-F.Leroy',
 'Psilanthus semsei Bridson',
 'Coffea costatifructa Bridson',
 'Coffea bertrandii A.Chev.',
 'Coffea schliebenii Bridson',
 'Coffea vohemarensis A.P.Davis & Rakotonas.',
 'Coffea salvatrix Swynn. & Philipson',
 'Coffea manombensis A.P.Davis',
 'Coffea sahafaryensis J.-F.Leroy',
 'Coffea bridsoniae A.P.Davis & Mvungi',
 'Coffea sessiliflora Bridson',
 'Coffea kapakata (A.Chev.) Bridson',
 'Coffea decaryana J.-F.Leroy',
 'Coffea mauritiana Lam.',
 'Psilanthus brassii (J.-F.Leroy) A.P.Davis',
 'Coffea littoralis A.P.Davis & Rakotonas.',
 'Coffea andrambovatensis J.-F.Leroy',
 'Coffea arabica Benth.',
 'Coffea bissetiae A.P.Davis & Rakotonas.',
 'Coffea bakossii Cheek & Bridson',
 'Coffea augagneurii Dubard',
 'Coffea humblotiana Baill.',
 'Coffea jumellei J.-F.Leroy',
 'Coffea labatii A.P.Davis & Rakotonas.',
 'Coffea anthonyi Stoff. & F.Anthony',
 'Coffea nkolbisonii Stoffelen',
 'Coffea melanocarpa Welw. ex Hiern',
 'Coffea minutiflora A.P.Davis & Rakotonas.',
 'Coffea grevei subsp. mahajangensis A.P.Davis & Rakotonas.',
 'Coffea pterocarpa A.P.Davis & Rakotonas.',
 'Coffea gallienii Dubard',
 'Coffea toshii A.P.Davis & Rakotonas.',
 'Coffea betamponensis Port\xc3\xa8res & J.-F.Leroy',
 'Coffea boiviniana subsp. drakei J.-F.Leroy',
 'Coffea ambanjensis J.-F.Leroy',
 'Coffea malayana Ridl.',
 'Coffea boiviniana (Baill.) A.Chev.',
 'Coffea fotsoana Stoff. & Sonk\xc3\xa9',
 'Coffea canephora Pierre',
 'Coffea vavateninensis J.-F.Leroy',
 'Coffea heterocalyx Stoff.',
 'Coffea namorokensis A.P.Davis & Rakotonas.',
 'Psilanthus merguensis (Ridl.) J.-F.Leroy',
 'Coffea zenkeri De Wild.',
 'Psilanthopsis kapakata A.Chev.',
 'Paracoffea lebruniana J.-F.Leroy',
 'Coffea klainii Pierre ex De Wild.',
 'Coffea brachyphylla Radlk.',
 'Coffea excelsa A.Chev.',
 'Coffea myrtifolia (A.Rich. ex DC.) J.-F.Leroy',
 'Coffea rosea Moc. & Sess\xc3\xa9 ex DC.',
 'Coffea boiviniana subsp. boiviniana',
 'Coffea canephora var. robusta (L. Linden) A. Chev.',
 'Coffea mufindiensis subsp. pawekiana (Bridson) Bridson',
 'Coffea laurentii De Wild.',
 'Coffea carissoi A. Rich.',
 'Coffea zenkeri De Wild. ex A.Chev.',
 'Coffea canephora var. hiernii Pierre',
 'Coffea antsingyensis J.-F.Leroy',
 'Psilanthus sapinii De Wild.',
 'Coffea kapakata Hort.',
 'Coffea staudtii A.Froehner',
 'Coffea wightiana Wall. ex Wight & Arn.',
 'Coffea pawekiana Bridson',
 'Coffea neoleroyi A.P.Davis',
 'Psilanthus melanocarpus (Welw. ex Hiern) J.-F.Leroy',
 'Coffea macrocarpa A.Rich.',
 'Psilanthus bengalensis (Roem. & Schultes) J.-F.Leroy',
 'Coffea liberica var. dewevrei (De Wild. & T.Durand) Lebrun',
 'Coffea rigida Miq.',
 'Coffea bengalensis Roxb.',
 'Coffea bonnieri subsp. androrangae J.-F.Leroy',
 'Coffea perrieri Drake',
 'Psilanthus travancorensis (Wight & Arn.) J.-F.Leroy',
 'Coffea uniflora K.Schum.',
 'Coffea liberica f. bwambensis Bridson',
 'Coffea benghalensis B.Heyne ex Schult.']
    for s in species:
        plot(s)
