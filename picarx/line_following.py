#!/usr/bin/env python3
from picarx_improved import Picarx, ADC, logging, constrain
from time import sleep
import numpy as np
class Grayscale_Sensor(object):
    LEFT = 0
    """Left Channel"""
    MIDDLE = 1
    """Middle Channel"""
    RIGHT = 2
    """Right Channel"""
    REFERENCE_DEFAULT = [1000]*3

    def __init__(self, pin0: ADC, pin1: ADC, pin2: ADC, reference: int = None):
        """
        Initialize Grayscale Module

        :param pin0: ADC object or int for channel 0
        :type pin0: robot_hat.ADC/int
        :param pin1: ADC object or int for channel 1
        :type pin1: robot_hat.ADC/int
        :param pin2: ADC object or int for channel 2
        :type pin2: robot_hat.ADC/int
        :param reference: reference voltage
        :type reference: 1*3 list, [int, int, int]
        """
        self.pins = (pin0, pin1, pin2)
        for i, pin in enumerate(self.pins):
            if not isinstance(pin, ADC):
                raise TypeError(f"pin{i} must be robot_hat.ADC")
        self._reference = self.REFERENCE_DEFAULT

    def reference(self, ref: list = None) -> list:
        """
        Get Set reference value

        :param ref: reference value, None to get reference value
        :type ref: list
        :return: reference value
        :rtype: list
        """
        if ref is not None:
            if isinstance(ref, list) and len(ref) == 3:
                self._reference = ref
            else:
                raise TypeError("ref parameter must be 1*3 list.")
        return self._reference

    def read_status(self, datas: list = None) -> list:
        """
        Read line status

        :param datas: list of grayscale datas, if None, read from sensor
        :type datas: list
        :return: list of line status, 0 for white, 1 for black
        :rtype: list
        """
        if self._reference == None:
            raise ValueError("Reference value is not set")
        if datas == None:
            datas = self.read()
        return [0 if data > self._reference[i] else 1 for i, data in enumerate(datas)]

    def read(self, channel: int = None) -> list:
        """
        read a channel or all datas

        :param channel: channel to read, leave empty to read all. 0, 1, 2 or Grayscale_Module.LEFT, Grayscale_Module.CENTER, Grayscale_Module.RIGHT 
        :type channel: int/None
        :return: list of grayscale data
        :rtype: list
        """
        if channel == None:
            return [self.pins[i].read() for i in range(3)]
        else:
            return self.pins[channel].read()

class Interpreter():
    """Interprets the greyscale sensor data and returns where the line is: 
         robot relative to the line as a value on the interval [−1,1], with positive values being to the left of the robot."""
    def __init__(self, light_sensitivity = 25, dark_sensitivity = 20, follow_dark_line = True):
        self.dark = dark_sensitivity
        self.light = light_sensitivity
        self.polarity = follow_dark_line
        self.counter = 0
        
    def return_pos(self, greyscale_value = [0, 0, 0]):
        
        # First check if we have a least one value below the thresehold and one value above, or we failed
        min_val = min(greyscale_value)
        max_val = max(greyscale_value)
        if not (min_val < self.dark) or not (max_val > self.light):
            self.counter += 1
            if self.counter > 10: 

                logging.error(f"Min/max thresehold not hit - following failed.")
                exit()
            return 0
        
        self.counter = 0
            
        # Check if the min/max is in the middle
        if self.polarity and greyscale_value.index(min(greyscale_value)) == 1:
            # Dark line, and the darkest is in the middle
            
            # Line towards the center, but we will adjust towards side based on which one is greater
            edges = [greyscale_value[0], greyscale_value[2]]
            ratio = min(edges)/max(edges)
            if greyscale_value[0] > greyscale_value[2]:
                sign = 1
            else: 
                sign = -1
            return sign * constrain(1 - ratio, -.5, .5)
        elif not self.polarity and greyscale_value.index(max(greyscale_value)) == 1:
            # light line, and the brightest is in the middle
            
            # Line towards the center, but we will adjust towards side based on which one is greater
            edges = [greyscale_value[0], greyscale_value[2]]
            ratio = min(edges)/max(edges)
            if greyscale_value[0] > greyscale_value[2]:
                sign = -1
            else: 
                sign = 1
            return sign * constrain(1 - ratio, -.5, .5)
        elif self.polarity and greyscale_value.index(min(greyscale_value)) == 2:
            # Dark line, edge to right
            
            print('This case')
            return greyscale_value[1]/greyscale_value[2]
        
        elif self.polarity and greyscale_value.index(min(greyscale_value)) == 0:
            print('That case')
            return -greyscale_value[1]/greyscale_value[0]
        elif not self.polarity and greyscale_value.index(max(greyscale_value)) == 2:
            # Dark line, edge to right
            
            print('This case')
            return greyscale_value[1]/greyscale_value[2]
        
        elif not self.polarity and greyscale_value.index(max(greyscale_value)) == 0:
            print('That case')
            return -greyscale_value[1]/greyscale_value[0]
            
class Controller():
    def __init__(self, picar: Picarx, scaling_factor = 15.0):
        self.scale_factor = scaling_factor
        
    def update_angle(self, line_pos = 0.0):
        scaled_val = self.scale_factor * line_pos
        picar.set_dir_servo_angle(scaled_val)
        return(scaled_val)
        
    
        
if __name__ == "__main__":
    # Set up picar class
    picar = Picarx()
    # Set up greyscale class for reading 
    grey_sensor = Grayscale_Sensor(ADC(Grayscale_Sensor.LEFT), ADC(Grayscale_Sensor.MIDDLE), ADC(Grayscale_Sensor.RIGHT))
    inter = Interpreter(25, 20, True)
    control = Controller(picar, 20)
    avg_read = 0
    reading = np.zeros((3,3))
    picar.forward(30)
    while True:
        # Get three readings
        for i in range(3):
            ahh = grey_sensor.read()
            print(ahh)
            reading[i, :] = ahh
            
        avg_reading = list(np.mean(reading, axis=0))
        # print(avg_reading)
        # print(reading)
        # break
        # print(sum(reading))
        
        inter_val = inter.return_pos(avg_reading)
        print(control.update_angle(inter_val))
        sleep(.05)