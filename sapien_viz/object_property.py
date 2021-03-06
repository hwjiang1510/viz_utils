import sapien.core as sapien
import os
import numpy as np

_YCB_OBJECT_MAPPING = {"master_chef_can": "002", "cracker_box": "003", "sugar_box": "004", "tomato_soup_can": "005",
                       "mustard_bottle": "006", "potted_meat_can": "010", "banana": "011", "bleach_cleanser": "021",
                       "bowl": "024", "mug": "025", "large_clamp": "051"}

SUPPORTED_OBJECT = list(_YCB_OBJECT_MAPPING.keys())


def load_ycb_objects(renderer: sapien.VulkanRenderer, scene: sapien.Scene, object_names):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    ycb_dir = os.path.join(current_dir, "assets/ycb")

    actors = {}
    for object_name in object_names:
        visual_file_name = os.path.join(ycb_dir, "visual", f"{_YCB_OBJECT_MAPPING[object_name]}_{object_name}",
                                        "textured_simple.obj")
        builder = scene.create_actor_builder()
        builder.add_visual_from_file(filename=visual_file_name)
        # TODO: add collision shapes
        actor = builder.build(object_name)
        actors[object_name] = actor

    return actors
