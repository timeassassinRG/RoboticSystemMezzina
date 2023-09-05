cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

find_package(gazebo REQUIRED)
include_directories(${GAZEBO_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})
list(APPEND CMAKE_CXX_FLAGS "${GAZEBO_CXX_FLAGS}")

add_library(pose_plugin SHARED pose/pose_plugin.cc)
add_library(tester_plugin SHARED tester/tester_plugin.cc)
add_library(control_plugin SHARED control/control_plugin.cc control/pid.cc)
target_link_libraries(pose_plugin ${GAZEBO_LIBRARIES})
target_link_libraries(tester_plugin ${GAZEBO_LIBRARIES})
target_link_libraries(control_plugin ${GAZEBO_LIBRARIES})
