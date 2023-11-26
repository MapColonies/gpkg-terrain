from fastapi import HTTPException
from osgeo import ogr
import json

TERRAIN_TILES_TABLE = 'terrain_tiles'
LAYER_JSON_TABLE = 'layer_json'

def queryLayerJsonFromGpkg(gpkgConnection: ogr.DataSource):
    if not gpkgConnection:
        raise HTTPException(status_code=500, detail="Couldn't connect to GPKG.")
    
    layer = gpkgConnection.GetLayer(LAYER_JSON_TABLE)

    if layer is None:
      raise HTTPException(status_code=500, detail="Something went wrong")

    # Only one layer should be in the table
    feature = layer.GetFeature((1))
    if feature:
        layerJsonData = feature.GetField("data")

        return json.loads(layerJsonData)
    else:
      raise HTTPException(status_code=404, detail="layer.json not found")

def queryTileFromGpkg(gpkgConnection, zoomLevel, tileColumn, tileRow):
    if not gpkgConnection:
        raise HTTPException(status_code=500, detail="Couldn't connect to GPKG.")
    
    layer = gpkgConnection.GetLayerByName(TERRAIN_TILES_TABLE)

    if layer is None:
        raise HTTPException(status_code=500, detail=f"Table {TERRAIN_TILES_TABLE} not found in GPKG")

    filterExpression = (
        f"zoom_level = {zoomLevel} AND tile_column = {tileColumn} AND tile_row = {tileRow}"
    )
    layer.SetAttributeFilter(filterExpression)

    feature = layer.GetNextFeature()

    if feature:
        tileData = feature.GetFieldAsBinary("tile_data")

        return tileData
    else:
      raise HTTPException(status_code=404, detail=f"Tile {zoomLevel}/{tileColumn}/{tileRow} not found.")
    