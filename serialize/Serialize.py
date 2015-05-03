"""Command pattern implementation for robot actions"""

import pickle

from Queue import Queue

def run_robot(pickled, robot):
    try:
        pickle.loads(pickled).run_robot(robot)
    except Exception as ex:
        print(ex)

def run_gui(pickled, gui):
    pickle.loads(pickled).run_gui(gui)

def unpickle(pickled):
    return pickle.loads(pickled)
    

class Command():
    def __init__(self, *args):
        self.args = args

    def run_robot(self, robot):
        pass

    def run_gui(self, gui):
        pass
        
    def dump(self):
        return pickle.dumps(self)

class Motor(Command):
    def __init__(self, number, speed):
        self.number = number
        self.speed = speed

    def run_robot(self, robot):
        #print("Command received! Attempting to write to arduino")
        robot.update_port(self.number, self.speed)
        #print("Command sent to arduino!")
        robot.queue_out.put(self.dump())
        #print("Shit sent back! Success!")
        
    def run_gui(self, gui):
        if gui:
            #gui.output("Motor " + str(self.number) + " set to " + "{0:.2f}".format(self.speed))
            #gui.update_readout(self.number, self.speed)
            print("Motor " + str(self.number) + " set to " + "{0:.2f}".format(self.speed))
        
if __name__ == "__main__":
    # command is created from the user side
    a = Queue()
    b = Queue()
    a.put(Turn(100).dump())
    b.put(a.get())

    run_robot(b.get(), None)
