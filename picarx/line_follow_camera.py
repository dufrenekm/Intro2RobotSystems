from time import sleep
from picamera import PiCamera
from picarx_improved import Picarx, ADC, logging, constrain
import cv2 as cv

class Process_Image():
    def __init__(self, dark_line = True):
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.start_preview()
        # Camera warm-up time
        sleep(2)
        
    def take_pic(self):
        self.camera.capture('pic.jpg')
        
    def grab_image(self):
        img = cv.imread('/home/kyle/Intro2RobotSystems/picarx/pic.jpg')
        gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return gray_image

    def thresehold_img(self, img):
        ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY) 
        cv.imshow("Threshold", th1)
        cv.waitKey(0)
    
    def get_line_pos(self):
        self.take_pic()
        img = self.grab_image()
        self.thresehold_img(img)
        

if __name__ == "__main__":
    # Set up picar class
    picar = Picarx()
    
    # Point the camera servo down
    picar.set_cam_pan_angle(0)
    picar.set_cam_tilt_angle(-20)
    # camera = PiCamera()
    # camera.resolution = (1024, 768)
    # camera.start_preview()
    # # Camera warm-up time
    # sleep(2)
    # camera.capture('pic.jpg')
    
    img = Process_Image()
    img.get_line_pos()
    