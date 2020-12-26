'''
@author:zeroing
@wx公众号：小张Python

'''

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from findtree import findtree
import os

path_dir = 'D:/ceshi_11/findtree'

path_list = [os.path.join(path_dir,str(i)) for i in os.listdir(path_dir)]


# 初始化figure size

fgsz = (16,8)

figthresh = plt.figure(figsize = fgsz,facecolor ='w')
figclust  = plt.figure(figsize = fgsz,facecolor ='w')
figcltwo = plt.figure(figsize = fgsz,facecolor = 'w')
figborder = plt.figure(figsize = fgsz,facecolor = 'w')
figorigin = plt.figure(figsize = fgsz,facecolor = 'w')


# 每张图设置一个 窗口名
figthresh.canvas.set_window_title('Thresholded HSV and Monochrome Brightness')
figclust.canvas.set_window_title('DBSCAN Clusters (Raw Pixel Output)')
figcltwo.canvas.set_window_title('DBSCAN Clusters (Slightly Dilated for Display)')
figborder.canvas.set_window_title('Trees with Borders')
figorigin.canvas.set_window_title("Original Image")


for ii,name in enumerate(path_list):
    # 打开图片
    rgbimg = np.asarray(Image.open(str(name)))

    # 运行脚本找到 bordeseg,X,Labels,Xslce
    borderseg,X,labels,Xslice = findtree(rgbimg)

    # 展示阈值分割后的图像
    axthresh =  figthresh.add_subplot(2,3,ii+1)
    axthresh.set_xticks([])
    axthresh.set_yticks([])
    binimg = np.zeros((rgbimg.shape[0],rgbimg.shape[1]))
    for v,h in X:
        binimg[v,h] = 255 # 初步筛选之后坐标点

    axthresh.imshow(binimg,interpolation = 'nearest',cmap = 'Greys')

    # Display color-coded clusters
    axclust = figclust.add_subplot(2,3,ii+1)
    axclust.set_xticks([])
    axclust.set_yticks([])
    axcltwo = figcltwo.add_subplot(2,3,ii+1)
    axcltwo.set_xticks([])
    axcltwo.set_yticks([])
    axcltwo.imshow(binimg,interpolation = 'nearest',cmap = 'Greys')

    clustimg = np.ones(rgbimg.shape)
    unique_labels = set(labels)
    # 为每个聚类生成单个颜色
    plcol = cm.rainbow_r(np.linspace(0,1,len(unique_labels)))
    print('plcol',plcol)
    for lbl,pix in zip(labels,Xslice):
        for col,unqlbl in zip(plcol,unique_labels):
            if lbl == unqlbl:
                # -1 表示无聚类成员
                if lbl == -1:
                    col = [0.0,0.0,0.0,1.0]
                for ij in range(3):
                    clustimg[pix[0],pix[1],ij] = col[ij]
            # 扩张 图像，用于更好展示
                axcltwo.plot(pix[1],pix[0],'o',markerfacecolor= col,markersize = 1,markeredgecolor = col)

    axclust.imshow(clustimg)
    axcltwo.set_xlim(0,binimg.shape[1]-1)
    axcltwo.set_ylim(binimg.shape[0],-1)

    # 在原图树边缘进行绘制

    axborder = figborder.add_subplot(2,3,ii+1)
    axborder.set_axis_off()
    axborder.imshow(rgbimg,interpolation ='nearest')
    for vseg,hseg in borderseg:
        axborder.plot(hseg,vseg,'g-',lw =3)
    axborder.set_xlim(0,binimg.shape[1]-1)
    axborder.set_ylim(binimg.shape[0],-1)


    # 保存原图
    origin_fig1 = figorigin.add_subplot(2, 3, ii + 1)
    origin_fig1.set_axis_off()
    origin_fig1.imshow(rgbimg, interpolation='nearest')
    axborder.set_xlim(0, binimg.shape[1] - 1)
    axborder.set_ylim(binimg.shape[0], -1)


    # axborder.savefig("D:/ceshi_11/findtree/final_")

    print(name,'Sucessfully find it !!!!!!!!')

plt.show()

