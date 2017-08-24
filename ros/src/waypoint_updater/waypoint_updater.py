#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Author: xxx xxx <xxx@xxx.xxx>
# Date:   xx.xx.xx
#-------------------------------------------------------------------------------

"""
This node will publish waypoints from the car's current position to some `x` distance ahead.

As mentioned in the doc, you should ideally first implement a version which does not care
about traffic lights or obstacles.

Once you have created dbw_node, you will update this node to use the status of traffic lights too.

Please note that our simulator also provides the exact location of traffic lights and their
current status in `/vehicle/traffic_lights` message. You can use this message to build this node
as well as to verify your TL classifier.

TODO (for Yousuf and Aaron): Stopline location for each traffic light.
"""

#pylint: disable=fixme

import math

import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane
#from styx_msgs.msg import Waypoint
#from styx_msgs.msg import TrafficLight

LOOKAHEAD_WPS = 200 # Number of waypoints we will publish. You can change this number

def distance(waypoints, wp1, wp2):
    """
    STUB
    """
    dist = 0
    dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
    for i in range(wp1, wp2+1):
        dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
        wp1 = i
    return dist


def get_square_gap(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return dx * dx + dy * dy


def get_closest_waypoint_index(my_position, waypoints):
    """
    position: geometry_msg.msgs.Pose instance
    waypoints: list of styx_msgs.msg.Waypoint instances
    returns index of the closest waypoint in the list waypoints
    """
    
    best_gap = 1000000000000000000000000000000.0 # Really big number
    best_index = 0 

    for i, point in enumerate(waypoints):

        other_position = waypoints.pose.pose.position 
        gap = get_square_gap(my_position, other_position)

        if gap < best_gap:
            best_index, best_gap = i, gap

    return best_index


class WaypointUpdater(object):

    def __init__(self):

        rospy.init_node('waypoint_updater')

        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        rospy.Subscriber('/base_waypoints', Lane, self.base_waypoints_cb)
        #rospy.Subscriber('/obstacle_waypoints', PoseStamped, self.obstacle_cb)
        #rospy.Subscriber('/traffic_waypoint', Int32, self.traffic_cb)

        self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)

        # Current location (x,y) of the vehicle
        self.position = None

        # Current list of base waypoints from Lane object
        self.base_waypoints = None

        rospy.loginfo('WaypointUpdater Initialized.')
        rospy.spin()

    def pose_cb(self, msg):
        rospy.loginfo('WaypointUpdater: Current Pose received.')

        # store location (x, y)
        self.position = msg.pose.position

        # get closest waypoint
        # make list of n waypoints ahead of vehicle, n = LOOKAHEAD_WPS
        # set velocity of all waypoints 
        
        # make lane data structure to be published
        # publish final waypoints

    def base_waypoints_cb(self, waypoints):
        #msg: styx_msgs.msg.lane
        rospy.loginfo('WaypointUpdater: base waypoints received')
        self.base_waypoints = msg.waypoints 

    def traffic_cb(self, msg):
        #pylint: disable=no-self-use
        rospy.loginfo('WaypointUpdater: traffic waypoint received')
        # Consider traffic light when setting waypoint velocity

    def obstacle_cb(self, msg):
        #pylint: disable=no-self-use
        rospy.loginfo('WaypointUpdater: obstacle waypoints received'
        # Consider obstacles when setting waypoint velocity

    def get_waypoint_velocity(self, waypoint):
        #pylint: disable=no-self-use
        return waypoint.twist.twist.linear.x

    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        #pylint: disable=no-self-use
        waypoints[waypoint].twist.twist.linear.x = velocity


if __name__ == '__main__':
    try:
        WaypointUpdater()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')
