import os
import subprocess


def pose_estimation(outpath, outanns):

    for i,(directory, fold, files) in enumerate(os.walk(outpath)):
        # run command on the frames
        if len(fold) == 0 and len(files) > 0:
            # loop over video frames
            print('Processing video frames in: {}'.format(directory))

            # run a python module 
            ldir = directory.split('/')
            cmd = "python demo.py --indir {}".format(directory)
            subprocess.call(cmd , shell=True)
