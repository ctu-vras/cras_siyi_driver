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

Subscribes to `/siyi/cmd/cmd_vel` (`geometry_msgs/TwistStamped`) and republishes it as gimbal
commands understood by siyi_ros2:

- `siyi_msgs/GimbalRateCmd` on `/siyi/cmd/rate`, using `angular.z` as the yaw rate and `angular.y`
  as the pitch rate (converted from rad/s to deg/s and multiplied by `rate_scale`),
- `siyi_msgs/srv/SetAbsoluteZoom` service calls on `/siyi/set_zoom`, using `linear.x` as a zoom
  velocity (clamped to ±1, ignored within `zoom_threshold`). The camera cannot report its zoom level,
  so the node is the sole authority on it: it keeps its own estimate, starting at `initial_zoom`
  (default `1.0`, which is also the minimum), never exceeds `max_zoom` (at most `30.0`), and
  integrates the velocity into it (`zoom_speed` zoom levels per second at full `linear.x`). The
  estimate is sent as an absolute zoom request at most `zoom_rate_hz` times per second (4 Hz
  maximum), so the zoom feels velocity-controlled while still being responsive. Only one request is
  in flight at a time and it always carries the newest zoom level. The first request is sent as soon
  as the service is available, and the estimate stops advancing when no `cmd_vel` arrives for
  `cmd_vel_timeout` seconds. A request unanswered for `zoom_service_timeout` seconds is abandoned,
  and a failed or abandoned zoom level is retried with a growing backoff for as long as the node
  wants the camera to be there.

It is launched by `siyi_full.launch.xml`.