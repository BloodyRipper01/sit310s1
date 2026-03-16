#!/usr/bin/env python3

# Import Dependencies
import rospy 
from geometry_msgs.msg import Twist 

def move_turtle_square(): 
    rospy.init_node('turtlesim_square_node', anonymous=True)
    
    # Init publisher
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) 
    rospy.loginfo("Turtles are great at drawing squares!")

    
    rate = rospy.Rate(1)  # 1 Hz
    
    while not rospy.is_shutdown():
        
        # 1. Move Forward
        cmd_vel_msg = Twist() 
        cmd_vel_msg.linear.x = 2.0   # Move forward at 2 m/s
        cmd_vel_msg.angular.z = 0.0  # Keep straight
        velocity_publisher.publish(cmd_vel_msg) 

        rate.sleep() # Executes the forward movement for 1 second

        # 2. Turn 90 Degrees
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x = 0.0    # Stop the turle from moving forward
        cmd_vel_msg.angular.z = 1.57  # Turn at ~1.57 rad/s (90 degrees)
        velocity_publisher.publish(cmd_vel_msg) 

        rate.sleep() # Executes the turn for 1 second

        ###########################################

if __name__ == '__main__': 
    try: 
        move_turtle_square() 
    except rospy.ROSInterruptException: 
        pass