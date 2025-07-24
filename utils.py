import cv2
import numpy as np

def mean_frame(frame1, frame2):
	mean_frame = (frame1.astype(np.int16) + frame1.astype(np.int16)) / 2
	mean_frame = mean_frame.astype(np.uint8)
	return mean_frame

def treat_key(key: int) -> int:
	if key == 2:
		return -1
	elif key == 27:
		return 0
	elif key == 32:
		return 1000
	elif key == 122:
		return 1, 0
	elif key == 113:
		return 0, -1
	elif key == 115:
		return -1, 0
	elif key == 100:
		return 0, 1
	return 1

def write_or_show(frame, output_type="show", out_dir="/Users/john/Desktop/crea/dev/Outputs/dump/", filename="img.png", fps=24, iter_nb="0", verbose=False) -> int:
	if output_type == "show":
		if verbose:
			print(f"Showing frame. frame_sum = {np.sum(frame)}")
		cv2.imshow("Image",  frame)
		key = cv2.waitKey(int(1000/fps))
		if key == 13:
			print(f"Writing file {filename} at {out_dir}. frame_sum = {np.sum(frame)}")
			cv2.imwrite(out_dir + iter_nb + '_' + filename, frame)
		print(key)
		return treat_key(key)
	if verbose:
		print(f"Writing file {filename} at {out_dir}. frame_sum = {np.sum(frame)}")
	if output_type == "write":
		cv2.imwrite(out_dir + iter_nb + '_' + filename, frame)
	else:
		print("error: Wrong output type.")
	return 1

def select_frame(video, frame_nb=0):
	while True:
		video.set(cv2.CAP_PROP_POS_FRAMES, frame_nb - 1)
		ret, frame = video.read()
		cv2.imshow("Image", frame)
		key = cv2.waitKey(0)
		print(key)
		if key == 3:
			frame_nb = frame_nb + 1
		if key == 2:
			frame_nb = frame_nb - 1
		if key == 27:
			return frame_nb



