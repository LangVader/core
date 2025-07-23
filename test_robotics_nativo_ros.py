#!/usr/bin/env python3
# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL ROBOTICS
# Archivo .vdr ejecutado nativamente para ROS

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Image

class VaderRoboticsROS:
    def __init__(self):
        rospy.init_node('vader_robotics_node')
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(10)
        print("🤖 VADER 7.0 - ROS Robotics Runtime")
    
    def mover_robot(self, linear=0.0, angular=0.0):
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.cmd_vel_pub.publish(twist)
    
    def ejecutar_comportamiento(self):
        while not rospy.is_shutdown():
            self.mover_robot(0.5, 0.0)  # Avanzar
            self.rate.sleep()

def main():
    robot = VaderRoboticsROS()
    robot.ejecutar_comportamiento()

if __name__ == '__main__':
    main()
