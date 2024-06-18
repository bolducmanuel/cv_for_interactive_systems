import mediapipe as mp 
import cv2

	

# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

mp_pose = mp.solutions.pose

mp_draw = mp.solutions.drawing_utils

def landmarks_to_keypoints(landmarks, definitions) :

    keypoints = dict()

    for j, landmark in enumerate(landmarks):
        x = float(landmark.x)
        y = float(landmark.y)
        part = definitions(j).name

        keypoints[part] = [x,y]

    return keypoints

def hand_height(data, image):

    first_hand = data[15]
    #second_hand = data[32:34]

    image = cv2.putText(image, 'hand height:' +  str(round(first_hand.y,2)), org = (50,125), fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale = 1, color = (255,255,255) , thickness = 2, lineType= cv2.LINE_AA)
 
    return image

def detection_context(dev_id=2):

    #load json parameters for detection
    #self.json_load(config)

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
            image = cv2.flip(image, 1)
            results = pose.process(image)

            # send osc messages 
            # osc_process()
            # osc_msg = oscbuildparse.OSCMessage("/hello", None, [0])
            # osc_send(osc_msg, "localhost")

            #osc_process()
            if results.pose_landmarks:

                mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                #image = hand_height(results.pose_landmarks.landmark, image) ##this is for the hand_height function

                keypoints = landmarks_to_keypoints(results.pose_landmarks.landmark, mp_pose.PoseLandmark)

                for keypoint in keypoints:
                    
                    osc_process()
                    osc_msg = oscbuildparse.OSCMessage("/keypoint/" + str(keypoint), None, keypoints[keypoint] )
                    osc_send(osc_msg, "localhost")

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imshow('frame', image)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        osc_terminate()

if __name__ == '__main__':

    osc_startup()
    osc_udp_client("127.0.0.1", 9000, "localhost")
    detection_context()
