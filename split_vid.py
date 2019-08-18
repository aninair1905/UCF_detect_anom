import os
import subprocess


def vid_into_frames(root_dataset, out_path):

    for i, (folders, fil, directory) in enumerate(os.walk(root_dataset)):
        for vid_name in fil:

            # path to video
            vid_path = os.path.join(directory, vid_name)

            # create a folder for each video
            fname = vid_name.split('.mp4')[0]
            path_fold = os.path.join(out_path, directory.split('/')[-1], fname)
            if not os.path.isdir(path_fold):
                os.makedirs(path_fold)

            # executing ffmpeg -i file.mp4 -vf fps=5 path/%04d.jpg
            print(path_fold)
            cmd = "ffmpeg -i {}  -vf fps=5  {}/%04d.jpg".format(vid_path, path_fold)
            subprocess.call(cmd, shell=True)

