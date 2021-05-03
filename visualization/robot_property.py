import sapien.core as sapien
import os
import numpy as np

_NAME_MAPPING = {
    "allegro": "../assets/allegro_hand_description_right.urdf",
    "allegro_left": "../assets/allegro_hand_description_left.urdf",
    "allegro_right": "../assets/allegro_hand_description_right.urdf",
    "adroit": "../assets/adroit_hand.urdf",
}
SUPPORTED_ROBOT = list(_NAME_MAPPING.keys())


def load_robot(renderer: sapien.VulkanRenderer, scene: sapien.Scene, robot_name):
    loader = scene.create_urdf_loader()
    robot_builder = loader.load_file_as_articulation_builder(_NAME_MAPPING[robot_name])
    for link_builder in robot_builder.get_link_builders():
        link_builder.set_collision_group(0, 1, 2, 2)
    robot = robot_builder.build(fix_root_link=True)
    scene.step()
    scene.update_render()

    # Robot specific property
    if robot_name == "adroit":
        # mat_viz = renderer.create_material()
        for link in robot.get_links():
            for geom in link.get_visual_bodies():
                for shape in geom.get_render_shapes():
                    print("hhh")
                    mat_viz = shape.material
                    mat_viz.set_base_color(np.array([0.9, 0.7, 0.5, 1]))
                    mat_viz.set_specular(0.7)
                    mat_viz.set_metallic(0.1)
                    mat_viz.set_roughness(0.1)

    return robot
