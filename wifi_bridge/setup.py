from setuptools import find_packages, setup

package_name = 'wifi_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='acer',
    maintainer_email='acer@todo.todo',
    description='WiFi Bridge',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'wifi_server = wifi_bridge.wifi_server:main',
        ],
    },
)
