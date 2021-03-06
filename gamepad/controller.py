import pygame
import time
from constants.constants import *

from serialize import Serialize

MIN_DETECTION=.2 #to account for misc. numbers in resting state
DELAY=.5 #to avoid sending excessive info

class Controller():

    UP, DOWN, HOLD, IS_DOWN = 0, 1, 2, 3
    AXIS_FUNC, AXIS_TIME_DELAY = 0, 1
    HAT_FUNC, HAT_TIME_DELAY = 0, 1

    def __init__(self, id) :
        pygame.init()
        pygame.joystick.init()
        if not pygame.joystick.get_count() :
            self.is_active = False
            return
        self.controller = pygame.joystick.Joystick(id)
        self.controller.init()

        self.id = id

        self.num_buttons = self.controller.get_numbuttons()
        self.num_axes = self.controller.get_numaxes()
        self.num_hats = self.controller.get_numhats()

        self.button_funcs = [[[],[],[],0] for i in range(self.num_buttons)]
        self.axis_funcs = [[[], 0] for i in range(self.num_axes)]
        self.hat_funcs = [[[], 0] for i in range(self.num_hats)]

        self.is_active = True

    def bind_button_up(self, button_id, func) :
        self.button_funcs[button_id][Controller.UP].append(func)

    def bind_button_down(self, button_id, func) :
        self.button_funcs[button_id][Controller.DOWN].append(func)

    def bind_button_hold(self, button_id, func) :
        self.button_funcs[button_id][Controller.HOLD].append(func)

    def bind_axis(self, axis_id, func) :
        self.axis_funcs[axis_id][Controller.AXIS_FUNC].append(func)

    def bind_hat(self, hat_id, func) :
        self.hat_funcs[hat_id][Controller.AXIS_FUNC].append(func)

    def clear_funcs(self) :
        for i in range(self.num_buttons):
            self.button_funcs[i][Controller.UP] = []
            self.button_funcs[i][Controller.DOWN] = []
            self.button_funcs[i][Controller.HOLD] = []
            self.button_funcs[i][Controller.IS_DOWN] = 0
        for i in range(self.num_axes):
            self.axis_funcs[i][Controller.AXIS_FUNC] = []
            self.axis_funcs[i][Controller.AXIS_TIME_DELAY] = 0
        for i in range(self.num_hats):
            self.axis_funcs[i][Controller.HAT_FUNC] = []
            self.axis_funcs[i][Controller.HAT_TIME_DELAY] = 0

    def update_loop(self) :
        while(self.is_active) :
            try:
                self.update()
            except Exception as e:
                print(e)

            #time.sleep(0.001)

    def update(self) :
        for event in pygame.event.get() :
            if event.type == pygame.JOYBUTTONDOWN :
                for i in range(self.num_buttons) :
                    if self.controller.get_button(i) and not self.button_funcs[i][Controller.IS_DOWN] :
                        self.button_funcs[i][Controller.IS_DOWN] = 1
                        for f in self.button_funcs[i][Controller.DOWN] :
                            f()
                    elif self.controller.get_button(i):
                        for f in self.button_funcs[i][Controller.HOLD] :
                            f()

            elif event.type == pygame.JOYBUTTONUP :
                for i in range(self.controller.get_numbuttons()) :
                    if not self.controller.get_button(i) and self.button_funcs[i][Controller.IS_DOWN] :
                        self.button_funcs[i][Controller.IS_DOWN] = 0
                        for f in self.button_funcs[i][Controller.UP] :
                            f()

        for i in range(self.num_axes) :
            if self.axis_funcs[i][Controller.AXIS_TIME_DELAY] < time.time():
                for f in self.axis_funcs[i][Controller.AXIS_FUNC] :
                    f(self.controller.get_axis(i) if (abs(self.controller.get_axis(i)) > MIN_DETECTION) else 0)
                self.axis_funcs[i][Controller.AXIS_TIME_DELAY] = time.time() + DELAY
            
        for i in range(self.num_hats) :
            if self.hat_funcs[i][Controller.HAT_TIME_DELAY] < time.time():
                for f in self.hat_funcs[i][Controller.HAT_FUNC] :
                    f(self.controller.get_hat(i) if (self.controller.get_hat(i) != (0,0)) else (0, 0))
                self.hat_funcs[i][Controller.HAT_TIME_DELAY] = time.time() + DELAY

    def shut_off(self) :
        self.is_active = False

class RobotController(Controller) :

    def __init__(self, id, queue_out):
        #queue_out should be gui's queue_in, so gui can process with sliders
        Controller.__init__(self, id)

        self.queue_out = queue_out

    def update_loop(self):
        while(self.is_active) :
            self.update()

            #time.sleep(0.001)

    def set_edison_mode(self):
        self.clear_funcs()

        print("edison mode!")

        self.pre_values = {}
        
        self.bind_axis(L_ANALOG_Y, self.generate_motor_func(AXIS, L_ANALOG_Y, LEFT_WHEEL))
        self.bind_axis(R_ANALOG_Y, self.generate_motor_func(AXIS, R_ANALOG_Y, RIGHT_WHEEL))

    def generate_motor_func(self, type, input_id, motor_id):
        def func(magnitude) :
            if not (motor_id in self.pre_values) or magnitude != self.pre_values[motor_id] :
                self.queue_out.put(Serialize.Motor(motor_id, magnitude).dump())
                self.pre_values[motor_id] = magnitude
        return func

def main() :
    """
    Testing code. It works.
    """
    pass
    
    pygame.init()
    pygame.joystick.init()
    if(pygame.joystick.get_count()) :
        joy = pygame.joystick.Joystick(0)
        joy.init()
        print("Axes: " + str(joy.get_numaxes()))
        print("Balls: " + str(joy.get_numballs()))
        print("Buttons : " + str(joy.get_numbuttons()))
        print("Hats : " + str(joy.get_numhats()))
    t = True
    while(t) :
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                print([joy.get_button(i) for i in range(0, joy.get_numbuttons())])
                if(joy.get_button(2)) :
                    t = False
            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            if event.type == pygame.JOYAXISMOTION:
                print([joy.get_axis(i) for i in range(0, joy.get_numaxes())])

            if event.type == pygame.JOYHATMOTION:
                print([joy.get_hat(i) for i in range(0, joy.get_numhats())])
    print("exited")
    pygame.quit
if __name__ == "__main__" :
    main()
