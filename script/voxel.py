import numpy as np
import pandas as pd

def process_single_file(file_path, voxelsize):
    # Read data from file
    data = pd.read_csv(file_path).to_numpy()
    if len(data) > 0:
        voxel_size = voxelsize

        # Calculate voxel grid range
        xmin = np.floor(np.min(data[:, 0]))
        xmax = np.ceil(np.max(data[:, 0]))
        ymin = np.floor(np.min(data[:, 1]))
        ymax = np.ceil(np.max(data[:, 1]))
        zmin = np.floor(np.min(data[:, 2]))
        zmax = np.ceil(np.max(data[:, 2]))

        # Create voxel grid
        x_range = np.arange(xmin, xmax + voxel_size, voxel_size)
        y_range = np.arange(ymin, ymax + voxel_size, voxel_size)
        z_range = np.arange(zmin, zmax + voxel_size, voxel_size)
        X, Y, Z = np.meshgrid(x_range, y_range, z_range, indexing='ij')

        # Initialize voxel occupancy array
        voxels = np.zeros(X.shape)
        # Mark occupied voxels
        for point in data:
            xi = int((point[0] - xmin) / voxel_size)
            yi = int((point[1] - ymin) / voxel_size)
            zi = int((point[2] - zmin) / voxel_size)
            if (0 <= xi < voxels.shape[0] and 
                0 <= yi < voxels.shape[1] and 
                0 <= zi < voxels.shape[2]):
                voxels[xi, yi, zi] = 1

        # Calculate voxel volume
        voxel_volume = np.sum(voxels) * voxel_size**3
        # 保留两位小数
        voxel_volume = round(voxel_volume, 2)
        return(voxel_volume)

