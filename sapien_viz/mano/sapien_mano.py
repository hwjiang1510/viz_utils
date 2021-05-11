import sapien.core as sapien
from .model import load
import transforms3d
import torch


class SapienMANOPredictor:
    def __init__(self, mano_path: str, batch_size: int = 1, use_cuda=True):
        self.model = load(model_path=mano_path, num_pca_comps=45, flat_hand_mean=False, batch_size=batch_size)
        if use_cuda:
            self.model = self.model.cuda()
        self.use_cuda = use_cuda
        self.batch_size = batch_size
        self.latest_result = None

    def forward(self, betas, hand_pose, global_trans=None, global_rot=None):
        if global_rot is None:
            global_rot = torch.zeros(self.batch_size, 3)
        else:
            global_rot = torch.from_numpy(global_trans)

        if global_trans is None:
            global_trans = torch.zeros(self.batch_size, 3)
        else:
            global_trans = torch.from_numpy(global_trans)

        betas = torch.from_numpy(betas)
        hand_pose = torch.from_numpy(hand_pose)

        if self.use_cuda:
            global_rot = global_rot.cuda()
            global_trans = global_trans.cuda()
            betas = betas.cuda()
            hand_pose = hand_pose.cuda()

        self.latest_result = self.model(betas=betas, global_orient=global_rot, hand_pose=hand_pose, transl=global_trans,
                                        return_verts=True, return_tips=True)
        return self.latest_result

    @property
    def latest_mesh(self):
        if self.latest_result is None:
            raise RuntimeError(f"Call latest mesh after at least one forward round")

    # def hand_meshes(self,output, vc= colors['skin']):
    #
    #     vertices = to_np(output.vertices)
    #     if vertices.ndim <3:
    #         vertices = vertices.reshape(-1,778,3)
    #
    #     meshes = []
    #     for v in vertices:
    #         hand_mesh = Mesh(vertices=v, faces=self.faces, vc=vc)
    #         meshes.append(hand_mesh)
    #
    #     return  meshes
