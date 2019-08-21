import os
import subprocess
import argparse

from pose import pose_estimation
from split_vid import vid_into_frames


parser = argparse.ArgumentParser('Pose estimation on ')
parser.add_argument('--split', action='store_true', default=False, help='Split videos')
parser.add_argument('--pose', action='store_true', default=False, help='Pose estimation')


def main():
    # root directory
    root_direct = '/home/ubuntu/PoseData'
    # UCF_Anomalies dataset path
    dset_root = os.path.join(root_direct, 'Anomaly-Videos-Part-1')
    args = parser.parse_args()

    out_split = os.path.join(root_direct, 'train')
    if not os.path.isdir(out_split):
        os.mkdir(out_split)

    # create new directory structure and write frames at path out_split
    if args.split:
        vid_into_frames(dset_root, out_split)


    # output annotation path
    outanns = os.path.join(root_direct, 'train_anns')
    if not os.path.isdir(outanns):
        os.mkdir(outanns)

    # set working directory for AlphaPose framework
    os.chdir(' /home/ubuntu/PoseData/AlphaPose/')
    # create new directory structure and write annotation files at out_anns
    if args.pose:
        print('Running pose estimation: \n')
        pose_estimation(out_split, outanns)

if __name__ == "__main__":
    main()
