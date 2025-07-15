import cv2
import os
import numpy as np
import random
import threading

def get_ssd(frame, poss_frame):
	return np.sum(np.square(frame.astype(np.int64) - poss_frame.astype(np.int64)))

def compute_min(filename, directory, frame, origin_file, duration, trashbin, is_max):
	global min_ssd
	global candidate_file
	global candidate_frame

	print("inside", filename, directory)
	video = cv2.VideoCapture(directory + filename)
	total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
	print("FILE " + filename + " " + str(total_frames))
	i = 0
	while total_frames - i > duration:
		ret, poss_frame = video.read()
		if not ret or frame is None or poss_frame is None:
			return
		if poss_frame.shape != frame.shape:
			return
		i = i + 1
		if i % 100 == 0:
			print("frame nb", i, filename)

		#if np.sum(poss_frame < 1000000):
		#	continue
		ssd = get_ssd(frame, poss_frame)
		with lock:
			if not is_max:
				if ssd < min_ssd:
					min_ssd = ssd
					candidate_frame = poss_frame
					candidate_file = filename
					print("New min :" + str(min_ssd), candidate_file)
			else:
				if ssd > min_ssd:
					min_ssd = ssd
					candidate_frame = poss_frame
					candidate_file = filename
					print("New max :" + str(min_ssd), candidate_file)
	video.release()

def find_min_next(directory, frame, origin_file, duration, files, trashbin, is_max, nb_threads, batch_size):
	i = 0
	while True:
		filename = files[i]
		#print(trashbin)
		#print(len(trashbin), len(files), filename)
		if filename in trashbin or origin_file in filename:
			#print("what")
			files.pop(i)
		else:
			i = i + 1
		if i >= len(files):
			break
	if batch_size != 0:
		random.shuffle(files)
		files = sorted(files[:batch_size])
	###globals
	global lock
	global candidate_frame
	global candidate_file
	global min_ssd
	lock = threading.Lock()
	candidate_frame = frame
	candidate_file = ""
	min_ssd = 0 if is_max else 1000000000000000000000000000000000000
	###globals

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
			thrthread.append(threading.Thread(target=compute_min, args=(filename, directory, frame, origin_file, duration, trashbin, is_max)))
			thrthread[j].start()
		for j in range(len(thrthread)):
			thrthread[j].join()
	print("chosen file :", candidate_file)
	return candidate_frame, candidate_file


def auto_edit_nonstop(directory: str, start_file: str, first_frame: int, duration: int, out_directory: str, batch_size = 0, out_name = "", nb_iter=100, nb_threads=6):
	total_files = sorted(os.listdir(directory))
	video = cv2.VideoCapture(directory + start_file)
	for i in range(first_frame):
		ret, frame = video.read()
	matched_frame = frame
	old_frame = np.zeros_like(matched_frame)
	matched_file = start_file
	trashbin = [matched_file]

	for j in range(nb_iter):
		print("NEW " + str(j))
		frame_count = 0
		while get_ssd(frame, matched_frame):
			ret, frame = video.read()
			frame_count = frame_count + 1
		print(trashbin)
		print(directory + matched_file + ' ' + str(frame_count / video.get(cv2.CAP_PROP_FPS)))
		for k in range(duration):
			cv2.imwrite(out_directory + out_name + str(j) +'_'+ str(k) + ".png", frame)
			ret, frame = video.read()
			if not ret:
				break
		video.release()
		if j%4 != 3:
			matched_frame, matched_file = find_min_next(directory, frame, matched_file, duration, total_files, trashbin, False, nb_threads, batch_size=batch_size)
		else:
			matched_frame, matched_file = find_min_next(directory, frame, matched_file, duration, total_files, trashbin, False, nb_threads, batch_size=batch_size)
			trashbin = []
		trashbin.append(matched_file)
		video = cv2.VideoCapture(directory + matched_file)

if __name__ == '__main__':
	directory = "/Users/john/Desktop/trains30/all1080/"
	out_directory = "/Users/john/Desktop/crea/dev/automontage_train/"
	matched_file = "00022 20241007_150829+.mp4"
	deb = 397
	auto_edit_nonstop(directory, matched_file, deb, 6, out_directory)
