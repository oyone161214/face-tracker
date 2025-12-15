import cv2
import mediapipe as mp



def find_and_open():

    cap = None
    
    for i in range(5):
        print(f"Attempting to open camera {i}...")

        current_cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
        
        if current_cap.isOpened():
            print(f"✅ Camera {i} opened successfully!")
            cap = current_cap
            break
        else:
            current_cap.release() 
    
    if cap is None:
        print("❌ No camera could be opened. Exiting.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)    

    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

    print("Starting face recognition... (Press 'q' to quit)")
    
    return cap,face_detection



def camera_mediapipe(cap, face_detection, debug=False):
    ret, frame = cap.read()
    if not ret: return None


    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)
    
    center = (frame.shape[1] // 2, frame.shape[0] // 2)
    move = None

    if results.detections:

        detection = results.detections[0] 
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = frame.shape
        

        x = int(bboxC.xmin * iw)
        y = int(bboxC.ymin * ih)
        w = int(bboxC.width * iw)
        h = int(bboxC.height * ih)
        
        face_center = (x + w // 2, y + h // 2)
        move = (center[0] - face_center[0], center[1] - face_center[1])

        if debug:
             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if debug:
        cv2.imshow('MediaPipe Face', frame)

    return move



def end_camera(cap):
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    print("Face recognition ended.")



if __name__ == '__main__':
    cap, cascade = find_and_open()
    
    if cap is not None:
        try:
            while True:
                resp = camera_mediapipe(cap, cascade)
                
                if resp is not None:
                    print(f"Moving: {resp}")
                else:
                    pass 

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            end_camera(cap)