import numpy as np
from scipy.spatial import ConvexHull
import pandas as pd

def calculate_convex_hull_volume(points):
    try:
        hull = ConvexHull(points)
        return hull.volume
    except Exception as e:
        #print(f"计算凸包体积时出错: {e}")
        return 0

def calculate_voxel_volume(points, voxel_size):
    xmin = np.floor(np.min(points[:, 0]))
    xmax = np.ceil(np.max(points[:, 0]))
    ymin = np.floor(np.min(points[:, 1]))
    ymax = np.ceil(np.max(points[:, 1]))
    zmin = np.floor(np.min(points[:, 2]))
    zmax = np.ceil(np.max(points[:, 2]))
    x_range = np.arange(xmin, xmax + voxel_size, voxel_size)
    y_range = np.arange(ymin, ymax + voxel_size, voxel_size)
    z_range = np.arange(zmin, zmax + voxel_size, voxel_size)
    X, Y, Z = np.meshgrid(x_range, y_range, z_range, indexing='ij')
    # Check if the shapes of X, Y, and Z are correct
    if X.shape != Y.shape or X.shape != Z.shape:
        raise ValueError("The shapes of X, Y, and Z are not compatible.")

    voxels = np.zeros(X.shape)
    for point in points:
            xi = int((point[0] - xmin) / voxel_size)
            yi = int((point[1] - ymin) / voxel_size)
            zi = int((point[2] - zmin) / voxel_size)
            if (0 <= xi < voxels.shape[0] and
                0 <= yi < voxels.shape[1] and
                0 <= zi < voxels.shape[2]):
                voxels[xi, yi, zi] = 1

    return np.sum(voxels) * voxel_size**3
def process_single_file(file_path, p, q):
    data = pd.read_csv(file_path).to_numpy()
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    upper_mask = z >= min(z)+(max(z)-min(z))*p
    lower_mask = z < min(z)+(max(z)-min(z))*p
    upper_points = np.column_stack((x[upper_mask], y[upper_mask], z[upper_mask]))
    lower_points = np.column_stack((x[lower_mask], y[lower_mask], z[lower_mask]))
    convex_hull_volume = 0
    if len(upper_points) > 0:
        convex_hull_volume = calculate_convex_hull_volume(upper_points)
    voxel_volume = 0
    if len(lower_points) > 0:
            voxel_volume = calculate_voxel_volume(lower_points, q)
    total_volume = convex_hull_volume + voxel_volume
    total_volume = round(total_volume, 2)
    return total_volume