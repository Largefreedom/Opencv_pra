import sys
import  numpy as np
import cv2

# Read points from text file
def readPoints(path):
    points = []

    # Read points
    with open(path) as file:
        for line in file:
            x,y = line.split()
            points.append((int(x),int(y)))

    return points

# Apply affine transform calculated using srcTri and dstTri to src and output an image of size
def applyAffineTransform(src,srcTri,dstTri,size):

    # Givern a pair of triangles , find the affine transform.
    warpMat  = cv2.getAffineTransform(np.float32(srcTri),np.float32(dstTri))

    # Apply the Affine Tranform just found to the src image
    dst = cv2.warpAffine(src,warpMat,(size[0],size[1]),None,flags=cv2.INTER_LINEAR,borderMode = cv2.BORDER_REFLECT_101)

    return dst

# Check if point is inside a rectangle
def rectContains(rect,point):
    if(point[0] <rect[0]):
        return False
    elif point[1] <rect[1]:
        return False
    elif point[0] > rect[0] +rect[2]:
        return False
    elif point[1] >rect[1] + rect[3]:
        return False
    return True


# calculate delanauy triangles
def calculateDelaunayTriangles(rect,points):
    # create subdiv
    subdiv = cv2.Subdiv2D(rect)

    # Insert points into subdiv
    for p in points:
        subdiv.insert(p)
    triangleList = subdiv.getTriangleList()

    delaunayTri = []
    pt = []

    for t in triangleList:
        pt.append((t[0],t[1]))
        pt.append((t[2],t[3]))
        pt.append((t[4],t[5]))

        pt1 = (t[0],t[1])
        pt2 = (t[2],t[3])
        pt3 = (t[4],t[5])

        if rectContains(rect,pt1) and rectContains(rect,pt2) and rectContains(rect,pt3):
            ind = []
            # get face-points (from 68 face detxctor) by coordinats
            for j in range(3):
                for k in range(0,len(points)):
                    if(abs(pt[j][0]-points[k][0])<1.0 and abs(pt[j][1]-points[k][1])<1.0):
                        ind.append(k)

            # Three points  form a triangle array. Triangle array corresponds to the file tri.txt
            # in Face Morph:
            if len(ind) ==3:
                delaunayTri.append((ind[0],ind[1],ind[2]))

        # setting empty
        pt = []

    return delaunayTri

def warpTriangle(img1,img2,t1,t2):

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by left top corner of respective rectangles

    t1Rect =[]
    t2Rect = []
    t2RectInt = []

    for i in range(0,3):
        t1Rect.append(((t1[i][0]-r1[0]),(t1[i][1]-r1[1])))
        t2Rect.append(((t2[i][0]-r2[0]),(t2[i][1]-r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]),(t2[i][1]-r2[1])))


    # Get mask by filling triangle
    mask = np.zeros((r2[3],r2[2],3),dtype = np.float32)
    cv2.fillConvexPoly(mask,np.int32(t2RectInt),(1.0,1.0,1.0),16,0)

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1]+r1[3],r1[0]:r1[0]+r1[2]]

    size = (r2[2],r2[3])
    img2Rect = applyAffineTransform(img1Rect,t1Rect,t2Rect,size)

    img2Rect = img2Rect*mask

    # Copy triangular region of the rectangular patch to the output image

    img2[r2[1]:r2[1]+r2[3],r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3],r2[0]:r2[0]+r2[2]] *((1.0,1.0,1.0)-mask)
    img2[r2[1]:r2[1] +r2[3],r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3],r2[0]:r2[0]+r2[2]] +img2Rect


if __name__ =='__main__':
    # Make sure Opencv is version or above

    filename1 = "E:/data_ceshi/sswap/1.png"
    filename2 = "E:/data_ceshi/sswap/1.jpg"
    filename3 = "E:/data_ceshi/sswap/mask.jpg"
    filename4 = "E:/data_ceshi/sswap/combina.jpg"
    filename5 = "E:/data_ceshi/sswap/swap.jpg"

    txt_path1 = "E:/data_ceshi/sswap/pointspng.txt"
    txt_path2 = "E:/data_ceshi/sswap/pointsjpg.txt"

    img1 = cv2.imread(filename1)
    img2  = cv2.imread(filename2)
    img1Warped = np.copy(img2)

    # Read array of corresponding points
    points1 = readPoints(txt_path1)
    print(len(points1))
    points2 = readPoints(txt_path2)
    print(len(points2))
    # Find convex hull
    hull1 = []
    hull2 = []
    img_corp = img1.copy()
    hullIndex = cv2.convexHull(np.array(points2),returnPoints= False)

    # find convexHull
    hullIndex1 = cv2.convexHull(np.array(points1))
    for i in range(len(hullIndex1)):
        cv2.line(img_corp,tuple(hullIndex1[i][0]),tuple(hullIndex1[(i+1)%len(hullIndex1)][0]),(255,0,0),2)
        #cv2.circle(img_corp,i,2,(205,0,0),2)
    img_point = img1.copy()
    for i in points1:
        cv2.circle(img_point,tuple(i),2,(0,255,0),5)
    fillbox = np.hstack((img1,img_point,img_corp))
    cv2.imwrite("E:/data_ceshi/sswap/fillbox.png",fillbox)

    for i in range(0,len(hullIndex)):
        hull1.append(points1[int(hullIndex[i])])
        hull2.append(points2[int(hullIndex[i])])

    # Finde delanauy triangulation for convex hull points
    sizeImg2 = img1.shape
    rect = (0,0,sizeImg2[1],sizeImg2[0])

    dt = calculateDelaunayTriangles(rect,hull2)
    if(len(dt) == 0):
        quit()

    img2_con = img1.copy()
    # Apply affine tranformation to Delaunay triangles
    for i in range(0,len(dt)):
        t1 = []
        t2 = []

        # Get points for img1,img2 corresponding to triangles
        for j in range(0,3):
            t1.append(hull1[dt[i][j]])
            t2.append(hull2[dt[i][j]])

        for j in range(0,3):
            cv2.line(img2_con,t1[j],t1[(j+1)%3],(255,0,0),2)

        warpTriangle(img1,img1Warped,t1,t2)

    out_convex = np.hstack((img1,img2_con))
    cv2.imwrite("E:/data_ceshi/sswap/fillbox_tri.png",out_convex)
    # Calculate Mask
    hull8U = []
    for i in range(0,len(hull2)):
        hull8U.append((hull2[i][0],hull2[i][1]))

    mask = np.zeros(img2.shape,dtype = img2.dtype)
    cv2.fillConvexPoly(mask,np.int32(hull8U),(255,255,255))

    cv2.imwrite(filename3,mask)
    cv2.imwrite(filename4,img1Warped)

    r = cv2.boundingRect(np.float32([hull2]))
    center = ((r[0]+int(r[2]/2),r[1] + int(r[3]/2)))
    output = cv2.seamlessClone(np.uint8(img1Warped),img2,mask,center,cv2.NORMAL_CLONE)
    output_mask = np.hstack((img1Warped,img2,mask,output))
    cv2.imwrite("E:/data_ceshi/sswap/out_mask.png",output_mask)
    output = np.hstack((cv2.resize(img1,(img2.shape[0],img2.shape[1])),output,img2))
    cv2.imwrite(filename5,output)
    # cv2.imshow("Face swapped",output)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()











