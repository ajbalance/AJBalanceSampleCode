# 6.00x Problem Set 7: Simulating robots

import math
import random

import ps7_visualize
#import pylab

# For Python 2.7:
from ps7_verify_movement27 import testRobotMovement

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleaned = []
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """

        x = pos.getX()
        y = pos.getY()

        cleanTile = (math.floor(x), math.floor(y))

        if cleanTile not in self.cleaned:
            self.cleaned.append(cleanTile) 

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """

        return (m,n) in self.cleaned
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """

        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """

        return len(self.cleaned)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """

        return Position(random.randrange(0,self.width,int=float),random.randrange(0,self.height,int=float)) 

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """

        
        x = pos.getX()
        y = pos.getY()

        return x < self.width and y < self.height and x >= 0 and y >= 0 


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = random.randrange(0,360)
        self.position = room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)   

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction    

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """

        self.setRobotPosition(self.position.getNewPosition(self.direction, self.speed))

        self.room.cleanTileAtPosition(self.position)

        raise NotImplementedError 


class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """      

        newpos = self.position.getNewPosition(self.direction, self.speed)

        if self.room.isPositionInRoom(newpos) == True:
            self.setRobotPosition(newpos)
            self.room.cleanTileAtPosition(self.position)

        else:
            self.setRobotDirection(random.randrange(0,360)) 

# Uncomment this line to see  implementation of StandardRobot 
#testRobotMovement(StandardRobot, RectangularRoom)


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """

    #master list of number of steps in each simulation
    mastersteps = []

    #for all of the trials in the number of trials

    for t in range(0,num_trials):

        #single simulation

            #create the room
            room = RectangularRoom(width, height)

            #create the set of robots
            robots = []

            #start all the robots at a position
            for r in range(1,num_robots + 1):
                robots.append(robot_type(room, speed))

            #create tile cleaned coverage and time step variable
            fractionCleaned = float(room.getNumCleanedTiles())/(float(room.getNumTiles()))
            timeStep = 0

            #while coverage is less than min_coverage
            while fractionCleaned < float(min_coverage):

                #send all of the robots to the next position and clean

                for r in robots:
                    r.updatePositionAndClean()

                #increment the time step by 1 and recalculate fractionCleaned
                timeStep += 1
                fractionCleaned = float(room.getNumCleanedTiles())/(float(room.getNumTiles()))

            #appends the number of steps taken in that simulation to master list
            mastersteps.append(timeStep)

    #return the average number of steps taken overall

    return float(sum(mastersteps)/len(mastersteps))


class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """        
       
        newpos = self.position.getNewPosition(self.direction, self.speed)

        if self.room.isPositionInRoom(newpos) == True:
            self.setRobotPosition(newpos)
            self.room.cleanTileAtPosition(self.position)
            self.setRobotDirection(random.randrange(0,360))

        else:
            self.setRobotDirection(random.randrange(0,360))
