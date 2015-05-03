from gui.gui import *
from gui.KeyManager import *
from robot.command import *
from thread import *
from Queue import Queue
from gamepad.controller import RobotController
from socketEndpoint import Server, Client

from serialize import Serialize

from constants.constants import *

import sys

def main():
    """
    1 = port
    """
    control_side_out = Queue()
    control_side_in = Queue()

    try:
        conClient = Server('0.0.0.0', int(sys.argv[1]), lambda : control_side_out.get(block=True, timeout=1), control_side_in.put)
    except:
        print("Please specifiy ip address and port.")
        return

    controller_1 = RobotController(0, control_side_in)
    controller_1.set_edison_mode()

    controller_1_thread_id = start_new_thread(controller_1.update_loop, ())
    conClient.start()

    while True:
        #pass
        sleep(0.001)

    controller_1.shut_off()
    conClient.close()

    print("Command center has exited.")

if __name__ == '__main__':
    main()
