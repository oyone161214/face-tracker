import cv2
import sys
from ultralytics import YOLO

# --------------------------------------------------
# カメラ探しの関数 (変更なし)
# --------------------------------------------------
def search_available_camera():
    """
    0番から9番まで順番にカメラをチェックし、
    最初に使えるようになったカメラのIDを返します。
    """
    print("--- 接続可能なカメラを検索中 ---")
    
    # 0番から9番までスキャンしてみる
    for camera_id in range(10):
        print(f"ID {camera_id} をチェック中...", end=" ")
        
        # カメラを開く試行
        # (ラズパイでUSBカメラが不安定な場合、次の行を試してください)
        # cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2) 
        cap = cv2.VideoCapture(camera_id)
        
        if cap.isOpened():
            # 開けたとしても、実際に画像が読めるか確認（重要）
            ret, frame = cap.read()
            if ret:
                print("-> OK! (接続成功)")
                cap.release() # YOLOで使うために一旦閉じる
                return camera_id
            else:
                print("-> NG (開けましたが映像が取れません)")
        else:
            print("-> NG (接続できません)")
        
        # 念のため閉じて次へ
        if cap.isOpened():
            cap.release()
            
    return None # どのカメラも見つからなかった場合

# ==========================================
# メイン処理
# ==========================================

# 1. 使えるカメラを自動で探す
found_id = search_available_camera()

if found_id is None:
    print("\n[エラー] 使用可能なカメラが1つも見つかりませんでした。")
    sys.exit() # 強制終了

print(f"\n[成功] カメラ ID {found_id} を使用して顔認識を開始します。")
print("--------------------------------------------------")
print("初回実行時は顔認識用モデル(yolov8n-face.pt)のダウンロードが始まります...")

# 2. YOLOの実行
# 【変更点1】 モデルを「一般物体用」から「顔認識専用」に変更します
# yolov8n-face.pt は、YOLOv8ベースの軽量な顔認識モデルです。
model = YOLO("yolov8n-face.pt")

try:
    # show=True で画面表示
    # 【変更点2 (任意)】 classes=[0] を追加して、念の為クラスID 0（顔）のみに限定します
    # (このモデルは顔しか知らないのでなくても動きますが、明示的に指定すると確実です)
    results = model.predict(source=found_id, show=True, conf=0.5, classes=[0])
except Exception as e:
    print("\n[YOLO実行エラー]")
    print(e)