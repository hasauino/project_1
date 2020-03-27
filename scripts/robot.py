#!/usr/bin/env python

import rospy
import actionlib
import numpy as np
from project_1.msg import MoveBaseAction
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


class Robot:
    def __init__(self):
        self.__acs = actionlib.SimpleActionServer("move_base", MoveBaseAction,
                                                execute_cb=self.__move_2_point,
                                                auto_start=False)
        self.__acs.start()
        rospy.loginfo("ready for a goal!")
        rospy.Subscriber("/odom", Odometry, self.__pose_cb)
        self.vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=50)

        self.position = [0,0]

        self.kp = rospy.get_param("~propotional_gain", 1.0)
        self.tolerance = rospy.get_param("~tolerance", 0.3)
        self.velocity_hz = rospy.get_param("~velocity_hz", 100)
        self.max_v = rospy.get_param("~max_linear_speed", 1.0)

        self.__spd_msg = Twist()
        self.vel_rate = rospy.Rate(self.velocity_hz)

    def __move_2_point(self, point):
        rospy.loginfo("moving robot to goal..")
        while True:
            error_x = point.x - self.position[0]
            error_y = point.y - self.position[1]
            v_x, v_y = self.__controller(error_x, error_y)
            self.set_velocity(v_x, v_y)
            self.vel_rate.sleep()

            if self.__acs.is_preempt_requested():
                rospy.logwarn("goal is canceled!")
                self.set_velocity(0, 0)
                self.__acs.set_preempted()
                return

            if np.linalg.norm([error_x, error_y]) < self.tolerance:
                self.__acs.set_succeeded()
                self.set_velocity(0, 0)
                rospy.loginfo("robot reached goal successfully!")
                break

    def __pose_cb(self, msg):
        self.position = [msg.pose.pose.position.x,
                         msg.pose.pose.position.y]

    def __controller(self, err_x, err_y):
        v_x = self.kp*err_x
        v_y = self.kp*err_y

        if abs(v_x) > self.max_v:
            v_x = np.sign(v_x)*self.max_v
        
        if abs(v_y) > self.max_v:
            v_y = np.sign(v_y)*self.max_v            
        
        return v_x, v_y

    def set_velocity(self, vx, vy, w=0):
        self.__spd_msg.linear.x = vx
        self.__spd_msg.linear.y = vy
        self.__spd_msg.angular.z = w
        self.vel_pub.publish(self.__spd_msg)
