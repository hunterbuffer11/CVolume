import numpy as np
from scipy.spatial import ConvexHull
import pandas as pd


def process_single_file(file_path):
    """
    Process a single CSV file to compute and visualize the convex hull of a 3D point cloud.
    
    Parameters:
    file_path (str): The path to the CSV file containing the 3D point cloud data.
    """
    # Read data
    data = pd.read_csv(file_path).to_numpy()
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    upper_mask = z > 0
    upper_points = np.column_stack((x[upper_mask], y[upper_mask], z[upper_mask]))
    # Create 3D plot
   # fig = plt.figure(figsize=(10, 8))
    #ax = fig.add_subplot(111, projection='3d')
    hull = ConvexHull(upper_points)
    """
    for simplex in hull.simplices:
        vertices = upper_points[simplex]
        poly = Poly3DCollection([vertices])
        poly.set_facecolor('yellow')
        poly.set_alpha(1.0)
        poly.set_edgecolor('black')
        ax.add_collection3d(poly)
    """
    # Calculate and display convex hull volume
    convex_hull_volume = hull.volume
    return (round(convex_hull_volume,2))
    """
    column=["Volume"]
    test=pd.DataFrame(columns=column,data=[convex_hull_volume])
    test.to_csv('test_convex.csv')
    """
    #上述代码可以把输出结果放到csv文件里去
    """
    # Set plot limits and properties
    ax.set_xlim([np.min(x), np.max(x)])
    ax.set_ylim([np.min(y), np.max(y)])
    ax.set_zlim([np.min(z), np.max(z)])
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Point Cloud Convex Hull')
    ax.grid(False)
    ax.view_init(elev=30, azim=45)
    plt.tight_layout()
    #plt.show()
"""

