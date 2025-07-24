import cv2
import numpy as np
import time
import random
from glob import glob

videos = glob("/Users/john/Desktop/videos/Batch v30/*")
random.shuffle(videos)
print(videos)
i = 1
video2 = cv2.VideoCapture(videos.pop())
while True:
	video1 = video2
	for i in range(10):
		ret, image1 = video1.read()
		cv2.imshow("Image",  image1)
		key = cv2.waitKey(25)
		if key == 27:
			cv2.destroyAllWindows()
	video2 = cv2.VideoCapture(videos.pop())
	ret, image2 = video2.read()
	j = 0
	while j < 100:
		j = j + 1
		ret, image2 = video2.read()


		which_1 = np.square((image1.astype(np.int32) - image2.astype(np.int32))) > 25
		#print(which_1.sum(), np.square((image1 - image2))>25)

		which_2 = which_1 == False
		print(which_2.sum(), which_1.sum())
		image = np.zeros_like(image1)
		print(j)
		image[which_1] + image1[which_1] + j
		image[which_2] = image2[which_2]
		cv2.imshow("Image", image)
		key = cv2.waitKey(125)
		if key == 27:
			cv2.destroyAllWindows()
	i = i + 1

