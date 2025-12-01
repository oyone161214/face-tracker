import cv2
import sys
from ultralytics import YOLO

# ---------------------------------------------------------
# カメラ設定
# 画像では 1 になっていましたが、まずは標準の 0 で試すのがおすすめです
# 0 でダメな場合はここを 1 に変更してください
CAMERA_ID = 0
# ---------------------------------------------------------

print(f"--- カメラ ID {CAMERA_ID} の接続テストを開始します ---")

# 1. OpenCVを使ってカメラが開けるか単独チェック
cap = cv2.VideoCapture(CAMERA_ID)

if not cap.isOpened():
    print(f"[エラー] カメラ ID {CAMERA_ID} を開けませんでした。")
    print("対処法: CAMERA_ID を 0 や 1 に変更するか、カメラの接続を確認してください。")
    sys.exit() # 強制終了

ret, frame = cap.read()
if not ret:
    print(f"[エラー] カメラには接続できましたが、映像データが取得できません。")
    print("対処法: 他のアプリがカメラを使っていないか確認してください。")
    cap.release()
    sys.exit() # 強制終了

# チェック成功ならカメラを解放（YOLOが使うため）
cap.release()
print(f"[成功] カメラ ID {CAMERA_ID} の動作を確認しました。YOLOを開始します。")
print("--------------------------------------------------")

# 2. YOLOの実行
# sourceには上で設定した CAMERA_ID を使います
model = YOLO("yolo11n.pt")
results = model.predict(source=CAMERA_ID, show=True, conf=0.5)