import numpy as np
import sapien.core as sapien
import open3d
from typing import List

Vector3dVector = open3d.utility.Vector3dVector
Vector3iVector = open3d.utility.Vector3iVector


def render_geometry_to_open3d_mesh(render_shape: sapien.RenderShape):
    mesh = render_shape.mesh
    pose = render_shape.pose.to_transformation_matrix()
    scale = render_shape.scale

    vertices = mesh.vertices
    indices = np.reshape(mesh.indices, [-1, 3]).astype(np.int32)
    normals = mesh.normals
    triangle_mesh = open3d.geometry.TriangleMesh(Vector3dVector(vertices * scale[None, :]), Vector3iVector(indices))
    triangle_mesh.vertex_normals = Vector3dVector(normals)
    triangle_mesh.transform(pose)
    return triangle_mesh


def generate_actor_point_cloud(actor: sapien.ActorBase, surface_density=500):
    points_list = []
    normals_list = []
    for render_body in actor.get_visual_bodies():
        for render_shape in render_body.get_render_shapes():
            triangle_mesh = render_geometry_to_open3d_mesh(render_shape)
            surface_area = triangle_mesh.get_surface_area()
            pc = triangle_mesh.sample_points_poisson_disk(int(surface_area * surface_density))
            points_list.append(np.asarray(pc.points))
            normals_list.append(np.asarray(pc.normals))

    pc = open3d.geometry.PointCloud(Vector3dVector(np.concatenate(points_list, 0)))
    pc.normals = Vector3dVector(np.concatenate(normals_list))
    return pc


def generate_actors_point_cloud(actors: List[sapien.ActorBase], surface_density=500):
    points_list = []
    normals_list = []
    for actor in actors:
        pose = actor.get_pose()
        pc = generate_actor_point_cloud(actor, surface_density)
        pc.transform(pose.to_transformation_matrix())
        points_list.append(np.asarray(pc.points))
        normals_list.append(np.asarray(pc.normals))

    pc = open3d.geometry.PointCloud(Vector3dVector(np.concatenate(points_list, 0)))
    pc.normals = Vector3dVector(np.concatenate(normals_list))
    return pc
