import pandas as pd
import sys,os,time
import matplotlib.pyplot as plt
import geocoder
import folium
import requests
from opencage.geocoder import OpenCageGeocode
import ee


class ProducerMap:
    def __init__(crops = 'all', self):

    def add_ee_layer(mapObject, ee_image_object, vis_params, name):
        """Adds a method for displaying Earth Engine image tiles to folium map."""
        # layerFG = plugins.FeatureGroupSubGroup(self.layersGroup, name, overlay=True, show=False).add_to(mapObject)
        map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
        folium.raster_layers.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
            name=name,
            overlay=True,
            control=True
        ).add_to(mapObject)
        if 'palette' in vis_params.keys():
            colormap = branca.colormap.LinearColormap(colors=['#' + c for c in layerPalette[self.currLayer]])
            paletteLen = len(layerPalette[self.currLayer])
            colormap = colormap.to_step(index=np.arange(vis_params['min'], vis_params['max'] + .01,
                                                        step=(vis_params['max'] - vis_params['min']) / paletteLen))
            colormap.caption = name
            colormap.add_to(mapObject)

    def alt_geocoder(zipcode):
        key = '9097161f691548e6993a4769c3cef649'
        geocoder = OpenCageGeocode(key)
        result = geocoder.geocode(zipcode, no_annotations = '1')
        r = result[0]['geometry']
        lat, long = r['lat'] , r['lng']
        return lat, long


    def VI(mapObject, layers = ['NDVI', 'EVI'], date = '2017-01-01'):
        self.vegetation = ee.ImageCollection('MODIS/006/MOD13Q1')
        self.layers = layers if type(layers) == list else [layers]
        for lay in self.layers:
            self.currLayer = lay
            img = self.vegetation.select(lay).filterDate(date).first()
            vis_params = {
                'min': 0, 'max': 8000,
                'palette': layerPalette[lay]}
            self.add_ee_layer(mapObject, img, vis_params, lay)

    def producer_map(crops = 'all'):
        ee.Authenticate()
        ee.Initialize()

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

def alt_geocoder(zipcode):
    key = '9097161f691548e6993a4769c3cef649'
    geocoder = OpenCageGeocode(key)
    result = geocoder.geocode(zipcode, no_annotations = '1')
    r = result[0]['geometry']
    lat, long = r['lat'] , r['lng']
    return lat, long


data = pd.read_csv('nevadagrown_master.csv')
adds = data['address']

for add in adds:
    print(alt_geocoder(add))
