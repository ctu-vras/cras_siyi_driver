<!--
SPDX-License-Identifier: BSD-3-Clause
SPDX-FileCopyrightText: Czech Technical University in Prague
-->

# cras_siyi_driver

A ROS 2 wrapper around the [siyi_ros2](https://github.com/mzahana/siyi_ros2) camera driver.

This driver replaces the siyi_sdk manual installation step.
Just clone (with `--recursive`) the repository to your ROS workspace and build it.
You can add siyi_ros2 and siyi_msgs into the same workspace and they will automatically use the SDK
installed by this package.

The dependencies are kind of twisted - this package depends on siyi_ros2, but practically, it is
siyi_ros2 that depends on this package.
However, both packages being Python, this doesn't matter at build time, and at run time, you already
have both packages.