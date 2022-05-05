import mediapipe as mp
import cv2
import time

cap = cv2.VideoCapture(0)
ptime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec((255, 0, 0), thickness=1, circle_radius=2)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for face_lms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, face_lms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f"FPS-{int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)