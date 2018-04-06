# coding=utf-8
import sys
import thread
import time
import Leap
import HandGesture

# global variables
frame_counter = 0
last_object = "null"
nx_counter = 0

class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bones_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "initialized"

    def on_connect(self, controller):
        print "Motion Sensor Connected!"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        global frame_counter, last_object, nx_counter
        frame = controller.frame()
        for hand in frame.hands:
            returnValue = "null"
            if len(frame.hands) == 1:
                if hand.is_left:
                    returnValue = HandGesture.numberAnalysis(frame)
                    if returnValue != "s":
                        objectVerify = "number"
                    else:
                        objectVerify = "letter"  # Special case for letter S
                else:
                    returnValue = HandGesture.wordAnalysis(frame)
                    objectVerify = "letter"
            else:
                print "Two handed mode not available"

            # print returnValue
            # Validates object during a frame of time
            if last_object != returnValue:
                if returnValue != "null":

                    if nx_counter == 3:
                        returnValue = "ñ"
                        nx_counter = 0
                        print ("Your " + objectVerify + " is: " + returnValue)  # Doubtful method of detecting ñ
                    elif returnValue == "n" and last_object == "x":
                        nx_counter += 1
                    else:
                        print returnValue

                last_object = returnValue
                frame_counter = 0

            elif last_object != "null":
                frame_counter += 1
                if frame_counter == 180:
                    print ("Your " + objectVerify + " is: " + returnValue)

        # Test code
        """
            print "Frame ID = " + str(frame.id) \
                  + " Timestamp: " + str(frame.timestamp) \
                  + " # of Hands: " + str(len(frame.hands)) \
                  + " # of Fingers: " + str(len(frame.fingers)) \
                  + " # of Tools: " + str(len(frame.tools)) \
                  + " # of Gestures: " + str(len(frame.gestures()))

            for hand in frame.hands:
                handType = "Left Hand" if hand.is_left else "Right Hand"

                print handType + " Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)

                normal = hand.palm_normal
                direction = hand.direction

                print "Pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) + " Roll: " + str(normal.roll * Leap.RAD_TO_DEG) \
                      + " Yaw: " + str(direction.yaw * Leap.RAD_TO_DEG)

                for finger in hand.fingers:
                    print "Type: " + self.finger_names[finger.type] + " ID: " + str(finger.id) \
                          + " Direction: " + str(finger.direction) + " Is extended: " + str(finger.is_extended)

                    for b in range(0, 4):
                        bone = finger.bone(b)
                        print "Bone: " + self.bones_names[bone.type] + " Start: " + str(bone.prev_joint) \
                              + " End: " + str(bone.next_joint) + " Direction: " + str(bone.direction)
        
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)
        
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2:
                        clockwiseness = "clockwise"
                    else:
                        clockwiseness = "counter-clockwise"
        
                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
        
                    print "ID: " + str(circle.id) + " Progress: " + str(circle.progress) \
                          + " Radius (mm): " + str(circle.radius) + " Swept Angle: " + str(swept_angle * Leap.RAD_TO_DEG) \
                          + " " + clockwiseness
        
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    print "ID: " + str(swipe.id) + " State: " + self.state_names[gesture.state] \
                          + " Position: " + str(swipe.position) + " Direction: " + str(swipe.direction) \
                          + " Speed (mm/s): " + str(swipe.speed)"""


def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print "Press enter to quit"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
    # TODO: validate number or letter after a few seconds (maybe 2 seconds or so)
