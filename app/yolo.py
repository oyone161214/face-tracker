import cv2
import sys
from ultralytics import YOLO

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
    print("以下の点を確認してください：")
    print("1. カメラが物理的に接続されているか")
    print("2. 'sudo raspi-config' で Legacy Camera が有効になっているか (純正カメラの場合)")
    sys.exit() # 強制終了

print(f"\n[成功] カメラ ID {found_id} を使用してYOLOを開始します。")
print("--------------------------------------------------")

# 2. YOLOの実行
# 見つかったID (found_id) を source に渡します
model = YOLO("yolo11n.pt")

try:
    # show=True で画面表示
    results = model.predict(source=found_id, show=True, conf=0.5)
except Exception as e:
    print("\n[YOLO実行エラー]")
    print(e)