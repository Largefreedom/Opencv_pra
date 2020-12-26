import cv2
import numpy as np

if __name__ =='__main__':

    #图片读取
    img_src = cv2.imread("D:/book2.jpg")
    position_src = np.array([[141,131],[480,159],[493,630],[64,601]],dtype = float)

    img_dst = cv2.imread("D:/book1.jpg")
    position_dst = np.array([[318,256],[543,372],[316,670],[73,473]],dtype = float)

    #计算转换矩阵
    h,status = cv2.findHomography(position_src,position_dst)

    #对图片进行仿射变换
    out_img = cv2.warpPerspective(img_src,h,(img_dst.shape[1],img_dst.shape[0]))

    #Display images;
    cv2.imshow("Source image",img_src)
    cv2.imshow("Destination Image",img_dst)
    cv2.imshow("Warped Source Image",out_img)

    cv2.waitKey(0)








