import cv2
import numpy as np
import wx
import copy
class ImageFilters():
    def __init__(self, input = None):
        self.input = input
        self.filter = ''

    def mono(self, input = None):
        if input is None:
            input = wx.Image('C:\\Users\\zbn6cg\\Downloads\\pic_ravi.jpeg', wx.BITMAP_TYPE_ANY)
        #cv2.namedWindow('Input image', cv2.WINDOW_AUTOSIZE)
        (w,h) = input.GetSize()
        print(input.GetSize())
        buf = input.GetData()
        print(type(buf))
        arr = np.frombuffer(buf, dtype='uint8', count=-1, offset=0)
        img = np.reshape(arr, (h, w, 3))

        if w > h:
            r = 1.0*w/h
            newW = 320
            newH = int(newW/r)
        else:
            r = 1.0*w/h
            newH = 240
            newW = int(newH*r)

        img2 = cv2.resize(img, (newW,newH), cv2.INTER_AREA)
        img3 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
        print(img3.shape)
        #img2 = np.resize(img, (640,480,3))
        #print(max(arr))
        '''while True:
            cv2.imshow('Input image', img)
            k = cv2.waitKey(1)
            if k%256 == 27:
                cv2.destroyAllWindows()
                break'''
        return cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)


if __name__ == '__main__':
    app = ImageFilters()
    app.mono()

