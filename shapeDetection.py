from win32api import GetSystemMetrics
import numpy as np
import cv2
from scipy.interpolate import splprep, splev

# the maximum width/height of a table
MAX_TABLE_DIMENSION = 15

#resize image to fit on the screen
def get_resized_for_display_img(img):
    screen_w, screen_h = GetSystemMetrics(0), GetSystemMetrics(1)
    #print("screen size", screen_w, screen_h)
    if(len(img.shape) == 2) :
        h, w = img.shape
    else: 
        h, w, _ = img.shape
    # img get w of screen and adapt h
    h = h * (screen_w / w)
    w = screen_w
    if h > screen_h:  # if img h still too big
        # img get h of screen and adapt w
        w = w * (screen_h / h)
        h = screen_h
    w, h = w*0.9, h*0.9  # because you don't want it to be that big, right ?
    w, h = int(w), int(h)  # you need int for the cv2.resize
    return cv2.resize(img, (w, h))


def detectCircles(image, displayImage = False):
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect circles in the image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 40, param1=50, param2=40, minRadius=55, maxRadius=120)
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for idx, (x, y, r) in enumerate(circles):
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5),(x + 5, y + 5), (0, 128, 255), -1)
            cv2.putText(output, str(idx), (x - 7, y - 7), cv2.FONT_HERSHEY_SIMPLEX, 1, (60,60,60), 2, cv2.LINE_AA )
            #print("x: %d\ty: %d\tr: %d" % (x, y, r))
        # show the output image
        if(displayImage):
            cv2.imshow("output", get_resized_for_display_img(np.hstack([image, output])))
            cv2.waitKey(0)
        return circles

def detectGrid(image):
    print("detecting grid")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh1 = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    contours1, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    c = 0
    for i in contours1:
        area = cv2.contourArea(i)
        if area > 1000:
                if area > max_area:
                    max_area = area
                    best_cnt = i
                    image = cv2.drawContours(image, contours1, c, (0, 255, 0), 3)
        c+=1
    #best_cnt = smoothContour(best_cnt)
    mask = np.zeros((gray.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)
    
    # mask out parts of the screen that are not the grid    
    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]
    
    #detect circles inside the grid part only
    bit_and = cv2.bitwise_and(cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) , image)
    circles = detectCircles(bit_and)
    # blot out the circles
    if (circles is not None):
        for (x,y,r) in circles:
            cv2.circle(out, (x, y), r+4, (0, 0, 0), -1)
    else:
        print("No circles found!! fatal error!")
    
    blur = cv2.GaussianBlur(out, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #calculate minimum area of a cell
    minarea = np.square(image.shape[0]/MAX_TABLE_DIMENSION)
    a = 0
    for c, i in enumerate(contours):
        area = cv2.contourArea(i)
        if area > max_area:
            gameboard = c
            print("found board @ %i" % (hierarchy[gameboard, c, 3]))
        if hierarchy[gameboard, c,3] == 1:
            a = a+1
            if area > minarea/2:
                p = int(np.abs(155 - np.abs(hierarchy[gameboard, c,3])))
                cv2.drawContours(image, contours, c, (p, 255, p), 3)
    
    print(a)

    cv2.imshow("thresholds", get_resized_for_display_img(thresh))
    #cv2.imshow("mask", mask)
    cv2.imshow("New image", get_resized_for_display_img(out))
    cv2.imshow("Anded Color", get_resized_for_display_img(bit_and))
    #cv2.imshow("blur1", blur)
    #cv2.imshow("thresh1", thresh)
    cv2.imshow("Final Image", get_resized_for_display_img(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()