import pandas as pd
import sys,os,time
import matplotlib.pyplot as plt
import geocoder
import folium
import requests
from opencage.geocoder import OpenCageGeocode

os.environ['GOOGLE_API_KEY'] = 'AIzaSyCwhaXDBEQhhmYKcm1ly_1wvC1edSWf3E8'

def crop_frequency():
    data = pd.read_csv('nevada_cropland.csv')
    crop = []

    for row in data.iterrows():
        i,row = row
        # c =[r.strip().lower() for r in (str(row['Production']) + str(row['Crops'])).split(',')]
        c =[r.strip().lower() for r in (str(row['Crops'])).split(',')]
        crop += pd.Series(c).unique().tolist()

    cropDict = {}
    for i in crop:
        if i not in cropDict.keys():
            cropDict[i] = 1
        cropDict[i] += 1

    dels = []
    for key, ele in cropDict.items():
        if ele<30:
            dels.append(key)
    for k in dels:
        cropDict.pop(k)

    plt.bar(cropDict.keys(), cropDict.values())
    plt.xticks(rotation = 90)
    plt.show()

def get_geocoder(zipcode):
    # initialize your variable to None
    apikey = 'AIzaSyCwhaXDBEQhhmYKcm1ly_1wvC1edSWf3E8'
    lat_lng_coords = None
    # loop until you get the coordinates
    while (lat_lng_coords is None):
        g = geocoder.google('Reno, NV', method = 'reverse')
        print(g)
        lat_lng_coords = g.latlng
    latitude = lat_lng_coords[0]
    longitude = lat_lng_coords[1]
    return latitude, longitude


def alt_geocoder(zipcode):
    key = '9097161f691548e6993a4769c3cef649'
    geocoder = OpenCageGeocode(key)
    result = geocoder.geocode(zipcode, no_annotations = '1')
    r = result[0]['geometry']
    lat, long = r['lat'] , r['lng']
    return lat, long


def forage_options():
    data = pd.read_csv('nevada_cropland.csv')
    master = pd.DataFrame()
    for row in data.iterrows():
        i, row = row
        if 'Forage' in row['Production'] or 'Bee' in row['Production']:
            master = master.append(row)
    zipDict = {}
    for zip in master['FarmAddZip']:
        if zip not in zipDict:
            zipDict[zip] = 1
        else:
            zipDict[zip] += 1

    master.to_csv('forage_bees_production.csv', index = False)
    sys.exit()
    plt.bar(zipDict.keys(), zipDict.values())
    plt.xticks(rotation = 60)
    plt.show()


def producer_map(crops = 'all'):
    baselayer = folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Satellite View',
        overlay = True,
        control = True)

    data = pd.read_csv('nevada_cropland.csv')
    if crops == 'all':
        crops = [c.strip().lower() for c in pd.Series(data['Crops'].apply(lambda x: str(x)).sum().split(',')).unique().tolist()]
    master = pd.DataFrame()
    if type(crops) != list:
        crops = [crops]
    for row in data.iterrows():
        i, row = row
        for crop in crops:
            if crop in str(row['Crops']).strip().lower() or crop in str(row['Production']).strip().lower():
                master = master.append(row)
                break

    if len(master) == 0:
        print(f'No growers for {crops} were found.')
        sys.exit()
    mmap = folium.Map(alt_geocoder('89503'), zoom_start = 20)
    baselayer.add_to(mmap)
    mmap.add_child(folium.LayerControl())

    for group in master.groupby('FarmAddZip'):
        zip, dat = group
        folium.Marker(alt_geocoder(zip), tooltip = dat.loc[dat.index[0], 'FarmAddCity'] + '<br>' + zip + '<br>' + str(len(dat)) + ' growers').add_to(mmap)
    filename = ''
    for c in crops:
        filename = filename + c +'_'
    mmap.save(f'grower_maps/{filename}nevada_growers.html')



def add_contacts():
    contacts = pd.read_csv('nevadagrown_master.csv')
    master = pd.read_csv('nevada_cropland.csv')

    contComps = contacts['company']
    masterComps = master['FarmName']

    count = 0
    for comp in contComps:
        if comp in masterComps:
            count += 1

    print(count)


add_contacts()