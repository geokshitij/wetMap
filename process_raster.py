import rasterio
import numpy as np
import csv
import sys

def get_geocoords(row, col, affine_transform):
    return affine_transform * (col, row)

def process_raster(state):
    raster_file_path = f'/scratch/kdahal3/wetland/{state}_wetlands_raster.tif'
    csv_file_path = f"/scratch/kdahal3/wetland/{state}_sampled_coords.csv"

    sampled_wetland_coords = []
    sampled_non_wetland_coords = []

    with rasterio.open(raster_file_path) as src:
        window_size = 10000

        for ji, window in src.block_windows(1):
            raster_data = src.read(1, window=window)
            wetland_pixels = np.where(raster_data == 1)
            non_wetland_pixels = np.where(raster_data == 2)

            sampled_wetland_indices = np.random.choice(len(wetland_pixels[0]), min(5, len(wetland_pixels[0])), replace=False)
            sampled_non_wetland_indices = np.random.choice(len(non_wetland_pixels[0]), min(5, len(non_wetland_pixels[0])), replace=False)

            for i in sampled_wetland_indices:
                coord = (wetland_pixels[1][i] + window.col_off, wetland_pixels[0][i] + window.row_off)
                sampled_wetland_coords.append(coord)

            for i in sampled_non_wetland_indices:
                coord = (non_wetland_pixels[1][i] + window.col_off, non_wetland_pixels[0][i] + window.row_off)
                sampled_non_wetland_coords.append(coord)

    with open(csv_file_path, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Longitude", "Latitude"])

        for coord in sampled_wetland_coords:
            geo_coord = get_geocoords(coord[1], coord[0], src.transform)
            writer.writerow(["Wetland", geo_coord[0], geo_coord[1]])

        for coord in sampled_non_wetland_coords:
            geo_coord = get_geocoords(coord[1], coord[0], src.transform)
            writer.writerow(["Non-Wetland", geo_coord[0], geo_coord[1]])

    print(f"Sampled coordinates for {state} saved to {csv_file_path}")

if __name__ == "__main__":
    state = sys.argv[1]
    process_raster(state)
