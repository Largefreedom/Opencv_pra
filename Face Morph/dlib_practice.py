import sys
import dlib
import cv2




predictor_path  = "E:/data_ceshi/shape_predictor_68_face_landmarks.dat"
png_path = "E:/data_ceshi/sswap/1.png"

txt_path = "E:/data_ceshi/sswap/pointspng.txt"
f = open(txt_path,'w+')


detector = dlib.get_frontal_face_detector()
#相撞
predicator = dlib.shape_predictor(predictor_path)
win = dlib.image_window()
img1 = cv2.imread(png_path)


# img =  dlib.load_rgb_image(png_path)
# win.clear_overlay()
# win.set_image(img1)

dets = detector(img1,1)
print("Number of faces detected : {}".format(len(dets)))
for k,d in enumerate(dets):
    print("Detection {}  left:{}  Top: {} Right {}  Bottom {}".format(
        k,d.left(),d.top(),d.right(),d.bottom()
    ))
    lanmarks = [[p.x,p.y] for p in predicator(img1,d).parts()]
    for idx,point in enumerate(lanmarks):
        f.write(str(point[0]))
        f.write("\t")
        f.write(str(point[1]))
        f.write('\n')
        point = (point[0],point[1])
        cv2.circle(img1,point,5,color=(0,0,255))
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cv2.putText(img1,str(idx),point,font,0.5,(0,255,0),1,cv2.LINE_AA)
        #对标记点进行递归；

    # shape = predicator(img,d)
    # #Get the landmarks/parts for face in box d
    # print("Part 0：{}，Part 1 :{}".format(shape.part(0),shape.part(1)))
    # win.add_overlay(shape)
    # for i in range(68):
    #     print(shape.part(i))
f.close()
cv2.namedWindow("img",cv2.WINDOW_NORMAL)
cv2.imshow("img",img1)
cv2.waitKey(0)
# win.add_overlay(dets)

dlib.hit_enter_to_continue()




# files = ["E:/"+str(i) for i in os.listdir("E:/") if str(i).endswith('.png')]
# for f in files:
#     img = dlib.load_rgb_image(f)
#     # img = cv2.imread(f,cv2.COLOR_BGR2RGB)
#     # 1对 图像进行代表上采样1词，上采样次数越大，即最终人脸识别效果更好一点
#     dets,score,idx = detector.run(img,1,-1)
#
#     print("Number of faces delected : {}".format(len(dets)))
#
#     for index,face in enumerate(dets):
#         print("face:{},left {},top {}, right : {}，bottom: {}".format(index,face.left(),
#                                                                      face.top(),face.right(),face.bottom()))
#         left = face.left()
#         top = face.top()
#         right = face.right()
#         bottom = face.bottom()
#
#         #绘制脸框
#         cv2.rectangle(img,(left,top),(right,bottom),(23,255,25),3)
#
#         cv2.namedWindow(f,cv2.WINDOW_AUTOSIZE)
#         cv2.imshow(f,img)
#     print(score)
#
#     win.clear_overlay()
#     win.set_image(img)
#     win.add_overlay(dets)
#     dlib.hit_enter_to_continue
#
#
# k = cv2.waitKey(0)
# cv2.destroyAllWindows()
