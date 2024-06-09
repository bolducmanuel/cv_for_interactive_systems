import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():

    success, image = cap.read()

    if not success: 
        print("ignoring empty camera frame.")

        continue

    cv2.imshow('frame', image)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

