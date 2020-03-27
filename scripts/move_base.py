#!/usr/bin/env python

import rospy
from robot import Robot


rospy.init_node("move_base")
youbot = Robot()

r = rospy.Rate(1)

while not rospy.is_shutdown():
    print youbot.position
    r.sleep()