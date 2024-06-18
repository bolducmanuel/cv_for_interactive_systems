import mediapipe as mp 
import cv2

mp_pose = mp.solutions.pose

mp_draw = mp.solutions.drawing_utils


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

            if results.pose_landmarks:

                mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.imshow('frame', image)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':

    detection_context()
