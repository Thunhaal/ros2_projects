#!/usr/bin/env python3
"""RViz2 display + interactive joint sliders for robot_arm.urdf."""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('robot_arm_description')
    urdf_file = os.path.join(pkg, 'urdf', 'robot_arm.urdf')
    rviz_file = os.path.join(pkg, 'config', 'view_robot.rviz')

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    gui = LaunchConfiguration('gui')

    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true',
                              description='Start joint_state_publisher_gui'),

        Node(package='robot_state_publisher',
             executable='robot_state_publisher',
             output='screen',
             parameters=[{'robot_description': robot_description,
                          'use_sim_time': False}]),

        Node(package='joint_state_publisher_gui',
             executable='joint_state_publisher_gui',
             condition=IfCondition(gui),
             output='screen'),

        Node(package='joint_state_publisher',
             executable='joint_state_publisher',
             condition=UnlessCondition(gui),
             output='screen'),

        Node(package='rviz2', executable='rviz2',
             arguments=['-d', rviz_file],
             output='screen'),
    ])
