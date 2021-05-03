# viz_utils

## Installation

Visit [Wheel Home](http://volcan.ucsd.edu:8088) and choose one wheel to install according to your python
version, for example (**python 3.8**):

```bash
pip3 install http://volcan.ucsd.edu:8088/files/wheel/sapien-0.11.0.dev2-cp38-cp38-manylinux2014_x86_64.whl
```

Then install the visualization utils, including robot model:

```bash
git clone https://github.com/yzqin/viz_utils
cd viz_utils
pip3 install .
```

## Usage

```bash
usage: viz_robot [-h] -r ROBOT [-j JOINT_POS [JOINT_POS ...]] [-f JOINT_FILE] [--fps FPS] [-s] [--dict-key DICT_KEY]

optional arguments:
  -h, --help            show this help message and exit
  -r ROBOT, --robot ROBOT
                        Name of the robot
  -j JOINT_POS [JOINT_POS ...], --joint-pos JOINT_POS [JOINT_POS ...]
                        Single frame joint pos. For joint trajectory visualization, please use numpy file
  -f JOINT_FILE, --joint-file JOINT_FILE
                        Filename to save the robot joint trajectory
  --fps FPS             FPS to visualize the trajectory
  -s, --smooth          Whether to use drive to generate trajectory (simulate but not animate)
  --dict-key DICT_KEY   Key name for joint pos if the given file is a dict
```

For example, use the test data in this repo:

```bash
viz_robot -f test_assets/obj_id_37.pkl -r adroit --dict-key retarget_qpos -s
```
