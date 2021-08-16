import fiona
import pandas as pd


def get_data(df, name):
    polyDf = df[df['Name'] == name]
    # get list of points
    xyList = []
    rowName = ''
    for _, row in polyDf.iterrows():
        xyList.append((row.X, row.Y))
        rowName = row.Name
    return xyList, rowName


def build_rowdict(xyList, rowName):
    # save record and close shapefile
    rowDict = {
        'geometry': {
            'type': 'Polygon',
            'coordinates': [xyList]
        },  # Here the xyList is in brackets
        'properties': {'Name': rowName},
    }
    return rowDict


polyDf = pd.read_csv('./multi_polygon_system/multi_polygon.csv', header=0)

# define schema
schema = {
    'geometry': 'Polygon',
    'properties': [('Name', 'str')]
}

# open a fiona object
polyShp = fiona.open('./multi_polygon_system/multi_polygon.shp', mode='w', driver='ESRI Shapefile',
                     schema=schema, crs="EPSG:4326")


for shapes in ['Border1', 'Border2']:
    xyList, rowName = get_data(polyDf, shapes)
    rowDict = build_rowdict(xyList, rowName)
    polyShp.write(rowDict)

# close fiona object
polyShp.close()
