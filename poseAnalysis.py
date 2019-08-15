import os
import subprocess
import json
import csv
import argparse


'''
This module contains three different functions: 
 - split_videos ---> runs ffmpeg on the dataset with fixed fps
 - pose_estimation ----> runs demo.py from AlphaPose framework on folder frames
 - vis_stats ---> prints and save statistics about pose estimation on the dataset
'''

parser = argparse.ArgumentParser('Pose estimation analysis on UCF-Anomaly-Detection dataset')

parser.add_argument('--split', action='store_true', default=False, help='Store true flag to split videos')
parser.add_argument('--pose', action='store_true', default=False, help='Store true flag to pose estimation')
parser.add_argument('--stats', action='store_true', default=False, help='Store true flag to print and save statistics')


def load_json(ann):
    #load json

    ann = os.path.join(ann, 'alphapose-results.json')
    if os.path.isfile(ann):
        results = json.load(open(ann, 'r'))

        anns = {}
        last_image_name = ' '
        for i in range(len(results)):
            imgpath = results[i]['image_id']
            if last_image_name != imgpath:
                anns[imgpath] = []
                anns[imgpath].append({'keypoints': results[i]['keypoints'], 'scores': results[i]['score']})
            else:
                anns[imgpath].append({'keypoints': results[i]['keypoints'], 'scores': results[i]['score']})
            last_image_name = imgpath
    else:
        anns = {}

    return anns

def split_videos(dset_root, outpath, target):

    for i, (dire, folds, fils) in enumerate(os.walk(dset_root)):
        if i ==0:
            #print('Main dataset directory: {}\n  Subdirectories within it: {}\n'.format(dire, folds))
            continue
        if i > 0 and len(fils) > 0 and (dire.split('/')[-1] not in target):
            continue

        #print('Processing videos in: {}'.format(dire))
        for vid_name in fils:

            # path to video
            pvid = os.path.join(dire, vid_name)

            # create a folder for each video
            fname = vid_name.split('.mp4')[0]
            path_fold = os.path.join(outpath, dire.split('/')[-1], fname)
            if not os.path.isdir(path_fold):
                os.makedirs(path_fold)

            #print('*' * 100)
            #print(pvid)
            #print(path_fold)

            cmd = "ffmpeg -i {}  -vf fps=5  {}/%04d.jpg".format(pvid, path_fold)
            subprocess.call(cmd, shell=True)

def pose_estimation(outpath, outanns, target):
    max_length = 2e03
    args = parser.parse_args()
    for i, (dire, folds, fils) in enumerate(os.walk(outpath)):
        if i == 0:
            print('Main dataset directory: {}\n  Subdirectories within it: {}\n'.format(dire, folds))
            continue
        if len(folds) == 0 and len(fils) > 0 and (dire.split('/')[-2] in target):
            if args.limit and len(fils) > max_length:
                continue

            print('Processing video frames in: {}'.format(dire))

            # run a python module and output the json file at the corresponding annotation folder
            ldir = dire.split('/')
            out_json = os.path.join(outanns, ldir[-2], ldir[-1])
            if not os.path.isdir(out_json):
                os.makedirs(out_json)
            cmd = "python demo.py --indir {}  --outdir {}".format(dire, out_json)
            subprocess.call(cmd, shell=True)

