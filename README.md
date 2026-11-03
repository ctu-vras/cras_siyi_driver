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

## Nodes

### `cmd_vel_to_gimbal`

Turns `geometry_msgs/TwistStamped` commands into the gimbal commands understood by siyi_ros2:
`siyi_msgs/GimbalRateCmd` on `siyi/cmd/rate`, `siyi_msgs/srv/SetAbsoluteZoom` service calls on
`siyi/set_zoom` and `siyi_msgs/srv/CenterGimbal` on `siyi/center`.

Multiple gimbal control modes are available:

#### Rate mode: `siyi/cmd/cmd_vel`

`angular.z` is the requested yaw rate and `angular.y` the requested pitch rate in rad/s.

`linear.x` is interpreted as change in zoom levels per second.

#### Relative position mode: `siyi/cmd/cmd_pos_rel`

Here the twist is a requested *relative pose change*: every message asks for a rotation of
`angular.z` around yaw and `angular.y` around pitch (in radians) with respect to the pose the camera
is currently at. An open-loop proportional controller running at `pos_rate_hz`
servos the gimbal to the requested pose through `siyi/cmd/rate` (output clamped to `pos_max_rate`
rad/s) and goes quiet once the pose is within `pos_tolerance_deg` from the relative target.

`linear.x` is interpreted as relative change in zoom level. The zoom is changed as fast as possible.

While a relative position command is being executed, all rate commands are ignored.

#### Absolute position mode: `siyi/cmd/cmd_pos`

So far, absolute pose gimbal control is not implemented. Only zoom is working in this mode.

`linear.x` is interpreted as absolute zoom level. The zoom is changed as fast as possible.

#### Zoom details

The node calls `siyi_msgs/srv/SetAbsoluteZoom` on `siyi/set_zoom`, even for velocity commands,
because the ManualZoom topic is broken. The camera cannot report its zoom level,
so the node is the sole authority on it: it keeps its own estimate starting at `initial_zoom`
(default `1.0`, which is also the minimum), never exceeds `max_zoom` (at most `30.0`), and integrates
the velocity or pose changes into it. The estimate is sent to topic `siyi/zoom` (latched) and also
to `siyi/set_zoom` (`zoom_rate_hz` times per second), so the zoom
feels velocity-controlled while still being responsive. Only one request is in flight at a time and
it always carries the newest zoom level.

Because the camera doesn't report its zoom level, treat the value as a rough estimate (namely, the
camera animates the zoom level changes, but this node reports the changes as executed instantly).
