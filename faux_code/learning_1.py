import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: no video capture")
    exit()

while (True):
    ret, frame = cap.read()
    if not ret:
        print("No more stream")
        break

    cv2.imshow("Webcam!", frame)
    # press q to quit
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()