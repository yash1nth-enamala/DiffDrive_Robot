import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
import xacro

def generate_launch_description():
    
    # this name has to match the robot name in the Xacro file
    robotXacroName='differential_drive_robot'
    # this is the name of our package, at the same time this
    # folder that will be used to define the paths
    namePackage = 'patrol_bot'
    
    # this is a relative path to the xacro file defining the
    modelFileRelativePath = 'model/robot.xacro'
    
    # this is a relative path to the Gazebo world file
    worldFileRelativePath = 'model/empty_world.world'
    
    # this is the absolute path to the model
    pathModelFile = os.path.join(get_package_share_directory(namePackage),modelFileRelativePath)
                                 
    # this is the absolute path to the world model
    pathWorldFile = os.path.join(get_package_share_directory(namePackage),worldFileRelativePath)
                                 
    # get the robot description from the xacro model file
    robotDescription = xacro.process_file(pathModelFile).toxml()
    # this is the launch file from the gazebo_ros package
    gazebo_rosPackageLaunch=PythonLaunchDescriptionSource (os.path.join(get_package_share_directory( 'gazebo_ros'),
    'launch', 'gazebo.launch.py'))
    
    # this is the launch description
    gazeboLaunch=IncludeLaunchDescription (gazebo_rosPackageLaunch, launch_arguments={'world': pathWorldFile}.items())
    
    # here, we create a gazebo_ros Node
    spawnModelNode = Node(package= 'gazebo_ros', executable= 'spawn_entity.py',
                            arguments=['-topic', 'robot_description','-entity', robotXacroName],output='screen')
    
    # Robot State Publisher Node
    nodeRobotStatePublisher = Node(
    package='robot_state_publisher', 
    executable='robot_state_publisher',
    output='screen',
    parameters=[{ 'robot_description': robotDescription,
    'use_sim_time': True}]
    )
    
    joint_state_publisher_node = Node(
    package='joint_state_publisher',
    executable='joint_state_publisher',
    name='joint_state_publisher'
    )
    
    joint_state_publisher_gui = Node(
    package='joint_state_publisher_gui',
    executable='joint_state_publisher_gui',
    output='screen',
    name='joint_state_publisher_gui'
    )
    
    rviz_config_file = os.path.join(get_package_share_directory(namePackage), 'rviz2', 'config.rviz')
    rviz_node = Node(
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    arguments=['-d', rviz_config_file],
    output='screen'
    ) 
    
    # here we create an empty launch description object
    launchDescriptionObject = LaunchDescription()
    
    # we add gazeboLaunch
    launchDescriptionObject.add_action(gazeboLaunch)
    
    # we add the two nodes
    launchDescriptionObject.add_action(spawnModelNode)
    launchDescriptionObject.add_action(nodeRobotStatePublisher)
    launchDescriptionObject.add_action(rviz_node)
    launchDescriptionObject.add_action(joint_state_publisher_gui)
    return launchDescriptionObject
