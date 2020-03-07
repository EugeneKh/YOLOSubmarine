import cv2
import os
import time as t

dataset_path = "in"
#sign_name = "circle"
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)

    if k == ord('s'):
        #f_path = os.sep.join([dataset_path, sign_name])
        f_path = os.path.abspath(dataset_path)
        os.makedirs(f_path, exist_ok=True)
        uniq = str(t.time()).replace(".", "")
        #f_name = os.sep.join([f_path, f"{sign_name}{uniq}.png"])
        f_name = os.sep.join([f_path, f"{uniq}.png"])

        cv2.imwrite(f_name, frame)
        print(f_name)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
