#!/usr/bin/env python3
"""Spawn robot_arm in Gazebo (gz-sim / Harmonic-Fortress) with ros2_control."""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (IncludeLaunchDescription, RegisterEventHandler,
                            ExecuteProcess, DeclareLaunchArgument)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('robot_arm_description')
    urdf_file = os.path.join(pkg, 'urdf', 'robot_arm.urdf')

    # The URDF ships with a "$(find robot_arm_description)" token inside the
    # gz_ros2_control <parameters> tag.  Plain URDF has no substitution engine,
    # so resolve it here to the installed share path.
    with open(urdf_file, 'r') as f:
        robot_description = f.read().replace('$(find robot_arm_description)', pkg)

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r -v 3 ', LaunchConfiguration('world')]}.items(),
    )

    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher',
               output='screen',
               parameters=[{'robot_description': robot_description,
                            'use_sim_time': True}])

    spawn = Node(package='ros_gz_sim', executable='create', output='screen',
                 arguments=['-topic', 'robot_description',
                            '-name', 'robot_arm',
                            '-x', '0', '-y', '0', '-z', '0'])

    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                  arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
                  output='screen')

    jsb = ExecuteProcess(
        cmd=['ros2', 'run', 'controller_manager', 'spawner',
             'joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen')
    arm = ExecuteProcess(
        cmd=['ros2', 'run', 'controller_manager', 'spawner',
             'arm_controller', '--controller-manager', '/controller_manager'],
        output='screen')
    grip = ExecuteProcess(
        cmd=['ros2', 'run', 'controller_manager', 'spawner',
             'gripper_controller', '--controller-manager', '/controller_manager'],
        output='screen')

    return LaunchDescription([
        DeclareLaunchArgument('world', default_value='empty.sdf'),
        gz_sim, rsp, bridge, spawn,
        RegisterEventHandler(OnProcessExit(target_action=spawn, on_exit=[jsb])),
        RegisterEventHandler(OnProcessExit(target_action=jsb,   on_exit=[arm])),
        RegisterEventHandler(OnProcessExit(target_action=arm,   on_exit=[grip])),
    ])
