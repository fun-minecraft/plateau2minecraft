import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 点の数を指定
num_points = 1000

# 点群の範囲を設定 (この例では、[-1, 1] の立方体内にランダムな点を生成)
min_coords = np.array([-1, -1, -1])
max_coords = np.array([1, 1, 1])

# ランダムな点の座標を生成
points = np.random.rand(num_points, 3) * (max_coords - min_coords) + min_coords

# matplotlibで3D点群を表示
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Point Cloud')
plt.show()