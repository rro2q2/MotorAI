import cv2
import numpy as np
import time
from skimage.feature import hog
from sklearn.externals import joblib

scaleFactor = 1.2
inverse = 1.0/scaleFactor
winStride = (8, 8)
winSize = (128, 64)

clf = joblib.load("pedestrian.pkl")
orig = cv2.imread('../img/p3.jpg')
img = orig.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def overlapping_area(detection_1, detection_2):
    x1_tl = detection_1[0]
    x2_tl = detection_2[0]
    x1_br = detection_1[0] + detection_1[3]
    x2_br = detection_2[0] + detection_2[3]
    y1_tl = detection_1[1]
    y2_tl = detection_2[1]
    y1_br = detection_1[1] + detection_1[4]
    y2_br = detection_2[1] + detection_2[4]
    # Calculate the overlapping Area
    x_overlap = max(0, min(x1_br, x2_br) - max(x1_tl, x2_tl))
    y_overlap = max(0, min(y1_br, y2_br) - max(y1_tl, y2_tl))
    overlap_area = x_overlap * y_overlap
    area_1 = detection_1[3] * detection_2[4]
    area_2 = detection_2[3] * detection_2[4]
    total_area = area_1 + area_2 - overlap_area
    return overlap_area / float(total_area)


def nms(detections, threshold=.5):
    print("DETECTIONS OLD", detections)
    detections = sorted(detections, key=lambda detections: detections[2], reverse=True)
    print("DETECTIONS NEW", detections)
    new_detections = []
    if len(new_detections) > 0:
        new_detections.append(detections[0])
        del detections[0]

    for index, detection in enumerate(detections):
        for new_detection in new_detections:
            print("Overlapping area", overlapping_area(detection, new_detection))
            if overlapping_area(detection, new_detection) > threshold:
                del detections[index]
                break
        else:
            new_detections.append(detection)
            del detections[index]
    return new_detections


def appendRects(i, j, conf, c, rects):
    x = int((j)*pow(scaleFactor, c))
    y = int((i)*pow(scaleFactor, c))
    w = int((64)*pow(scaleFactor, c))
    h = int((128)*pow(scaleFactor, c))
    rects.append((x, y, conf, w, h))

# Locates the bounding boxes based on the threshold level
# Returns the appended rectangles holding the bounding boxes
def locateBoundingBoxes(img):
    rects = []
    h, w = img.shape
    count = 0
    sum = 0
    while (h >= 128 and w >= 64):
        print(img.shape)
        h, w = img.shape
        horiz = w - 64
        vert = h - 128
        print(horiz, vert)
        i = 0
        while i < vert:
            j = 0
            while j < horiz:
                portion = img[i:i+winSize[0], j:j+winSize[1]]
                features = hog(portion, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm="L2")
                result = clf.predict([features])
                #print("RESULT", result)
                if int(result[0]) == 1:
                    print(result, i, j)
                    sum +=1
                    print(sum)
                    confidence = clf.decision_function([features])
                    appendRects(i, j, confidence, count, rects)
                j += winStride[1]
            i += winStride[0]
        img = cv2.resize(img, (int(w*inverse), int(h*inverse)), interpolation=cv2.INTER_AREA)
        count += 1
        print(count)
    print("This is rects")
    print(len(rects))
    return rects


def isDetected(rects):
    return


# Displays the resulting image in a before and after format
def displayImage(rects, nms_rects):
    count = 0
    for (a, b, conf, c, d) in rects:
        cv2.rectangle(orig, (a, b), (a+c, b+d), (0, 255, 0), 2)

    print("Before NMS")
    cv2.imshow("Before NMS", orig)
    cv2.waitKey(0)

    for (a, b, conf, c, d) in nms_rects:
        cv2.rectangle(img, (a, b), (a+c, b+d), (0, 255, 0), 2)
        count += 1
    print("COUNT", count)

    print("After NMS")
    cv2.imshow("After NMS", img)
    cv2.waitKey(0)


rects = locateBoundingBoxes(gray)

nms_rects = nms(rects, 0.2)

displayImage(rects, nms_rects)
