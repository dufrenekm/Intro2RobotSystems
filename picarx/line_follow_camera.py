from time import sleep
from picamera import PiCamera
from picarx_improved import Picarx, ADC, logging, constrain
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import math

class Process_Image():
    def __init__(self, dark_line = True):
        # self.camera = PiCamera()
        # self.camera.resolution = (1024, 768)
        # self.camera.start_preview()
        # # Camera warm-up time
        # sleep(1)
        pass
        
    def take_pic(self):
        self.camera.capture('pic.jpg')
        
    def grab_image(self):
        img = cv.imread('/home/kyle/Intro2RobotSystems/picarx/pic.jpg')
        
        return img

    def thresehold_img(self, img):
        gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret,th1 = cv.threshold(gray_image,75,255,cv.THRESH_BINARY) 
        # cnts, hierarchy = cv.findContours(th1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        print("Th1 shape: ", th1.shape)
        
        
        grey_image_shrunk = np.copy(th1)[200:,100:668]
        
        print("Shrunk shape", grey_image_shrunk.shape)
        
        
        
        dst = cv.Canny(grey_image_shrunk, 50, 200, None, 3)
    
        # Copy edges to the images that will display the results in BGR
        cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
        # cdstP = np.copy(cdst)
        lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
        
        
    
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                print("x0 ", x0, " y0 ", y0)
                print("rho ", rho)
                print("theta ", theta)
                pt1 = (int(x0 + 100*(-b)), int(y0 + 100*(a)))
                pt2 = (int(x0 - 100*(-b)), int(y0 - 100*(a)))
                cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
                print(pt1)
                print(pt2)
        
        
        
        
        cv.imshow("Source", grey_image_shrunk)
        cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
        # cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
        
        cv.waitKey()
        
        
        
        
        
        
        # # print(contours)
        # # Sort contours largest to smallest by area
        # sort_cont = sorted(cnts, key=cv.contourArea, reverse=False)
        # thres_new = cv.drawContours(img, sort_cont, 1, (0,255,0), 3)
        # c = sort_cont[1]
        # #print(f"C1: {c}")
        # epsilon = 0.1*cv.arcLength(c,True)
        # approx_cont_1 = cv.approxPolyDP(c,epsilon,True)
        # cont_1 = np.array([approx_cont_1[0][0], approx_cont_1[1][0]])
        # print(cont_1)
        
        # # edges = cv.Canny(th1,100,200)
        # # plt.subplot(121),plt.imshow(th1,cmap = 'gray')
        # # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        # # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
        # # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        # # plt.show()
        # cv.namedWindow("Threshold", cv.WINDOW_NORMAL) 
        # cv.resizeWindow("Threshold", 100, 300)
        # cv.imshow("Threshold", thres_new)
        
        # cv.waitKey(0)
    
    def get_line_pos(self):
        # self.take_pic()
        img = self.grab_image()
        self.thresehold_img(img)
        

if __name__ == "__main__":
    # Set up picar class
    picar = Picarx()
    
    # Point the camera servo down
    picar.set_cam_pan_angle(0)
    picar.set_cam_tilt_angle(-30)
    # camera = PiCamera()
    # camera.resolution = (1024, 768)
    # camera.start_preview()
    # # Camera warm-up time
    # sleep(2)
    # camera.capture('pic.jpg')
    
    img = Process_Image()
    img.get_line_pos()
    