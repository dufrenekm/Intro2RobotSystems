from time import sleep
from picamera import PiCamera
from picarx_improved import Picarx, ADC, logging, constrain
import cv2 as cv
# from matplotlib import pyplot as plt
import numpy as np
import math
from line_following import Controller

class Process_Image():
    def __init__(self, dark_line = True):
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.start_preview()
        # Camera warm-up time
        sleep(1)
        cv.namedWindow("Window", cv.WINDOW_NORMAL) 
        cv.namedWindow("th", cv.WINDOW_NORMAL) 
        pass
        
    def take_pic(self):
        self.camera.capture('pic.jpg')
        
    def grab_image(self):
        img = cv.imread('/home/kyle/Intro2RobotSystems/picarx/pic.jpg')
        
        return img

    def thresehold_img(self, img):
        gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret,th1 = cv.threshold(gray_image,100,255,cv.THRESH_BINARY) 
        # cnts, hierarchy = cv.findContours(th1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        
        removed_x = np.copy(th1)[:,:]
        grey_image_shrunk = np.copy(removed_x)[:,100:924] #668
        
        # print("Shrunk shape", grey_image_shrunk.shape)
        
        cv.imshow("th", grey_image_shrunk)
        
        cv.waitKey(1)
        
        dst = cv.Canny(grey_image_shrunk, 50, 200, None, 3)
    
        # Copy edges to the images that will display the results in BGR
        cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
        # cdstP = np.copy(cdst)
        lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
        
        
        x_values = [0,0]
        lookahead_pixels = 150
        image_cap = (568, 824) # minus 1
    
        # print(lines.shape)
        if lines is None:
            return None
        elif len(lines) == 1:
            return None
        if lines is not None:
            for i in range(2):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                # print("x0 ", x0, " y0 ", y0)
                # print("rho ", rho)
                # print("theta ", theta)
                pt1 = (int(x0 + 100*(-b)), int(y0 + 100*(a)))
                pt2 = (int(x0 - 100*(-b)), int(y0 - 100*(a)))
                
                # cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
                # print(pt1)
                # print(pt2)
                if a == 0 or b == 0:
                    return None
                x_values[i] = ((568-lookahead_pixels)-rho/b)*-b/a
                
        center_point = (int(np.mean(x_values)), int(568-lookahead_pixels))
        print("X vals: ", x_values)
        print("Average: ", center_point)
        cv.circle(cdst,center_point, 10, (0,255,255), -1)
        
        # Convert image width to scale from -1 to 1
        scaled_center = center_point[0]/(grey_image_shrunk.shape[1]/2) - 1# width of image
        print("Scaled center: ",scaled_center)
        # Where it passes the bottom at 823...
        
        # bottom_point = (568-rho/b)*-b/a
        # print(bottom_point)
        # cv.circle(cdst,(int(bottom_point),int(568)), 10, (0,255,255), -1)
        
        # mid_point = (500-rho/b)*-b/a
        # print(bottom_point)
        # cv.circle(cdst,(int(bottom_point),int(500)), 10, (0,255,255), -1)
        
        cv.imshow("Window", cdst)
        
        cv.waitKey(1)
        
        
        return scaled_center
        
        
        
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
        self.take_pic()
        img = self.grab_image()
        location = self.thresehold_img(img)
        return location
        

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
    
    control = Controller(picar, 20)
    picar.forward(25)
    while True:
        inter_val = img.get_line_pos()
        if not inter_val:
            continue
        logging.debug(f"Line position: {inter_val}")
        control.update_angle(inter_val)
    
    