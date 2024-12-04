import numpy as np
from scipy.spatial import ConvexHull
import pandas as pd


def process_single_file(file_path):
    # Read data
    data = pd.read_csv(file_path).to_numpy()
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    upper_mask = z > 0
    upper_points = np.column_stack((x[upper_mask], y[upper_mask], z[upper_mask]))
    hull = ConvexHull(upper_points)
    
    # Calculate and display convex hull volume
    convex_hull_volume = hull.volume
    return (round(convex_hull_volume,2))

