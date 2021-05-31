import cv2
import numpy as np
import imutils

def rotate_bound(rotateImage, angle):
    #Source geeksforgeeks: https://www.geeksforgeeks.org/rotate-image-without-cutting-off-sides-using-python-opencv/
    # Taking image height and width
    imgHeight, imgWidth = rotateImage.shape[0], rotateImage.shape[1]

    # Computing the centre x,y coordinates
    # of an image
    centreY, centreX = imgHeight / 2, imgWidth / 2

    # Computing 2D rotation Matrix to rotate an image
    rotationMatrix = cv2.getRotationMatrix2D((centreX, centreY), -angle, 1.0)

    # Now will take out sin and cos values from rotationMatrix
    # Also used numpy absolute function to make positive value
    cosofRotationMatrix = np.abs(rotationMatrix[0][0])
    sinofRotationMatrix = np.abs(rotationMatrix[0][1])

    # Now will compute new height & width of
    # an image so that we can use it in
    # warpAffine function to prevent cropping of image sides
    newImageHeight = int((imgHeight * sinofRotationMatrix) +
                         (imgWidth * cosofRotationMatrix))
    newImageWidth = int((imgHeight * cosofRotationMatrix) +
                        (imgWidth * sinofRotationMatrix))

    # After computing the new height & width of an image
    # we also need to update the values of rotation matrix
    rotationMatrix[0][2] += (newImageWidth / 2) - centreX
    rotationMatrix[1][2] += (newImageHeight / 2) - centreY

    # Now, we will perform actual image rotation
    rotatingimage = cv2.warpAffine(
        rotateImage, rotationMatrix, (newImageWidth, newImageHeight))

    return rotatingimage

def evaluate_rotate_bound():
    img = cv2.imread('opencv.png')
    img2 = rotate_bound(img, -45)
    print(img.shape)
    print(img2.shape)
    cv2.namedWindow('Rotation', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('Input', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Input',img)
    cv2.imshow('Rotation', img2)
    cv2.waitKey(0)
    return img2

def transform_image(ip_img = None):
    ip_img = cv2.imread("C:\\Users\\zbn6cg\\Downloads\\IMG_2456.jpeg")
    h,w,_ = ip_img.shape
    ip_img = cv2.resize(ip_img, (int(720*w*1.0/h),720))
    gray = cv2.cvtColor(ip_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 7), 0)
    median = np.median(gray)
    sigma = 1
    lower = int(max(0, (1-sigma)*median))
    upper = int(min(255, (1+sigma)*median))
    print('lower = {}, upper = {}'.format(lower, upper))
    edged = cv2.Canny(gray, lower, upper)

    cv2.namedWindow('Edged', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Edged', edged)
    cv2.waitKey(0)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts[0], key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    cv2.drawContours(ip_img, [screenCnt], -1, (0, 255, 0), 2)
    cv2.imshow('Outline',ip_img)
    cv2.waitKey(0)

if __name__ == '__main__':
    #evaluate_rotate_bound()
    transform_image()
