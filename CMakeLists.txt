cmake_minimum_required(VERSION 2.8.3)
project(project_1)


find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  nav_msgs
  actionlib_msgs
)

 add_action_files(
   FILES
   MoveBase.action
 )

 generate_messages(
   DEPENDENCIES
   geometry_msgs nav_msgs actionlib_msgs
 )

catkin_package(
  CATKIN_DEPENDS rospy geometry_msgs nav_msgs actionlib_msgs
)

include_directories(

  ${catkin_INCLUDE_DIRS}
)
