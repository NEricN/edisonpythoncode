from collections import deque
from constants.constants import *
from Queue import Queue
from serialize import Serialize
from time import sleep, time

from wiringx86 import GPIOEdison as GPIO

class motorManager():
    def __init__(self, queue_in, queue_out) :
        self.arduino = {}
        self.translations = {}
        self.gpio = GPIO(debug=false)

        self.gpio.pinMode(LEFT_WHEEL, self.gpio.OUTPUT)
        self.gpio.pinMode(RIGHT_WHEEL, self.gpio.OUTPUT)

        self.queue = deque()

        self.queue_in = queue_in

        self.is_active = True

    def emergency_stop(self) :
        self.update_port(LEFT_WHEEL, 0)
        self.update_port(RIGHT_WHEEL, 0)

    def read_inputs(self) :
        while(self.is_active) :
            Serialize.run_robot(self.queue_in.get(), self)
        print("read inputs closed")

    def run_input(self, input_string):
        Serialize.run_robot(input_string, self)

    def update_port(self, port, value) :
        self.gpio.writeAnalog(port, value)

    def shut_off(self) :
        self.emergency_stop()
        self.is_active = False

def main():
    r = motorManager(Queue(), Queue())

if __name__ == "__main__" :
    main()
