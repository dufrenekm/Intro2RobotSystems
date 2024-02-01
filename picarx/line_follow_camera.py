from time import sleep
from picamera import PiCamera
from picarx_improved import Picarx, ADC, logging, constrain
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import math
from line_following import Controller
from copy import deepcopy

class Process_Image():
    def __init__(self, dark_line = True):
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.start_preview()
        # Camera warm-up time
        sleep(1)
        cv.namedWindow("Window", cv.WINDOW_NORMAL) 
        # cv.namedWindow("th", cv.WINDOW_NORMAL) 
        pass
        
    def take_pic(self):
        self.camera.capture('pic.jpg')
        
    def grab_image(self):
        img = cv.imread('/home/kyle/Intro2RobotSystems/picarx/pic.jpg')
        
        return img

    def thresehold_img(self, img):
        def click_data(event, x, y, flags, param):

            if (event == cv.EVENT_LBUTTONDOWN):
                # print(x,' , ', y)
                font = cv.FONT_HERSHEY_SIMPLEX
                blue = img[x,y,0]
                green = img[x,y,1]
                red = img[x,y,2]
                text = str(red) + ',' + str(green) + ',' + str(blue)
                font = cv.FONT_HERSHEY_SIMPLEX
                print(text)
                # cv.putText(img,text,(x,y),font,1,(0,255,255),1,cv.LINE_AA)
                # cv.imshow('th',img)
        # lower_blue= np.array([78,158,124])
        # upper_blue = np.array([138,255,255])

        # mask = cv2.inRange(img,lower_blue,upper_blue)
        # gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
        # img_shrunk = deepcopy(img)[:,:]
        
        blurred = cv.GaussianBlur(img, (9, 9), 0)
        gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
        val, mask = cv.threshold(gray, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
                                
                                    
            # cv.imshow("th", mask)
            # # cv.setMouseCallback('th',click_data)
            # cv.waitKey(0)
        # ret,th1 = cv.threshold(gray_image,120,255,cv.THRESH_BINARY) 
        # cnts, hierarchy = cv.findContours(th1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        th1 = mask
        removed_x = np.copy(th1)[:,:]
        grey_image_shrunk = np.copy(removed_x)[:,:] #668
        
        # print("Shrunk shape", grey_image_shrunk.shape)
        
        # cv.imshow("th", grey_image_shrunk)
        
        # cv.waitKey(1)
        
        dst = cv.Canny(grey_image_shrunk, 50, 200, None, 3)
    
        # Get array slice towards bottom
        slice_dst = dst[500,:]
        # Get edges 
        new_edges = np.where(slice_dst == 255)
        
        
        # plt.subplot(121),plt.imshow(th1,cmap = 'gray')
        # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(dst,cmap = 'gray')
        # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        # plt.show()
    
        # # Copy edges to the images that will display the results in BGR
        # cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
        # # cdstP = np.copy(cdst)
        # lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
        
        
        # x_values = [0,0]
        # lookahead_pixels = 150
        # image_cap = (568, 824) # minus 1
    
        # # print(lines.shape)
        # if lines is None:
        #     return None
        # elif len(lines) == 1:
        #     return None
        # if lines is not None:
        #     for i in range(2):
        #         rho = lines[i][0][0]
        #         theta = lines[i][0][1]
        #         a = math.cos(theta)
        #         b = math.sin(theta)
        #         x0 = a * rho
        #         y0 = b * rho
        #         # print("x0 ", x0, " y0 ", y0)
        #         # print("rho ", rho)
        #         # print("theta ", theta)
        #         pt1 = (int(x0 + 100*(-b)), int(y0 + 100*(a)))
        #         pt2 = (int(x0 - 100*(-b)), int(y0 - 100*(a)))
                
        #         # cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
        #         # print(pt1)
        #         # print(pt2)
        #         if a == 0 or b == 0:
        #             return None
        #         x_values[i] = ((568-lookahead_pixels)-rho/b)*-b/a
                
        # center_point = (int(np.mean(x_values)), int(568-lookahead_pixels))
        if len(new_edges[0]) >= 2:
            center_point = (int((new_edges[0][0] +new_edges[0][1])/2.0), 500)
            cv.circle(img,center_point, 10, (0,255,255), -1)
            
            # Convert image width to scale from -1 to 1
            scaled_center = center_point[0]/(grey_image_shrunk.shape[1]/2) - 1# width of image
            # Where it passes the bottom at 823...
            
            # bottom_point = (568-rho/b)*-b/a
            # print(bottom_point)
            # cv.circle(cdst,(int(bottom_point),int(568)), 10, (0,255,255), -1)
            
            # mid_point = (500-rho/b)*-b/a
            # print(bottom_point)
            # cv.circle(cdst,(int(bottom_point),int(500)), 10, (0,255,255), -1)
            
            # cv.imshow("Window", img)
            # cv.resizeWindow("Window", 500, 500)
            # cv.waitKey(1)
        else:
            return 0
        
        
        return scaled_center
    
    def get_line_pos(self):
        self.take_pic()
        img = self.grab_image()
        location = self.thresehold_img(img)
        return location
        

if __name__ == "__main__":
    # Set up picar class
    picar = Picarx()
    logging.getLogger('matplotlib.font_manager').disabled = True
    # Point the camera servo down
    picar.set_cam_pan_angle(0)
    picar.set_cam_tilt_angle(-30)
    img = Process_Image()
    
    control = Controller(picar, 35)
    
    while True:
        inter_val = img.get_line_pos()
        if not inter_val:
            continue
        logging.debug(f"Line position: {inter_val}")
        control.update_angle(inter_val)
        picar.forward(25)
    
    