from Car import Car

#make a lane class
class Lane:
    #length will be the number of car lengths the lane has
    #direction will be if the lane is going toward the intersection or away from it
    def __init__(self, length, direction):
        self.len = length
        #if direction is 1, the cars will be going toward the intersection, if the direction is -1, the cars will be going away from it
        self.dir = direction
        #this is an array with length equal to the length of the lane
        #it will store 0 for no car in that position and 1 for a car in that position
        self.contents = []

        for i in range(self.len):
            self.contents.append(0)

    #now adding cars is done by intersection
    # #put a car at the start of the lane
    # def addCar(self):
    #     self.contents[0] = Car()

    #be able to add a car that was previously in the intersection into an away lane
    def addx(self,x):
        self.contents[0] = x

    #move all of the contents of the lane forward and return the end of the lane and put a 0 at the start of the lane
    def move(self):
        new_contents = []
        new_contents.append(0)
        for i in range(self.len - 1):
            new_contents.append(self.contents[i])

        end = self.contents.pop()
        self.contents = new_contents
        return end