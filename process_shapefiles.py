# import geopandas as gpd
# import rasterio
# from rasterio.features import rasterize
# from rasterio.transform import from_origin
# import sys

# def process_shapefile(state):
#     shapefile_path = f'/scratch/kdahal3/wetland/{state}_shapefile_wetlands/{state}_Wetlands.shp'
#     try:
#         gdf = gpd.read_file(shapefile_path)
#     except Exception as e:
#         print(f"Error reading shapefile for {state}: {e}")
#         return

#     bounds = gdf.total_bounds
#     cell_size = 10
#     num_col = int((bounds[2] - bounds[0]) / cell_size)
#     num_row = int((bounds[3] - bounds[1]) / cell_size)
#     transform = from_origin(bounds[0], bounds[3], cell_size, cell_size)

#     def burn_shapes(shapes, value):
#         return rasterize(shapes, out_shape=(num_row, num_col), fill=2, default_value=value, transform=transform)

#     rasterized = burn_shapes(gdf.geometry, 1)

#     output_raster = f'{state}_wetlands_raster.tif'
#     with rasterio.open(
#         output_raster,
#         'w',
#         driver='GTiff',
#         height=rasterized.shape[0],
#         width=rasterized.shape[1],
#         count=1,
#         dtype=rasterized.dtype,
#         crs=gdf.crs,
#         transform=transform,
#     ) as dst:
#         dst.write(rasterized, 1)

#     print(f'Rasterized {state} shapefile.')

# if __name__ == "__main__":
#     state = sys.argv[1]
#     process_shapefile(state)


import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin
import sys
import os
import pandas as pd

def process_shapefile(state):
    directory = f'/scratch/kdahal3/wetland/{state}_shapefile_wetlands/'

    # Include regional keywords and the state name itself
    include_keywords = ["West", "East", "North", "South", state]
    exclude_keywords = ["Historic", "Metadata", "Riparian"]

    shapefiles = [os.path.join(directory, f) for f in os.listdir(directory) 
                  if f.endswith('.shp') and 
                     any(kw in f for kw in include_keywords) and 
                     not any(kw in f for kw in exclude_keywords)]

    # Read and merge shapefiles
    gdf_list = [gpd.read_file(shp) for shp in shapefiles]
    gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))

    # Continue with the existing rasterization process
    bounds = gdf.total_bounds
    cell_size = 10
    num_col = int((bounds[2] - bounds[0]) / cell_size)
    num_row = int((bounds[3] - bounds[1]) / cell_size)
    transform = from_origin(bounds[0], bounds[3], cell_size, cell_size)

    def burn_shapes(shapes, value):
        return rasterize(shapes, out_shape=(num_row, num_col), fill=2, default_value=value, transform=transform)

    rasterized = burn_shapes(gdf.geometry, 1)

    output_raster = f'{state}_wetlands_raster.tif'
    with rasterio.open(
        output_raster,
        'w',
        driver='GTiff',
        height=rasterized.shape[0],
        width=rasterized.shape[1],
        count=1,
        dtype=rasterized.dtype,
        crs=gdf.crs,
        transform=transform,
    ) as dst:
        dst.write(rasterized, 1)

    print(f'Rasterized {state} shapefile.')

if __name__ == "__main__":
    state = sys.argv[1]
    process_shapefile(state)
