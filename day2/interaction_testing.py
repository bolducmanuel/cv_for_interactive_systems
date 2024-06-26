import mediapipe as mp 
import cv2

mp_pose = mp.solutions.pose

def hand_height(data, image):

    first_hand = data[15]
    #second_hand = data[32:34]

    image = cv2.putText(image, 'hand height:' +  str(round(first_hand.y,2)), org = (50,125), fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale = 1, color = (255,255,255) , thickness = 2, lineType= cv2.LINE_AA)
 
    return image

def detection_context(dev_id=0):

    cap = cv2.VideoCapture(dev_id)
    with mp_pose.Pose(smooth_landmarks=True) as pose:
        while cap.isOpened():

            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            results = pose.process(image)
            image = cv2.flip(image, 1)
            
            if results.pose_landmarks:

                image = hand_height(results.pose_landmarks.landmark, image) ##this is for the hand_height function


            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            cv2.imshow('frame', image)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        osc_terminate()

if __name__ == '__main__':

    detection_context()