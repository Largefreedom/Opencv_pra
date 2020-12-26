from PIL import Image
import numpy as np
import scipy
import matplotlib.colors as colors
from sklearn.cluster import DBSCAN
from math import ceil,sqrt




'''
Inputs:
    
    rgbimg: M,N,3 numpy 包含 uint(0-255) color image
    
    hueleftthr: Scalar constant to maximum  hue in  yellow-green region
    
    huerightthr: Scalar constant to maximum allowed hue in blue-purple region
    
    satthr: Scalar constant to select minimum allow saturation
    
    valthre: Scalar constant to select minimum allow value
    
    monothr: Scalar constant to select minimum allow monochrome
    
    maxpoints: Scalar constant maximum number of pixels  to forward to the DBSCAN clustering algoritm

    proxthresh: Proximity threshold to use for DBSCAN, as da fraction of the diagonal size of thre image
                接近阈值占图像对角线尺寸


Outputs:
    
    borderseg: [K,2,2] Nested list containing K pairs of x- and y- pixel values for drawimg the tree border
    
    X:  [P,2] List of pixels that passed the threshold step
    
    labels: [Q,2] List of cluster labels for points in  Xslice(see below)
    
    Xslice: [Q,2] Reduced list of pixels to be passed to DBSCAN


'''

'''实现脚本'''

def findtree(rgbimg,
             hueleftthr = 0.2,
             huerightthr = 0.95,
             satthr =0.7,
             valthr = 0.7,
             monothr = 220,
             maxpoints = 5000,
             proxthresh = 0.04):
    # 将 RGB 图像转化为 灰度图
    grayimg = np.asarray(Image.fromarray(rgbimg).convert('L'))

    # 将 rbg => hsv(float [0,1.0])
    hsvimg = colors.rgb_to_hsv(rgbimg.astype(float)/255)

    # 二值化阈值图像初始化

    binimg = np.zeros((rgbimg.shape[0],rgbimg.shape[1]))

    #1， heu < 0.2 or hue > 0.95(red or yellow)
    #2， saturated and bright both greater than 0.7
    # 满足以上条件被认为是圣诞树上的灯
    boolidx = np.logical_and(
        np.logical_and(
            np.logical_or((hsvimg[:,:,0]<hueleftthr),
            (hsvimg[:,:,0]>huerightthr)),
            (hsvimg[:,:,1]>satthr)),
            (hsvimg[:,:,2]>valthr))


    # 找到满足 hsv 标准的像素，赋值为255
    binimg[np.where(boolidx)] = 255
    # 添加像素来满足garay brightness 条件
    binimg[np.where(grayimg>monothr)] = 255

    # 用 DBSCAN 聚类算法分割这些点
    X = np.transpose(np.where(binimg==255))
    Xslice = X
    nsample = len(Xslice)

    if nsample > maxpoints:
        # 确保样本数不超过 DNSCAN 算法最大限度
        Xslice = X[range(0,nsample,int(ceil(float(nsample/maxpoints))))] # 将样本每隔几个采样一次

    # 将 DNSCAN 阈值接近像素单位，并运行 DBSCAN
    pixproxthr = proxthresh * sqrt(binimg.shape[0]**2 + binimg.shape[1]**2) # 对角巷长*proxthresh
    db = DBSCAN(eps = pixproxthr,min_samples=10).fit(Xslice) # 拟合样本
    labels = db.labels_.astype(int)

    # 寻找最大聚类
    unique_labels = set(labels)
    maxclustpt = 0

    for k in unique_labels:
        class_numbers = [index[0] for index in np.argwhere(labels==k)]
        if(len(class_numbers) > maxclustpt):
            points = Xslice[class_numbers]
            hull = scipy.spatial.ConvexHull(points) # 建立凸包
            maxclustpt = len(class_numbers)
            borderseg = [[points[simplex,0], points[simplex,1]] for simplex in hull.simplices]


    return borderseg,X,labels,Xslice
