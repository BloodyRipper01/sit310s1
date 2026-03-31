#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped
from duckietown_msgs.msg import FSMState


class Drive_Square:
    def __init__(self):
        # Initialize global class variables
        self.cmd_msg = Twist2DStamped()
        self.is_moving = False   # prevents multiple triggers

        # Initialize ROS node
        rospy.init_node('drive_square_node', anonymous=True)

        # ✅ Updated with your Duckiebot name
        self.pub = rospy.Publisher('/mybota002437/car_cmd_switch_node/cmd', Twist2DStamped, queue_size=1)
        rospy.Subscriber('/mybota002437/fsm_node/mode', FSMState, self.fsm_callback, queue_size=1)

    # robot only moves when lane following is selected on the duckiebot joystick app
    def fsm_callback(self, msg):
        rospy.loginfo("State: %s", msg.state)

        if msg.state == "NORMAL_JOYSTICK_CONTROL":
            self.is_moving = False
            self.stop_robot()

        elif msg.state == "LANE_FOLLOWING":
            if not self.is_moving:
                rospy.sleep(1)  # wait for system to stabilize
                self.move_robot()

    # Sends zero velocities to stop the robot
    def stop_robot(self):
        self.cmd_msg.header.stamp = rospy.Time.now()
        self.cmd_msg.v = 0.0
        self.cmd_msg.omega = 0.0
        self.pub.publish(self.cmd_msg)

    # Keep node alive
    def run(self):
        rospy.spin()

    # Helper function to publish movement commands
    def publish_cmd(self, v, omega):
        self.cmd_msg.header.stamp = rospy.Time.now()
        self.cmd_msg.v = v
        self.cmd_msg.omega = omega
        self.pub.publish(self.cmd_msg)

    # Robot drives in a square and then stops
    def move_robot(self):
        self.is_moving = True

        # 🔧 You will tune these values on your robot
        forward_speed = 0.3
        forward_time = 3.5     # adjust for ~1 meter

        turn_speed = 4.0
        turn_time = 1.0        # adjust for ~90 degrees

        stop_time = 0.5

        rospy.loginfo("Starting square motion")

        for i in range(4):
            rospy.loginfo("Side %d: Moving forward", i + 1)
            self.publish_cmd(forward_speed, 0.0)
            rospy.sleep(forward_time)

            rospy.loginfo("Stopping")
            self.stop_robot()
            rospy.sleep(stop_time)

            # Skip turning after last side
            if i < 3:
                rospy.loginfo("Turn %d: Rotating", i + 1)
                self.publish_cmd(0.0, turn_speed)
                rospy.sleep(turn_time)

                rospy.loginfo("Stopping after turn")
                self.stop_robot()
                rospy.sleep(stop_time)

        rospy.loginfo("Square complete")
        self.stop_robot()
        self.is_moving = False


if __name__ == '__main__':
    try:
        duckiebot_movement = Drive_Square()
        duckiebot_movement.run()
    except rospy.ROSInterruptException:
        pass
