import argparse
import logging
from pathlib import Path

import trimesh

from plateau2minecraft.converter import Minecraft
from plateau2minecraft.impart_color import assign
from plateau2minecraft.merge_points import merge
from plateau2minecraft.parser import get_triangle_meshs
from plateau2minecraft.voxelizer import voxelize

import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def _extract_feature_type(file_path: str) -> str:
    return file_path.split("/")[-1].split("_")[1]


# ポイントをプロットする関数
def _make_plot(point_cloud: trimesh.points.PointCloud) -> None:
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # 点群をプロット
    ax.scatter(point_cloud.vertices[:,0],point_cloud.vertices[:,1],point_cloud.vertices[:,2],c=[( 0.0 , 0.0 , 0.0 , 1.0 )]) # 点の大きさ

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

_XPATH_LIST = {
    "bldg": [
        # ".//bldg:Building",
        ".//bldg:WallSurface",
        ".//bldg:RoofSurface",
        ".//bldg:GroundSurface",
        ".//bldg:OuterFloorSurface",
        ".//bldg:OuterCeilingSurface",
        ".//bldg:ClosureSurface",
        ".//bldg:BuildingInstallation",
        ".//bldg:Window",
        ".//bldg:Door",
    ],
    "tran": [".//tran:Road", ".//tran:TrafficArea"],
    "brid": [
        ".//brid:Bridge",
        ".//brid:BridgePart",
        ".//brid:RoofSurface",
        ".//brid:GroundSurface",
        ".//brid:WallSurface",
        ".//brid:ClosureSurface",
        ".//brid:OuterFloorSurface",
        ".//brid:OuterCeilingSurface",
        ".//brid:BridgeConstructionElement",
        ".//brid:OuterBridgeInstallation",
        ".//brid:Door",
        ".//brid:Window",
        ".//brid:IntBridgeInstallation",
        ".//brid:BridgeFurniture",
    ],
    "frn": [".//frn:CityFurniture"],
    "veg": [".//veg:PlantCover", ".//veg:SolitaryVegetationObject"],
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        required=True,
        type=Path,
        nargs="*",
        help="the output result encompasses the specified CityGML range",
    )
    parser.add_argument("--output", required=True, type=Path, help="output folder")
    args = parser.parse_args()

    point_cloud_list = []
    for file_path in args.target:
        logging.info(f"Processing start: {file_path}")
        feature_type = _extract_feature_type(str(file_path))

        for obj_path in _XPATH_LIST[feature_type]:
            logging.info(f"Object path: {obj_path}")


            logging.info(f"Triangulation: {obj_path}")
            triangle_mesh = get_triangle_meshs(file_path, obj_path)

            logging.info(f"Voxelize: {file_path}")
            # print(triangle_mesh.triangles)
            if len(triangle_mesh.triangles) == 0:
                continue
            point_cloud = voxelize(triangle_mesh)
            point_cloud = assign(point_cloud, obj_path)

            point_cloud_list.append(point_cloud)
            logging.info(f"Processing end: {file_path}")

    logging.info(f"Merging: {args.target}")
    merged = merge(point_cloud_list)

    logging.info(f"To : {args.target}")
    region = Minecraft(merged).build_region(args.output)
    # _make_plot(point_cloud)