# GeoPackage Terrain Server

The GeoPackage Terrain Server is a FastAPI-based server designed to serve terrain tiles stored in GeoPackages. It provides a simple and efficient way to distribute and visualize terrain data in applications such as Cesium.JS.

## Requirements

- Python 3.x
- Dependencies (Install using `pip install -r requirements.txt`)

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/MapColonies/gpkg-terrain.git
   cd gpkg-terrain
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
### Running The Server

To run the GeoPackage Terrain Server, set the `GPKG_LIST` environment variable with a JSON array containing the GeoPackages you want to serve. Each GeoPackage should have an `id` and a `path`.

Example:
```bash
  GPKG_LIST='[{"id": "my-terrain", "path": "/path/to/my-terrain.gpkg" }]'\
  python3 -m uvicorn src.server:app
```
Replace /path/to/my-terrain.gpkg with the actual path to your GeoPackage.

The server will start on the default port (8000). You can customize the port by appending --port `<your-port>` to the uvicorn command.

Visit http://localhost:8000/docs in your browser to access the interactive API documentation and test the server.

### Integration with tiles-to-gpkg CLI

The GeoPackage Terrain Server is designed to work seamlessly with the [tiles-to-gpkg CLI](https://github.com/MapColonies/tiles-to-gpkg-cli), providing a powerful combination for handling and serving terrain tiles.

### How to Use with tiles-to-gpkg CLI

1. **Generate Terrain Tiles with Cesium Terrain Builder:**
   - Use the [Cesium Terrain Builder](https://github.com/geo-data/cesium-terrain-builder) or any other tool to generate QMESH tiles.

2. **Wrap QMESH Tiles with tiles-to-gpkg CLI:**
   - Use the [tiles-to-gpkg CLI](https://github.com/your-username/tiles-to-gpkg-cli) to wrap your QMESH tiles into a GeoPackage. For example:
     ```bash
     tilesToGpkg PATH_TO_DIR/terrain_new --watch_patterns "*.terrain" "layer.json" "foo.*"
     ```
    For more extensive usage examples and options, refer to the [tiles-to-gpkg CLI documentation](https://github.com/MapColonies/tiles-to-gpkg-cli).


## Helm Chart Deployment

If you prefer deploying the GeoPackage Terrain Server using Helm, follow these steps:

- **Build the Docker Image:**
   ```bash
   docker build -t gpkg-terrain .
   ```
- **Tag the Docker Image:**
  ```bash
  docker tag gpkg-terrain:latest your-docker-registry/gpkg-terrain:latest
  ```
  Replace your-docker-registry with the address of your Docker registry.

- **Upgrade Helm Chart with Custom Values:**
  ```bash
  docker push your-docker-registry/gpkg-terrain:latest
  ```
- **Upgrade Helm Chart with Custom Values:**
  Edit the Helm values file (values.yaml) to set the GPKG_LIST environment variable and any other configuration options.
  
  Example values.yaml:
  ```yaml
  ...
  image:
    repository: your-docker-registry/gpkg-terrain
    tag: latest
  ...
  
  env:
    gpkgList: '[{"id": "my-terrain", "path": "/data/my-terrain.gpkg" }]'
  ```

- **Upgrade with Helm:**
  ```bash
  helm upgrade --install geo-package-terrain-server ./helm -f values.yaml
  ```
**Access the Deployed GeoPackage Terrain Server:**

  Use Kubernetes port forwarding or expose the service as needed to access the deployed GeoPackage Terrain Server.
  
  Now your GeoPackage Terrain Server is deployed and configured using Helm with custom values in your Kubernetes cluster.
