import mediapipe as mp
import cv2
import math

from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

mp_hands = mp.solutions.hands

mp_draw = mp.solutions.drawing_utils

def distance_thumb_pinky(landmarks, image):

    thumb_tip = landmarks[4]
    pinky_tip = landmarks[20]

    thumb_tip_position = [thumb_tip.x, thumb_tip.y]
    pinky_tip_position = [pinky_tip.x, pinky_tip.y]

    distance = math.dist(thumb_tip_position, pinky_tip_position)

    print(distance)

    return distance, image 

def detection_context(dev_id = 0):

    cap = cv2.VideoCapture(dev_id)
    with mp_hands.Hands(max_num_hands = 5) as hands:
        while cap.isOpened():

            success, image = cap.read()

            if not success: 

                print("Ignoring empty camera frame")

                continue

            # To imporve performance, can mark the image as not writeable to pass by reference
            image.flags.writeable = False

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = hands.process(image)

            image.flags.writeable = True

            if results.multi_hand_landmarks:

                hand_index = 0

                for hand_landmarks in results.multi_hand_landmarks:

                    mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    distance, image = distance_thumb_pinky(hand_landmarks.landmark, image)

                    osc_process()
                    osc_msg = oscbuildparse.OSCMessage("/distance/hand" + str(hand_index), None, [distance])
                    osc_send(osc_msg, "localhost")

                    hand_index += 1

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.flip(image, 1)
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
