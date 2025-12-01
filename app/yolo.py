import cv2
import sys
from ultralytics import YOLO

# --------------------------------------------------
# カメラ探しの関数
# --------------------------------------------------
def search_available_camera():
    for camera_id in range(10):
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                cap.release()
                return camera_id
        cap.release()
    return None

# ==========================================
# メイン処理
# ==========================================

# 1. カメラを探す
found_id = search_available_camera()
if found_id is None:
    print("カメラが見つかりません")
    sys.exit()

print(f"カメラID {found_id} で開始します。")
print("終了するには、ターミナルで [Ctrl] + [C] を押してください。")

# 2. モデル読み込み（顔専用）
model = YOLO("yolov8n-face.pt")

try:
    # 3. リアルタイム推論の実行
    # stream=True にすると、forループで次々と結果を取り出せるようになります
    results = model.predict(source=found_id, show=True, conf=0.5, classes=[0], stream=True)

    # ずっとループし続けます
    for result in results:
        
        # 検出された「箱」があれば処理
        if result.boxes:
            for box in result.boxes:
                # 座標を取得 (x1, y1, x2, y2)
                coords = box.xyxy[0].tolist()
                x1, y1, x2, y2 = map(int, coords)
                
                # 中心の座標を計算
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                
                # 画面サイズ（参考：標準的なWebカメラは 横640, 縦480）
                # printでログを流しすぎると重くなるので、見やすく整形します
                print(f"顔検出: 中心({center_x:3d}, {center_y:3d}) | 範囲[{x1},{y1} ~ {x2},{y2}]")
                
                # ★ここに「もし中心が右すぎたら、右を向け」などの命令を書くことができます
        
        else:
            # 何も映っていない時
            print("...", end="\r") # 改行せずに待機表示

except KeyboardInterrupt:
    print("\n終了します")
    sys.exit()
    
except Exception as e:
    print(f"\nエラー: {e}")