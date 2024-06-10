from trimesh.points import PointCloud

from plateau2minecraft.feature_color import colors

import random
import numpy as np


def assign(point_cloud: PointCloud, obj_path: str) -> PointCloud:
    # colors = np.array([(255, 0, 0) for _ in range(len(point_cloud.vertices))])
    # point_cloud.colors = colors
    list_obj = {
        ".//bldg:Building": (255, 0, 0),
        ".//bldg:WallSurface": (0, 255, 0),
        ".//bldg:RoofSurface": (0, 0, 255),
        ".//bldg:GroundSurface": (255, 255, 0),
        ".//bldg:OuterFloorSurface" : (255, 0, 255),
        ".//bldg:OuterCeilingSurface": (0, 255, 255),
        ".//bldg:ClosureSurface": (255, 255, 255),
        ".//bldg:BuildingInstallation": (0, 0, 0),
        ".//bldg:Window": (128, 128, 128),
        ".//bldg:Door" : (129, 129, 129),
    }
    colors = np.array([list_obj[obj_path] for _ in range(len(point_cloud.vertices))])
    point_cloud.colors = colors

    return point_cloud