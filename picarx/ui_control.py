import picarx_improved 
px = picarx_improved.Picarx()
try:
    
    while True:
        user_in = input("Input a command (or e to exit): \n 1 - new steering angle \n 2 - forward \n 3 - backward \n 4 - stop \n 5 - parallel park left \n 6 - parallel park right \n 7 - k turn left \n 8 - k turn right \n")
        
        if user_in == 'e':
            break
        elif user_in == '1':
            new_angle = input(f"Enter new angle (old angle: {px.dir_current_angle}): ")
            px.set_dir_servo_angle(int(new_angle))
        elif user_in == '2':
            px.forward(50)
        elif user_in == '3':
            px.backward(50)
        elif user_in == '4':
            px.stop()
        elif user_in == '5':
            px.parallel_park_left()
        elif user_in == '6':
            px.parallel_park_right()
        elif user_in == '7':
            px.k_turn_left()
        elif user_in == '8':
            px.k_turn_right()
       
        
        

    # 
    # px.k_turn_left()
    # # px.forward(50)
    # # time.sleep(1)
    # # px.parallel_park_left()

    # px.stop()
except Exception as e:
    print(e)
    px.stop()