import cv2
import numpy as np
import utils
import random

def switch_rvb(video : str, out_dir="", output_type="show", nb_frames=2000, iter_nb=0, fps=24):
	video = cv2.VideoCapture(video)
	ret, image = video.read()
	image_switched = np.zeros_like(image)
	frame_nb = 1
	idx = [0,1,2]
	while True:
		ret, frame = video.read()
		if not ret:
			break
		image_switched = frame
		copy_values = image_switched[:,:,idx[0]]
		image_switched[:,:,idx[0]] = image_switched[:,:,idx[1]]
		image_switched[:,:,idx[1]] = image_switched[:,:,idx[2]]
		image_switched[:,:,idx[2]] = copy_values
		movement = utils.write_or_show(frame, output_type=output_type, fps=fps)
		if not movement:
			return
		if movement == 1000:
			random.shuffle(idx)
			movement = 0
		frame_nb = frame_nb + movement
		video.set(cv2.CAP_PROP_POS_FRAMES, frame_nb)


if __name__ == '__main__':
	video = "/Users/john/Desktop/Bureauthelast/bureau1604/bureau next/Bureau le rangement arrive/Faudra ranger/Bureau nouveau/Burea/Film/VID_20211104_090832.mp4"
	switch_rvb(video, fps=0.1)