import mediapipe as mp 
import cv2
import math 


mp_pose = mp.solutions.pose

mp_draw = mp.solutions.drawing_utils

def right_hand_detector(results):

    right_hand_position = results[16]

    y_data = right_hand_position.y

    if y_data < 0.5:
        print("hello")

    else : 
        print("bye")

    return y_data

def distance_between_hands(results):

    right_hand_position = results[16]

    left_hand_position = results[15]

    point1 = [right_hand_position.x, right_hand_position.y]
    point2 = [left_hand_position.x, left_hand_position.y]

    distance = math.dist(point1, point2)

    print(distance)

    return distance

def distance_from_camera(results):

    left_hip_position = results[23]
    right_hip_position = results[24]

    left_hip_point = [left_hip_position.x, left_hip_position.y]
    right_hip_point = [right_hip_position.x, right_hip_position.y]

    distance = math.dist(left_hip_point, right_hip_point)
    
    if distance < 0.1 : 

        print("come closer to me!")

    if distance > 0.15: 

        print("not that close!!")

    return distance

def distance_from_camera2(results, image):

    left_hip_position = results[23]
    right_hip_position = results[24]

    left_hip_point = [left_hip_position.x, left_hip_position.y]
    right_hip_point = [right_hip_position.x, right_hip_position.y]

    distance = math.dist(left_hip_point, right_hip_point)
    
    if distance < 0.1 : 

        image = cv2.putText(image, "come closer to me!", org = (50,125), fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale = 1, color = (255,255,255) , thickness = 2, lineType= cv2.LINE_AA)

    if distance > 0.15: 

         image = cv2.putText(image, "not that close!!", org = (50,125), fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
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

            if results.pose_landmarks:

                mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                image = cv2.flip(image, 1)

                #distance_between_hands(results.pose_landmarks.landmark)
                #right_hand_detector(results.pose_landmarks.landmark)
                #image = distance_from_camera2(results.pose_landmarks.landmark, image)

            else:
                image = cv2.flip(image, 1)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            cv2.imshow('frame', image)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':

    detection_context()