from typing import Dict
from src.utils.gpkgs_query_utils import queryLayerJsonFromGpkg, queryTileFromGpkg
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, HTTPException
from osgeo import ogr
import sys, os, json, logging
from src.utils.OGRConnectionPool import OGRConnectionPool

MAX_CONNECTIONS_IN_POOL = 10

logger = logging.getLogger(__name__)

connectionPools = {}

def createConnectionPoolsDict(gpkgsList) -> Dict[str, OGRConnectionPool]:
    connectionPools = {}

    for gpkg in gpkgsList:
        pool = OGRConnectionPool(MAX_CONNECTIONS_IN_POOL, gpkg.get("path"))
        connectionPools[gpkg.get("id")] = pool
    
    return connectionPools


@asynccontextmanager
async def lifespan(app: FastAPI):
    global connectionPools
    # On Load
    ogr.RegisterAll()
    
    # [{id, path}...]
    gpkgsListStr = os.environ.get('GPKG_LIST')
    gpkgsList = json.loads(gpkgsListStr) if gpkgsListStr is not None else None

    if gpkgsList is None:
        error_message = 'GPKG_LIST env is not defined.'
        logger.error(error_message)
        raise EnvironmentError(error_message)
    try:
        # Init Connections To GPKG(s)
        connectionPools = createConnectionPoolsDict(gpkgsList)
    except FileNotFoundError as e:
        logger.error(f"Error creating connection pools: {e}")
        
    yield
    if connectionPools is not None: 
        # Clean up
        for connectionPool in list(connectionPools.values()):
            connectionPool.close_all_connections()

app = FastAPI(lifespan=lifespan)

@app.get('/{gpkgId}/layer.json')
async def getTerrainTile(gpkgId: str):
    connectionPool = connectionPools.get(gpkgId)
    gpkgConnection = connectionPool.get_connection()
    layerJsonData = queryLayerJsonFromGpkg(gpkgConnection)

    connectionPool.release_connection(gpkgConnection)
    return layerJsonData

@app.get('/{gpkgId}/{zoomLevel}/{tileColumn}/{tileRow}.terrain')
async def getTerrainTile(gpkgId: str, zoomLevel: int, tileColumn: int, tileRow: int, res: Response):
    connectionPool = connectionPools.get(gpkgId)
    if connectionPool is None:
        raise HTTPException(status_code=404, detail=f"GPKG {gpkgId} not found.")
    
    gpkgConnection = connectionPool.get_connection()
    
    tileData = queryTileFromGpkg(gpkgConnection, zoomLevel, tileColumn, tileRow)
    connectionPool.release_connection(gpkgConnection)
    return Response(content=tileData, media_type="application/octet-stream", headers={"Content-Encoding": "gzip"})