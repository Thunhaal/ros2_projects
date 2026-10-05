# robot_arm_description

URDF model of the arm in **`Robotic Arm 3D Model.STEP`** (SolidWorks 2022, AP214 export).

Every link length, joint origin and joint axis below was **extracted from the STEP file**
with an OpenCASCADE-based reader (assembly tree + placement transforms + analytic
cylindrical-surface axes). Nothing kinematic was guessed. The sections marked
*assumption* say exactly what the STEP file could not supply.

---

## 1. What the STEP file actually contains

The assembly tree has 14 distinct parts:

```
Robotic Arm 3D Model
├── Base                        96.04 cm³
├── Servo Motor MG996R  x3      33.88 cm³ each
├── Waist                       68.04 cm³
├── Arm 01                      64.39 cm³
├── Arm 02 v3                   50.27 cm³
├── Arm 03                      16.50 cm³
├── Servo Motor Micro 9g x3      7.13 cm³ each
└── Gripper Assembly
    ├── Gripper base            15.72 cm³
    ├── gear1 / gear2            2.64 / 2.57 cm³
    ├── Gripper 1  x2            5.40 cm³ each
    └── grip link 1 x4           0.80 cm³ each
```

The servo part names are real evidence: **3 × MG996R** (waist, shoulder, elbow) and
**3 × 9 g micro servo** (wrist roll, wrist pitch, gripper). That gives a **5-DOF arm +
1-DOF parallel gripper** — not 6 DOF. The URDF follows the hardware, so the links are
named `link_1 … link_5` plus the two gripper fingers, as the brief allows.

### How each joint axis was found

Each revolute axis was identified as a **cluster of coaxial cylindrical faces shared by
two neighbouring parts plus a servo output shaft**. All six axes were recovered this way:

| Joint | Shared coaxial features (radius, mm) | Axis direction (raw STEP frame) |
|---|---|---|
| joint_1 | Base 60.63 / 49 / 45 / 37, Waist 48.5, MG996R#1 10.5 / 6.5 | (0, 0, 1) |
| joint_2 | Waist 24.5 / 21.5 / 9, Arm 01 21 / 18, MG996R#2 10.5 / 6.5 | (−0.1679, 0.9858, 0) |
| joint_3 | Arm 01 21 / 18, Arm 02 19 / 16 / 9, MG996R#3 10.5 / 6.5 | (−0.1679, 0.9858, 0) |
| joint_4 | Arm 02 6.5, Arm 03 6.0 / 2.5, Micro 9g#1 6.2 | (0.9839, 0.1676, −0.0626) |
| joint_5 | Arm 03 16.5 / 13.5 / 6.5, Gripper base 10 / 3.5 / 2.5, Micro 9g#2 6.2 | (−0.1524, 0.9684, 0.1975) |
| gripper | gear1 / gear2 14.63 / 12.09, Gripper base 5.4, Micro 9g 6.2 | (0.7811, −0.0044, 0.6244) |

Orthogonality checks confirm the wrist is a proper roll-pitch pair:
`d4 · d5 = −6.0e−6` and `d_gripper · d5 = 1.8e−5`.

---

## 2. Coordinate system

The whole assembly sits **yawed 9.664° about +Z** in the raw STEP frame (the `Arm 01`
pitch axis is `(−0.1679, 0.9858, 0)` instead of `(0, 1, 0)`), and the base plate sits
36.108 mm above the STEP origin. `base_link` removes both offsets:

* **origin** = on the base-plate axis (STEP X 40.780, Y −92.880), at its **bottom face**
  (STEP Z 36.108)
* **X** = forward, the arm's reach direction (STEP `(0.9858, 0.1679, 0)`)
* **Y** = left (STEP `(−0.1679, 0.9858, 0)`, i.e. the shoulder/elbow pitch axis)
* **Z** = up (STEP `(0, 0, 1)`)

Right-handed, REP-103 compliant.

Each child link frame sits **on its own joint's rotation centre with local +Z along the
rotation axis**, and local +X pointing down the link toward the next joint. That is why
every `<axis>` in the URDF is exactly `0 0 1` (always normalised by construction) and why
every link's simplified cylinder lies along its local X.

### Zero configuration

**q = 0 for all joints reproduces exactly the pose modelled in the STEP file.** That is
the only choice that does not invent information — the STEP file has no mechanical-zero
or home-pose data. As a consequence the joint limits are expressed *relative to the CAD
pose*. If you would rather have "arm straight up" as zero, measure the offset once on the
real hardware and add it to each joint's origin `rpy` (rotation about that joint's local Z).

Forward-kinematics check at q = 0, URDF vs. STEP, expressed in `base_link` (metres):

| frame | URDF FK | STEP | error |
|---|---|---|---|
| link_1 | (0.00000, 0.00000, 0.05600) | (0.00000, 0.00000, 0.05600) | 0.000 mm |
| link_2 | (0.01374, 0.00000, 0.09745) | (0.01374, 0.00000, 0.09745) | 0.0005 mm |
| link_3 | (−0.00991, 0.00000, 0.21510) | (−0.00991, 0.00000, 0.21510) | 0.0002 mm |
| link_4 | (0.08122, 0.01251, 0.20432) | (0.08122, 0.01251, 0.20432) | 0.0003 mm |
| link_5 | (0.10946, 0.01152, 0.20746) | (0.10946, 0.01152, 0.20746) | 0.0007 mm |
| gripper_finger_left | (0.13376, 0.01949, 0.17924) | (0.13376, 0.01949, 0.17924) | 0.0005 mm |
| gripper_finger_right | (0.13343, −0.00688, 0.17393) | (0.13343, −0.00688, 0.17393) | 0.0010 mm |
| end_effector | (0.19436, 0.01835, 0.11875) | (0.19436, 0.01835, 0.11875) | 0.0005 mm |

Max position error **0.001 mm**; all rotation matrices agree to < 1e−5.

---

## 3. Link–joint hierarchy

```
world
 └── world_to_base  (fixed)
      └── base_link                     cylinder  r 0.060625  h 0.056
           └── joint_1  revolute  axis Z (vertical, waist yaw)
                └── link_1              cylinder  r 0.048500  h 0.065450
                     └── joint_2  revolute  axis Z (= base +Y, shoulder pitch)
                          └── link_2    cylinder  r 0.021000  L 0.120003
                               └── joint_3  revolute  axis Z (elbow pitch, ∥ joint_2)
                                    └── link_3          cylinder  r 0.019000  L 0.092613
                                         └── joint_4  revolute  axis Z (forearm ROLL)
                                              └── link_4          cylinder  r 0.016500  L 0.046
                                                   └── joint_5  revolute  axis Z (wrist pitch)
                                                        └── link_5   box 0.07811 × 0.03202 × 0.0444
                                                             ├── joint_gripper        revolute → gripper_finger_left
                                                             ├── joint_gripper_mimic  revolute (mimic ×−1) → gripper_finger_right
                                                             └── joint_ee  fixed → end_effector
```

Structure validation (all pass):

* exactly one root link (`world`)
* every non-root link has exactly one parent
* no disconnected links, no cycles
* every joint references valid parent/child links
* every `<axis>` is a unit vector (`0 0 1`)
* every dimension is in metres
* visual and collision share identical origin + geometry on every link

---

## 4. Measurement table (STEP → URDF)

| Component | STEP measurement | URDF value | Unit | How it was obtained from the STEP geometry |
|---|---:|---:|---|---|
| Base diameter | 121.250 mm | 0.121250 | m | Outer cylindrical face of `Base`, r = 60.625 mm |
| Base height | 56.000 mm | 0.056000 | m | `Base` bounding box Z: 36.108 → 92.108 |
| Waist (link_1) diameter | 97.000 mm | 0.097000 | m | `Waist` outer cylindrical face, r = 48.500 mm |
| Waist (link_1) height | 65.450 mm | 0.065450 | m | `Waist` bounding box Z: 93.108 → 158.558 |
| Joint 1 position (in base_link) | 56.000 mm | (0, 0, 0.056000) | m | Intersection of the vertical axis (X 40.780, Y −92.880, shared by Base / Waist / MG996R#1) with the top face of `Base` |
| Joint 2 position (in link_1) | 43.670 mm | (0.013738, 0, 0.041452) | m | Common perpendicular between the joint_1 axis and the joint_2 axis; joint_2 lies exactly on the arm mid-plane (local Y = 0.000) |
| Link 2 length (J2→J3) | 120.003 mm | 0.120003 | m | Perpendicular distance between the two parallel `Arm 01` r = 21 boss axes |
| Link 2 radius | 21.000 mm | 0.021000 | m | `Arm 01` boss cylindrical faces, r = 21 (both ends) |
| Joint 3 position (in link_2) | 120.003 mm | (0.120003, 0, 0) | m | As above; J3 = orthogonal projection of J2 onto the elbow axis |
| Link 3 length (J3→J4) | 92.613 mm | 0.092613 | m | Elbow centre to the `Arm 02` / `Arm 03` mating plane on the roll axis (Arm 02 ends at t = 88.70 mm, Arm 03 starts at t = 90.55 mm along d₄) |
| Link 3 radius | 19.000 mm | 0.019000 | m | `Arm 02 v3` largest structural boss, r = 19 |
| Joint 4 position (in link_3) | 92.613 mm | (0.091765, 0, 0.012506) | m | Point on the roll axis at the Arm 02 / Arm 03 mating plane; the 12.506 mm is the real side-plate offset along the elbow axis |
| Link 4 length (along roll axis) | 46.000 mm | 0.046000 | m | `Arm 03` extent projected on d₄: 90.55 → 136.55 mm |
| Link 4 radius | 16.500 mm | 0.016500 | m | `Arm 03` outer boss, r = 16.5 (matches its 33.0 mm cross-section exactly) |
| Joint 5 position (in link_4) | 28.424 mm | (0.004993, 0, 0.027982) | m | Common perpendicular between roll axis d₄ and pitch axis d₅ (offset 4.993 mm, 27.982 mm along the roll axis) |
| Link 5 (gripper base) envelope | 78.11 × 32.02 × 44.40 mm | 0.078110 × 0.032020 × 0.044400 | m | `Gripper base` + its 9 g servo, exact extents in the link_5 frame |
| Gripper finger pivot separation | 26.900 mm | 0.026900 | m | Distance between the `gear1` and `gear2` axes |
| Finger envelope (left / right) | 93.65 × 40.69 × 16.50 / 91.58 × 41.33 × 16.50 mm | see URDF | m | gear + 2 × grip link + pad, exact extents in each finger frame |
| End-effector position (in link_5) | 122.980 mm | (0.122593, 0, −0.009776) | m | Midpoint of the two extreme `Gripper 1` fingertip vertices |
| End-effector position (in base_link) | 221.96 mm from base | (0.194360, 0.018350, 0.118750) | m | Same point, through the full transform chain |
| Overall envelope (base_link frame) | 273.47 × 139.89 × 240.43 mm | — | m | AABB of all 20 solid bodies |

**Nothing in this table is "Not directly determinable from STEP".** Everything the table
asks for was recoverable. What was *not* recoverable is listed in §6.

---

## 5. Simplified geometry

| Link | Primitive | Why this primitive |
|---|---|---|
| base_link | cylinder | `Base` genuinely is a round plate (r = 60.625 analytic face) |
| link_1 | cylinder | `Waist` is a round column (r = 48.5 analytic face) |
| link_2 | cylinder | two coaxial r = 21 bosses 120 mm apart; the real part is a 21 mm-thick plate, so the cylinder is **conservative in thickness** |
| link_3 | cylinder | r = 19 boss; real part is a 40.7 × 27.0 mm section, cylinder is conservative |
| link_4 | cylinder | r = 16.5 matches the part's 33.0 mm cross-section exactly |
| link_5 | **box** | `Gripper base` is a C-shaped bracket — a cylinder would be wrong here |
| fingers | **box** | each finger is a gear + 4-bar linkage + pad; a box envelope is the honest simplification |

The URDF has **no mesh dependency at all** — the original STEP meshes are not referenced.

### 4-bar simplification (documented deviation)

Each physical finger is a **parallel four-bar** (gear + 2 × `grip link 1` + `Gripper 1`
pad) that keeps the pad parallel while closing. URDF cannot express a closed kinematic
loop, so each finger is collapsed to **one rigid body on one revolute joint**. The pivot
location, the 26.9 mm pivot spacing and the finger envelope are all exact; only the
pad-stays-parallel behaviour is lost. `joint_gripper_mimic` mirrors `joint_gripper` with
multiplier −1.

---

## 6. STEP-derived measurements vs. assumptions

### A — Directly extracted / calculated from the STEP file

* Number of moving bodies and the assembly hierarchy
* All 6 rotation axis **directions** (from coaxial analytic cylinder clusters)
* All 6 rotation **centres** (from common perpendiculars between consecutive axes and
  from part mating planes)
* Every link length, link-to-link offset and joint spacing
* Every cylinder radius and every box extent used for visual/collision geometry
* Base location, base diameter, base height, overall arm envelope
* The 9.664° assembly yaw and the 36.108 mm base elevation in the raw STEP frame
* End-effector (TCP) position, as the midpoint of the two modelled fingertips
* The **volume** of every solid body (cm³ figures in §1)
* Gripper closing travel: rotating the modelled pads about their pivots until they meet
  on the centreline gives **−0.331 rad** (left) and **−0.376 rad** (right)

### B — Assumed, because the STEP file does not contain it

STEP AP214 as exported here carries **no material, no density, no mass and no kinematic
constraints**. The following are therefore assumptions:

1. **Density of the printed parts: 700 kg/m³.** A typical FDM part in PLA with solid
   walls and ~25 % infill. Solid PLA would be ~1240 kg/m³; if your parts are printed
   denser, scale the printed contribution of each mass accordingly.
2. **Servo masses**: MG996R = 55 g, 9 g micro servo = 9 g — manufacturer datasheet
   values. These are *named* in the STEP file, so the part identity is real; only the
   mass number comes from outside.
3. **Joint limits ±1.5708 rad** for joint_1 … joint_5. The STEP file has no limit data.
   These are conservative placeholders centred on the CAD pose, consistent with the
   ~180° travel of the named servos. **They were not read from the STEP file.**
4. **Effort / velocity limits** from servo datasheets (MG996R ≈ 0.90 N·m, 6.0 rad/s;
   9 g micro ≈ 0.18 N·m, 8.0 rad/s), derated slightly.
5. **Gripper limit −0.35 rad**, rounded from the two geometry-derived values above
   (the CAD pose is not perfectly symmetric, so one value is used for both fingers).
6. **Joint damping 0.05 and friction 0.02** — Gazebo stability values, not physical
   measurements.
7. **Inertia tensors** are computed analytically from the simplified primitive and the
   assumed mass, as requested. They are *not* the true inertia of the CAD solids.

Resulting masses:

| Link | Printed volume | Servo | Mass used |
|---|---:|---|---:|
| base_link | 96.04 cm³ | MG996R | 0.1222 kg |
| link_1 | 68.04 cm³ | MG996R | 0.1026 kg |
| link_2 | 64.39 cm³ | MG996R | 0.1001 kg |
| link_3 | 50.27 cm³ | 9 g | 0.0442 kg |
| link_4 | 16.50 cm³ | 9 g | 0.0205 kg |
| link_5 | 15.72 cm³ | 9 g | 0.0200 kg |
| gripper_finger_left | 9.57 cm³ | — | 0.0067 kg |
| gripper_finger_right | 9.64 cm³ | — | 0.0067 kg |

---

## 7. Build

```bash
cd ~/ros2_ws/src
cp -r robot_arm_description .
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select robot_arm_description --symlink-install
source install/setup.bash
```

Sanity-check the URDF before launching anything:

```bash
check_urdf $(ros2 pkg prefix robot_arm_description)/share/robot_arm_description/urdf/robot_arm.urdf
urdf_to_graphiz $(ros2 pkg prefix robot_arm_description)/share/robot_arm_description/urdf/robot_arm.urdf
```

## 8. RViz2

```bash
ros2 launch robot_arm_description display.launch.py
```

Starts `robot_state_publisher`, `joint_state_publisher_gui` (sliders for all 6 actuated
joints) and RViz2 with `world` as the fixed frame, RobotModel and TF enabled. Drag the
sliders to move the arm. Without the GUI:

```bash
ros2 launch robot_arm_description display.launch.py gui:=false
```

## 9. Gazebo

```bash
ros2 launch robot_arm_description gazebo.launch.py
# optional: gazebo.launch.py world:=empty.sdf
```

This starts `gz sim`, publishes `robot_description`, spawns the arm, bridges `/clock`,
then loads `joint_state_broadcaster`, `arm_controller` and `gripper_controller` in order.

Move it:

```bash
ros2 control list_controllers

ros2 topic pub --once /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{
  joint_names: [joint_1, joint_2, joint_3, joint_4, joint_5],
  points: [{positions: [0.5, -0.3, 0.4, 0.0, 0.2], time_from_start: {sec: 2}}]}"

ros2 topic pub --once /gripper_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{
  joint_names: [joint_gripper],
  points: [{positions: [-0.35], time_from_start: {sec: 1}}]}"
```

The arm is anchored by a fixed `world → base_link` joint, so it cannot tip or drift.
If you want it free-floating (on a mobile base, for example), delete the `world` link and
the `world_to_base` joint; `base_link` then becomes the root.

### Gazebo Classic instead of gz-sim

Replace in `urdf/robot_arm.urdf`:

* `gz_ros2_control/GazeboSimSystem` → `gazebo_ros2_control/GazeboSystem`
* the `<plugin filename="gz_ros2_control-system" …>` block →
  `<plugin name="gazebo_ros2_control" filename="libgazebo_ros2_control.so">`

and in `package.xml` swap `ros_gz_sim` / `gz_ros2_control` for `gazebo_ros` /
`gazebo_ros2_control`. The launch file then uses
`gazebo_ros/launch/gazebo.launch.py` and `spawn_entity.py`.

---

## 10. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| RViz: "No transform from [link_x] to [world]" | `robot_state_publisher` is not running, or `/joint_states` is empty | check `ros2 topic echo /joint_states`; start `joint_state_publisher_gui`; set RViz **Fixed Frame** to `world` |
| RobotModel shows nothing, status "URDF failed" | RViz subscribed before `robot_description` was latched | the display uses Transient Local QoS; if you changed it, set Durability Policy back to *Transient Local* |
| TF tree has two roots | you removed `world_to_base` but left the `world` link | delete both, or keep both |
| `check_urdf` — "link has no inertial" | you added a link without `<inertial>` | every non-root link needs mass > 0 and a positive-definite inertia; Gazebo silently drops links with zero mass |
| Links explode / fly apart on spawn | inertia values too small relative to mass, or a mass of 0 | keep `ixx, iyy, izz` ≥ 1e−7; do not lower the masses below the values in §6 |
| Arm slowly sags or drifts | no controller is holding position | make sure `arm_controller` actually loaded (`ros2 control list_controllers`), and that `update_rate` in `arm_controllers.yaml` is ≥ the physics rate |
| Arm jitters at rest | `update_rate` too low, or damping too small | raise `update_rate` to 500, or raise `<dynamics damping>` to 0.2 |
| Whole robot sinks through the ground | no `world` anchor and no ground contact | keep the `world_to_base` fixed joint |
| `gz_ros2_control` — "Could not find parameter file" | the `$(find robot_arm_description)` token was not substituted | launch via `gazebo.launch.py`, which does the substitution; if you load the URDF by hand, replace the token with the absolute share path |
| Controllers never spawn | `controller_manager` lives inside the Gazebo process and starts late | the launch file already chains spawners on `OnProcessExit`; if you spawn manually, add `--controller-manager-timeout 60` |
| Gripper fingers move together instead of opposite | `<mimic>` unsupported in your ros2_control version | drop the mimic and add `joint_gripper_mimic` to `gripper_controller`'s joint list with an inverted command |
| Joints move the wrong way | sign convention | negate the joint's `<axis>` (`0 0 -1`) — it stays normalised, and the kinematics stay exact |
| Robot appears rotated ~9.7° | you loaded raw STEP coordinates somewhere | the URDF already removes the assembly yaw; don't re-apply it in the spawn pose |
