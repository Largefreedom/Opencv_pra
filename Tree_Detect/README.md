#### 检测并标记图片中的圣诞树

> 参考链接：https://stackoverflow.com/questions/20772893/how-to-detect-a-christmas-tree

#### 1，提取图片特征点(根据图像明亮度，色调，饱和度)

![Snipaste_2020-12-26_15-48-34](https://images.zeroingpython.top/img/Snipaste_2020-12-26_15-48-34.jpg)

从上图可以看到，图片中的黑点即提取到的特征点(圣诞树)，基本大致轮廓已经出来了，但会有少许噪点，见图二、图四，建筑中的灯光、地平线特征也被提取出来了，但这些不是我们所需要的，所以需要下面的一个步骤：**聚类**，来剔除这些噪点

#### 2，用 DBSCAN 算法对特征点进行聚类



![Snipaste_2020-12-26_16-29-26](https://images.zeroingpython.top/img/Snipaste_2020-12-26_16-29-26.jpg)描边扩张后效果：

![Snipaste_2020-12-26_16-19-55](https://images.zeroingpython.top/img/Snipaste_2020-12-26_16-19-55.jpg)



#### 3，对目标特征点集计算凸包，在原图上绘制



![Snipaste_2020-12-26_14-46-39](https://images.zeroingpython.top/img/Snipaste_2020-12-26_14-46-39.jpg)

---

#### 个人建议：代码结合博客食用效果更佳，博客地址：[小张Python | 专注 Python 编程！ (zeroingpython.top)](https://zeroingpython.top/)

#### 鉴于个人水平有限，如有问题可以在公众号（小张Python）后台留言：

**公众号二维码地址：**

![687474703a2f2f7777312e73696e61696d672e636e2f6c617267652f303038623852797a677931676c6b353768696b616b6a333164703068616469782e6a7067](https://images.zeroingpython.top/img/687474703a2f2f7777312e73696e61696d672e636e2f6c617267652f303038623852797a677931676c6b353768696b616b6a333164703068616469782e6a7067.jpg)
