from setuptools import find_packages, setup

package_name = 'esp32_interface'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            'share/' + package_name,
            ['package.xml'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='acer',
    maintainer_email='acer@todo.todo',
    description='ESP32 ROS2 Interface',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
	    'serial_node = esp32_interface.serial_node:main',
	    'motor_node = esp32_interface.motor_node:main',
            'speed_controller = esp32_interface.speed_controller:main',
        ],
    },
)
