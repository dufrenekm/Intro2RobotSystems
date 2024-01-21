import picarx_improved
import time

def check_steering_calibration(picar):
    # Was -10
    print("Old calibration value: ", picar.dir_cali_val)
    while True:
        # Loop through, get user input and update value until done
        picar.forward(50)
        time.sleep(1)
        picar.stop()
        time.sleep(.2)
        picar.backward(50)
        time.sleep(1)
        picar.stop()
        user_in = input("Enter a new value (or e to exit). Old val: %d   : "%float(picar.config_flie.get("picarx_dir_servo", default_value=0)))
        if user_in == 'e':
            break
        else:
            user_in_int = int(user_in)
            picar.config_flie.set("picarx_dir_servo", "%s"%user_in_int)
            picar.dir_servo_pin.angle(user_in_int)

px = picarx_improved.Picarx()
check_steering_calibration(px)
