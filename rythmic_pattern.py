import cv2
import numpy as np
import utils

def rythmic_pattern(videos_names: list, pattern: list, out_dir="", output_type="show", nb_frames=2000, iter_nb=0, fps=10):
	videos = []
	for video_name in videos_names:
		videos.append(cv2.VideoCapture(video_name))
	ret, frame = videos[0].read()
	i = 0
	
	while i < nb_frames:
		frame = np.zeros_like(frame)
		nb_sound = 0
		k = 0
		while k < len(pattern):
			patt_len = len(pattern[k])
			if pattern[k][i % patt_len]:
				ret, intermediate_frame = videos[k].read()
				nb_sound = nb_sound + 1
				frame = frame + intermediate_frame.astype(np.int32)
			k = k + 1
			if not ret:
				break
			#frame = mean_frame(intermediate_frame, intermediate_frame)
		if not ret:
			break
		#if nb_sound:
			frame = (frame / nb_sound)
		frame = frame.astype(np.uint8)
		utils.write_or_show(frame=frame, output_type=output_type, filename=f"{i:04d}.png", fps=fps, iter_nb=iter_nb, verbose=False)
		i = i + 1



if __name__ == '__main__':
	vid2 = "/Users/john/Desktop/Bureauthelast/bureau1604/bureau next/Bureau le rangement arrive/Faudra ranger/Bureau nouveau/Burea/Film/VID_20211103_174347.mp4"
	vid1 = "/Users/john/Desktop/Bureauthelast/bureau1604/bureau next/Bureau le rangement arrive/Faudra ranger/Bureau nouveau/Burea/Film/VID_20211102_153646.mp4"
	pattern1 = [True, False, False, False, True, False, False, False]
	pattern2 = [True, False, False, True, False, False, True, False]
	rythmic_pattern([vid1, vid2], [pattern1], nb_frames=100, iter_nb=0)
	rythmic_pattern([vid1, vid2], [pattern1, pattern2], nb_frames=100, iter_nb=1)

