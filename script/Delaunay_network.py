import numpy as np
from scipy.spatial import Delaunay
from multiprocessing import Pool
import pandas as pd

def project_to_2d(points):
    return points[:, :2]

def layer_point_cloud(points, layer_height):
    """Divide the point cloud into horizontal layers."""
    z_min = np.min(points[:, 2])
    z_max = np.max(points[:, 2])
    layers = []
    z_values = []
    for z in np.arange(z_min, z_max, layer_height):
        mask = (points[:, 2] >= z) & (points[:, 2] < z + layer_height)
        layer_points = points[mask]
        if len(layer_points) >= 3:
            layers.append(layer_points)
            z_values.append(z)
    return layers, z_values

def calculate_triangle_area(triangle_points):
    p1, p2, p3 = triangle_points
    return 0.5 * np.abs(np.cross(p2 - p1, p3 - p1))

def process_layer(points, max_edge_length):
    if len(points) < 3:
        return 0, None
    else:
      points_2d = project_to_2d(points)

    
      tri = Delaunay(points_2d)
      valid_triangles = []
      total_area = 0
      for simplex in tri.simplices:
            triangle_points = points_2d[list(simplex)]
            edges = [np.linalg.norm(triangle_points[i] - triangle_points[j])
                     for i in range(3) for j in range(i + 1, 3)]
            if all(edge <= max_edge_length for edge in edges):
                area = calculate_triangle_area(triangle_points)
                total_area += area
                valid_triangles.append(simplex)

    return total_area, (tri, valid_triangles)


def process_layer_parallel(args):
    points, max_edge_length = args
    return process_layer(points, max_edge_length)

def process_single_file(file_path, layer_height, max_edge_length):
    data = pd.read_csv(file_path).to_numpy()
    points = data[:, 0:3]
    # Assuming 'points' is your numpy array of points
    jitter_amount = 1e-6
    jitter = np.random.uniform(-jitter_amount, jitter_amount, size=points.shape)
    points=points+jitter
    layers, z_values = layer_point_cloud(points, layer_height)
    total_volume = 0
    triangulations = []

    with Pool() as pool:
        results = pool.map(process_layer_parallel, [(layer, max_edge_length) for layer in layers])
        for i, (layer_area, triangulation) in enumerate(results):
            layer_volume = layer_area * layer_height
            total_volume += layer_volume
            triangulations.append(triangulation)

    return(round(total_volume, 2))

