import cv2
import numpy as np
from matplotlib import pyplot as plt


img1 = cv2.imread('F:/opencv_test/1.jpg')
gray2 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(gray2,cv2.COLOR_RGB2GRAY)
# Otsu ' s 二值化；
ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV +cv2.THRESH_OTSU)

plt.subplot(1,3,1),
plt.imshow(gray2),
plt.title('Original')
plt.subplot(1,3,3),
plt.imshow(thresh),
plt.title("Otsu's")


#nosing removoal迭代两次
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations = 3)


dist_transform = cv2.distanceTransform(opening,1,5)
ret,sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

sure_fg = np.uint8(sure_fg)
unknow = cv2.subtract(sure_bg,sure_fg)


plt.subplot(1,3,1),
plt.imshow(sure_bg),
plt.title('Black region\n must be background')

plt.subplot(1,3,3),
plt.imshow(unknow),
plt.title('Yellos region\n must be foregroun'),




#Marker labeling
ret,makers1 = cv2.connectedComponents(sure_fg)

#Add one to all labels so that sure background is not 0 but 1;
markers = makers1 +1

#Now mark the region of unknow with zero;
markers[unknow ==255] =0



markers3 = cv2.watershed(img1,markers)
img1[markers3 == -1] =[255,0,0]

plt.subplot(1,3,1),
plt.imshow(makers1),
plt.title('makers1')
plt.subplot(1,3,2),
plt.imshow(markers3),
plt.title('markers3')
plt.subplot(1,3,3),
plt.imshow(img1),
plt.title('img1'),
