import numpy as np
import os
from utils.dataset import Dataset
from utils.skeleton import Skeleton

# The dataset contains 32 joints but only 16 are movable

H36M_JOINTS = {
    'Hip':   0,
    'RHip':  1,
    'RKnee': 2,
    'RFoot': 3,
    'LHip':  6,
    'LKnee': 7,
    'LFoot': 8,
    'Spine': 12,
    'Thorax': 13,
    'Neck/Nose': 14,
    'Head': 15,
    'LShoulder': 17,
    'LElbow': 18,
    'LWrist': 19,
    'RShoulder': 25,
    'RElbow': 26,
    'RWrist': 27
}

class DatasetH36M(Dataset):

    def __init__(self, mode, t_his=25, t_pred=100, actions='all', use_vel=False):
        self.use_vel = use_vel
        super().__init__(mode, t_his, t_pred, actions)
        if use_vel:
            self.traj_dim += 3

    def prepare_data(self):
        self.data_file = os.path.join('data', 'data_3d_h36m.npz')
        self.subjects_split = {'train': [1, 5, 6, 7, 8],
                               'test': [9, 11]}
        self.subjects = ['S%d' % x for x in self.subjects_split[self.mode]]
        self.skeleton = Skeleton(parents=[-1, 0, 1, 2, 3, 4, 0, 6, 7, 8, 9, 0, 11, 12, 13, 14, 12,
                                          16, 17, 18, 19, 20, 19, 22, 12, 24, 25, 26, 27, 28, 27, 30],
                                 joints_left=[6, 7, 8, 9, 10, 16, 17, 18, 19, 20, 21, 22, 23],
                                 joints_right=[1, 2, 3, 4, 5, 24, 25, 26, 27, 28, 29, 30, 31])
        self.removed_joints = {4, 5, 9, 10, 11, 16, 20, 21, 22, 23, 24, 28, 29, 30, 31}
        self.kept_joints = np.array([x for x in range(32) if x not in self.removed_joints])
        self.skeleton.remove_joints(self.removed_joints)
        self.skeleton._parents[11] = 8
        self.skeleton._parents[14] = 8
        self.process_data()

    def process_data(self):
        data_o = np.load(self.data_file, allow_pickle=True)['positions_3d'].item()
        data_f = dict(filter(lambda x: x[0] in self.subjects, data_o.items()))
        if self.actions != 'all':
            for key in list(data_f.keys()):
                data_f[key] = dict(filter(lambda x: all([a in x[0] for a in self.actions]), data_f[key].items()))
                if len(data_f[key]) == 0:
                    data_f.pop(key)
        for data_s in data_f.values():
            for action in data_s.keys():
                seq = data_s[action][:, self.kept_joints, :]
                if self.use_vel:
                    v = (np.diff(seq[:, :1], axis=0) * 50).clip(-5.0, 5.0)
                    v = np.append(v, v[[-1]], axis=0)
                seq[:, 1:] -= seq[:, :1]
                if self.use_vel:
                    seq = np.concatenate((seq, v), axis=1)
                data_s[action] = seq
        self.data = data_f


if __name__ == '__main__':
    np.random.seed(0)
    actions = {'WalkDog'}
    dataset = DatasetH36M('train', actions=actions)
    generator = dataset.sampling_generator(num_samples=1000, batch_size=8)
    dataset.normalize_data()
    # generator = dataset.iter_generator()
    for data in generator:
        print(data.shape)


