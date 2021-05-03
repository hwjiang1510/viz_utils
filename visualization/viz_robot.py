import numpy as np
import sapien.core as sapien
from sapien.utils import Viewer
import argparse
import os

_NAME_MAPPING = {
    "allegro": "../assets/allegro_hand_description_right.urdf",
    "allegro_left": "../assets/allegro_hand_description_left.urdf",
    "allegro_right": "../assets/allegro_hand_description_right.urdf"
}
_SUPPORTED_ROBOT = list(_NAME_MAPPING.keys())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--robot', action='store', type=str, required=True, help="Name of the robot")
    parser.add_argument('-j', '--joint-pos', nargs='+', type=float,
                        help="Single frame joint pos. For joint trajectory visualization, please use numpy file")
    return parser.parse_args()


def visualize_articulation(filename, qpos_array=np.zeros([0, 0]), fps=10):
    # Setup
    engine = sapien.Engine()
    renderer = sapien.VulkanRenderer(offscreen_only=False)
    engine.set_renderer(renderer)
    config = sapien.SceneConfig()
    config.gravity = np.array([0, 0, 0])
    scene = engine.create_scene(config=config)
    scene.set_timestep(1 / 125)
    visual_material = renderer.create_material()
    visual_material.set_base_color(np.array([232, 231, 201, 255]) / 255)
    visual_material.set_roughness(0.8)
    scene.add_ground(-1, render_material=visual_material)

    # Lighting
    render_scene = scene.get_renderer_scene()
    render_scene.set_ambient_light(np.array([0.4, 0.4, 0.4]))
    render_scene.add_directional_light(np.array([1, -1, -1]), np.array([0.5, 0.5, 0.5]))
    render_scene.add_point_light(np.array([2, 2, 2]), np.array([1, 1, 1]))
    render_scene.add_point_light(np.array([2, -2, 2]), np.array([1, 1, 1]))
    render_scene.add_point_light(np.array([-2, 0, 2]), np.array([1, 1, 1]))

    # Articulation
    loader = scene.create_urdf_loader()
    robot_builder = loader.load_file_as_articulation_builder(filename)
    for link_builder in robot_builder.get_link_builders():
        link_builder.set_collision_group(0, 1, 2, 2)
    robot = robot_builder.build(fix_root_link=True)

    # Validate joint trajectory
    trajectory_dof = qpos_array.shape[1]
    if trajectory_dof != robot.dof and trajectory_dof > 0:
        raise ValueError(f"DoF not match: given trajectory has {trajectory_dof} joints"
                         f" while the robot model only has {robot.dof} joints")

    # Viewer
    viewer = Viewer(renderer)
    viewer.set_scene(scene)
    viewer.set_camera_xyz(1, 0, 1)
    viewer.set_camera_rpy(0, -0.6, 3.14)

    # Visualization Loop
    trajectory_length = qpos_array.shape[0]
    scene.step()
    scene.update_render()

    for i in range(trajectory_length):
        for _ in range(int(fps)):
            robot.set_qpos(qpos_array[i])
            robot.set_drive_target(qpos_array[i])
            scene.step()
            scene.update_render()
            viewer.render()
    if trajectory_length > 0:
        print(f"Finish visualize robot trajectory with {trajectory_length} trajectory points.")

    while not viewer.closed:
        scene.step()
        scene.update_render()
        viewer.render()


def main():
    args = parse_args()
    if args.robot not in _SUPPORTED_ROBOT:
        raise ValueError(
            f"Robot name {args.robot} not supported. List of supported robots are shown below: \n{_SUPPORTED_ROBOT}")

    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_path = os.path.join(current_dir, _NAME_MAPPING[args.robot])
    qpos = args.joint_pos
    if qpos is not None:
        qpos_array = np.array(qpos)[None, :]
    else:
        qpos_array = np.zeros([0, 0])

    visualize_articulation(robot_path, qpos_array)


if __name__ == '__main__':
    main()
