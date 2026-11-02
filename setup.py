# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: Czech Technical University in Prague

from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'cras_siyi_driver'

setup(
    name=package_name,
    version='0.0.0',
    package_dir={'': 'siyi_sdk'},
    packages=find_packages(exclude=['test']) + ['siyi_sdk'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.xml')),
        (os.path.join('lib', package_name), glob('nodes/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Martin Pecka',
    maintainer_email='peckama2@fel.cvut.cz',
    description='CRAS wrapper of siyi_ros2 driver for SIYI gimbal-camera systems',
    license='BSD-3-Clause',
)
