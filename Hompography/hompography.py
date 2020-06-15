import cv2
import numpy as np
import sys


def mouse_handler(event,x,y,flags,data):
    if event ==cv2.EVENT_LBUTTONDOWN:
        cv2.circle(data['im'],(x,y),3,(0,0,255),5,16)
        cv2.namedWindow("Image",0)
        cv2.imshow("Image",data['im'])
        if len(data['points']) <4:
            data['points'].append([x,y])

def get_four_points(im):

    data = {}
    data['im'] = im.copy()
    data['points'] = []
    # Set the callback function for any mouse event
    cv2.namedWindow("Image", 0)
    cv2.imshow('Image',im)
    #请注意你标记点的数据，是顺时针，需要与pst_src 方向一致
    cv2.setMouseCallback("Image",mouse_handler,data)
    cv2.waitKey(0)
    # Convert array to np.array
    #竖直方向堆叠起来;;;
    points = np.vstack(data['points']).astype(float)
    return points


if __name__ =='__main__':

    img_src = cv2.imread("D:/first-image.jpg")
    size = img_src.shape
    # 取得四个坐标
    pst_src = np.array(
        [
            [0,0],[size[1]-1,0],
            [size[1]-1,size[0]-1],
            [0,size[0]-1]
         ],dtype=float
    )

    #Read the destination image
    img_dst = cv2.imread("D:/times-square.jpg")

    print("Click on four corners of bllboard and the press ENTER")
    four_point  = get_four_points(img_dst)

    # Calculate  Homography between  source and destination points
    h,status = cv2.findHomography(pst_src,four_point)

    im_temp = cv2.warpPerspective(img_src,h,(img_dst.shape[1],img_dst.shape[0]))

    cv2.fillConvexPoly(img_dst,four_point.astype(int),0,16)

    #add wraped source image to destination image

    img_dst = img_dst + im_temp
    cv2.namedWindow("Image", 0)
    cv2.imshow("Image",img_dst)
    cv2.waitKey(0)
