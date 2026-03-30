#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from std_msgs.msg import Float64
import math

# Global variables to track our turtle's journey
previous_x = None
previous_y = None
total_distance = 0.0

# Define the publisher globally so the callback function can use it
distance_pub = None

def pose_callback(data):
    """
    This function is called every time a new message is received on the pose topic.
    """
    global previous_x, previous_y, total_distance, distance_pub
    
    # 1. Handle the initial state
    # If this is the very first time we're getting a pose, we just set the 
    # previous coordinates to where the turtle currently is and return.
    if previous_x is None or previous_y is None:
        previous_x = data.x
        previous_y = data.y
        return
        
    # 2. Calculate the difference
    x_diff = data.x - previous_x
    y_diff = data.y - previous_y
    
    # 3. Apply Euclidean distance formula
    distance_moved = math.sqrt(x_diff**2 + y_diff**2)
    
    # 4. Add to total distance 
    total_distance += distance_moved
    
    # 5. Update previous coordinates for the next time the callback runs 
    previous_x = data.x
    previous_y = data.y
    
    # 6. Publish the new total distance
    distance_pub.publish(total_distance)

def distance_tracker_node():
    global distance_pub
    
    # 1. Initialize the node
    rospy.init_node('turtle_distance_tracker', anonymous=True)
    
    # 2. Set up the Publisher
    # Publishing to '/turtle_dist' using the Float64 message type [cite: 11, 19]
    distance_pub = rospy.Publisher('/turtle_dist', Float64, queue_size=10)
    
    # 3. Set up the Subscriber
    # Subscribing to the turtlesim pose topic to get live coordinates 
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
    
    rospy.loginfo("Distance tracker started! Listening to /turtle1/pose and publishing to /turtle_dist...")
    
    # rospy.spin() keeps your node running and listening for messages
    rospy.spin()

if __name__ == '__main__':
    try:
        distance_tracker_node()
    except rospy.ROSInterruptException:
        pass
