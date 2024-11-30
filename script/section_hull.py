import numpy as np
from scipy.spatial import ConvexHull
import pandas as pd

def layer_point_cloud(points, layer_height):
    z_min = np.min(points[:, 2])
    z_max = np.max(points[:, 2])
    layers = []
    z_values = []
    z_not=[]
    for z in np.arange(z_min, z_max, layer_height):
        mask = (points[:, 2] >= z) & (points[:, 2] < z + layer_height)
        layer_points = points[mask]
        if len(layer_points) >= 4:
            layers.append(layer_points)
            z_values.append(z)
        else:
            z_not.append(z)
    return layers, z_values, z_not

#分层处理凸包多边形
def process_single_file(file_path,p):
    total_volume=[]
    data = pd.read_csv(file_path).to_numpy()
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    layers, _ ,z_not= layer_point_cloud(data, p)
    for i, points in enumerate(layers):
        if len(points) >= 4:
            hull = ConvexHull(points)
            total_volume.append(hull.volume)
    totalvolume=np.sum(total_volume)
    return totalvolume,z_not
    
    




  