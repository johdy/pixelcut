import cv2
import os
import numpy as np
import random
import utils

def add_video_frames(vid1: str, vid2: str, out_dir="", output_type="show", nb_frames=2000, iter_nb=0, fps=24):
	video1 = cv2.VideoCapture(vid1)
	video2 = cv2.VideoCapture(vid2)
	frame_nb1 = 0
	frame_nb2 = 0
	while True:
		ret1, frame1 = video1.read()
		ret2, frame2 = video2.read()
		if not ret1 or not ret2:
			break
		frame = frame1 + frame2
		movement1, movement2 = utils.write_or_show(frame, output_type=output_type, fps=fps)
		if not movement1 and not movement2:
			return
		frame_nb1 = frame_nb1 + movement1
		frame_nb2 = frame_nb2 + movement2
		video1.set(cv2.CAP_PROP_POS_FRAMES, frame_nb1)
		video2.set(cv2.CAP_PROP_POS_FRAMES, frame_nb2)





if __name__ == '__main__':
	vid1 = "/Users/john/Desktop/trains30/all1080/00022 20241007_150829+.mp4"
	vid2 = "/Users/john/Desktop/trains30/all1080/00013 VID_20250507_085726 (1).mp4"
	add_video_frames(vid1, vid2, output_type="show")