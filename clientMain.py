from robot.command import *
from thread import *
from Queue import Queue
from socketEndpoint import Server, Client

from serialize import Serialize

import sys

"""
    1 is ip
    2 argument is port
"""

def main():
    robot_side_out = Queue()
    robot_side_in = Queue()

    r = motorManager(robot_side_in, robot_side_out)

    while True:
        r.is_active = True
        try:
            #print("Trying to connect...")
            robServer = Client(sys.argv[1], int(sys.argv[2]), lambda : robot_side_out.get(block=True, timeout=1), r.run_input, r.shut_off)
            r.is_active = True
        except:
            #print("Connection failed.")
            #print("Trying to reconnect...")
            continue

        #c = start_new_thread(r.read_inputs, ())

        robServer.start()

        while(robServer.isOn):
            pass
            sleep(0.0001)

    try:
            r.shut_off()
            robServer.close()
    except Exception as e:
            print(e)

    r.emergency_stop()

if __name__ == '__main__':
    main();
