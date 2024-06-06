import argparse
import logging
from pathlib import Path

from plateau2minecraft.converter import Minecraft
from plateau2minecraft.impart_color import assign
from plateau2minecraft.merge_points import merge
from plateau2minecraft.parser import get_triangle_meshs
from plateau2minecraft.voxelizer import voxelize

# ログの基本設定を行います。ログレベルはINFOで、出力フォーマットを指定します。
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ファイルパスから特徴タイプを抽出する関数
def _extract_feature_type(file_path: str) -> str:
    return file_path.split("/")[-1].split("_")[1]

# メイン処理
if __name__ == "__main__":
    # コマンドライン引数のパーサーを作成
    parser = argparse.ArgumentParser()
    
    # --target引数を追加（必須）
    parser.add_argument(
        "--target",
        required=True,
        type=Path,
        nargs="*",
        help="指定されたCityGML範囲を含む出力結果",
    )
    
    # --output引数を追加（必須）
    parser.add_argument("--output", required=True, type=Path, help="出力フォルダ")
    
    # 引数を解析
    args = parser.parse_args()

    # ポイントクラウドリストの初期化
    point_cloud_list = []
    
    # 各ターゲットファイルに対して処理を実行
    for file_path in args.target:
        logging.info(f"処理開始: {file_path}")
        feature_type = _extract_feature_type(str(file_path))

        logging.info(f"三角形分割: {file_path}")
        triangle_mesh = get_triangle_meshs(file_path, feature_type)

        logging.info(f"ボクセル化: {file_path}")
        point_cloud = voxelize(triangle_mesh)
        point_cloud = assign(point_cloud, feature_type)

        # ポイントクラウドリストに追加
        point_cloud_list.append(point_cloud)
        logging.info(f"処理終了: {file_path}")

    # ポイントクラウドのマージ
    logging.info(f"マージ中: {args.target}")
    merged = merge(point_cloud_list)

    # マインクラフトリージョンの作成
    logging.info(f"出力先: {args.target}")
    region = Minecraft(merged).build_region(args.output)
