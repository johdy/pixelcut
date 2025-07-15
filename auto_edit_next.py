import cv2
import os
import numpy as np
import random
import threading

def get_ssd2(frame, poss_frame):
	return np.sum(np.square(frame.astype(np.int64) - poss_frame.astype(np.int64)))

def write_mins(filename, directory, image, duration, out_name):

	print("inside", filename, directory)
	video = cv2.VideoCapture(directory + filename)
	total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
	print("FILE " + filename + " " + str(total_frames))
	min_ssd = 1000000000000000000
	wrote = False
	i = 0
	candidate_frame = image
	while total_frames - i > duration:
		ret, poss_frame = video.read()
		if not ret or image is None or poss_frame is None:
			return
		if poss_frame.shape != image.shape:
			return
		i = i + 1
		if i % 100 == 0:
			print("frame nb", i, filename)

		#if np.sum(poss_frame < 1000000):
		#	continue
		ssd = get_ssd2(image, poss_frame)
		if ssd < min_ssd:
			min_ssd = ssd
			candidate_frame = poss_frame
			print("New min :" + str(min_ssd), filename)
	print("wrote ?", wrote)
	if not wrote:
		video.release()
		video = cv2.VideoCapture(directory + filename)
		frame_video = image
		while get_ssd2(candidate_frame, frame_video):
			ret, frame_video = video.read()
		for k in range(duration):
			print(k)
			cv2.imwrite(out_name + str(k) + '_' + filename + ".png", frame_video)
			ret, frame_video = video.read()
	video.release()


def auto_edit_next(directory: str, picture:str, duration: int, out_directory: str, out_name = "", nb_iter=100, nb_threads=6):
	files = sorted(os.listdir(directory))
	image = cv2.imread(picture)

	i = 0

	#print(len(files), files)
	#print("TRASH", trashbin)
	for i in range(int(len(files) / nb_threads) + 1):
		print("FILE NB", i)
		thrthread = []
		for j in range(nb_threads):
			print(j)
			if i * nb_threads + j >= len(files):
				break
			filename = files[i * nb_threads + j]
			thrthread.append(threading.Thread(target=write_mins, args=(filename, directory, image, duration, out_directory + out_name)))
			thrthread[j].start()
		for j in range(len(thrthread)):
			thrthread[j].join()


if __name__ == '__main__':
	directory = "/Users/john/Desktop/trains30/all1080/"
	out_directory = "/Users/john/Desktop/crea/dev/automontage_train/"
	matched_file = "00022 20241007_150829+.mp4"
	deb = 397
	automontage(directory, matched_file, deb, 6, out_directory)
