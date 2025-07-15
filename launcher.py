import auto_edit_nonstop
import auto_edit_next
import os

def auto_edit_nonstop_launcher():
	#directory = "/Users/john/Desktop/trains30/all1080/"
	directory = "/Users/john/Desktop/trains30/all1080/shorts/"
	out_directory = "/Users/john/Desktop/crea/dev/Outputs/automontage_train/outs/"
	matched_file = "00013 VID_20250507_085726 (1).mp4"
	deb = 8
	auto_edit_nonstop.auto_edit_nonstop(directory, matched_file, deb, 6, out_directory, 4, "little_try_newshuffle", nb_threads=4)
	return

def auto_edit_next_launcher(directory, picture, duration, out_dir, out_name="", nb_threads=6):
	auto_edit_next.auto_edit_next(directory, picture, duration, out_dir, out_name, nb_threads=nb_threads)

def multiple_auto_edit_next(directory_pictures, directory_videos, duration, out_dir):
	files = os.listdir(directory_pictures)
	i = 0
	for file in files:
		print("launcher file", file)
		try:
			os.mkdir(out_dir + str(i))
		except FileExistsError as e:
			print(e)
		auto_edit_next_launcher(directory_videos, directory_pictures + file, duration, out_dir + str(i) + '/')
		i = i + 1

if __name__ == '__main__':
	directory = "/Users/john/Desktop/trains30/all1080/"
	out_dir = "/Users/john/Desktop/crea/dev/Outputs/auto_edit_next/raccord6/"
	picture = "/Users/john/Desktop/frames_train_dir/train1.png"
	auto_edit_next_launcher(directory, picture, 6, out_dir)
	#multiple_auto_edit_next(directory_pictures="/Users/john/Desktop/frames_train_dir/",
		#directory_videos="/Users/john/Desktop/trains30/all1080/",
		#duration=6,
		#out_dir="/Users/john/Desktop/crea/dev/Outputs/auto_edit_next/")