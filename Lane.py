#import car functionality
#actually, don't need it
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

        #make a total wait time counter for the lane
        self.wait_time = 0

        for i in range(self.len):
            self.contents.append(0)

    #now adding cars is done by intersection
    # #put a car at the start of the lane
    # def addCar(self):
    #     self.contents[0] = Car()

    #be able to add a car that was previously in the intersection into an away lane
    def addx(self, x):
        self.contents[0] = x

    #increase the lane's total wait time by one for each car in it
    def tick(self):
        for spot in self.contents:
            if spot != 0:
                self.wait_time += 1


    #function to move the lane up if there is a red light
    def moveRed(self):
        #make a copy of the contents and then reverse it so that we can loop through the beginning to the end
        _contents = self.contents.copy()
        _contents.reverse()

        for i in range(self.len):
            #loop from end of lane to begining because it was reversed
            #if there is a 0, or not a car, then keep the cars at the begining where they were with _contents[0:i]
            #then move the section of the array that had a 0 in front forward
            #have to be careful about reversing and which way the arrays are
            if _contents[i] == 0:
                #if there is no car in the last position in the lane before it goes into the intersection then we can move it normally
                if i == 0:
                    self.move()
                #if there is a car waiting at this last position then
                else:
                    needs_moving_part = _contents[i:(self.len + 1)].copy()
                    needs_moving_part.reverse()

                    needs_moving_part = self.advance(needs_moving_part)
                    needs_moving_part.reverse()

                    staying_the_same_part = _contents[0:i]

                    staying_the_same_part.extend(needs_moving_part)

                    staying_the_same_part.reverse()
                    self.contents = staying_the_same_part
                break


    #take in an array and then add a 0 at the start, move everything forward, and discard the end of the input array
    #input is an array
    #output everything moved up one spot, add a zero at the begining and discard the end of the input array
    def advance(self,array):
        #make the new array
        new_arr = []
        #start it with a 0
        new_arr.append(0)

        #the first element of the input becomes the second element of the output, the end of the input is lost
        for i in range(len(array) - 1):
            new_arr.append(array[i])

        #return the new array
        return new_arr


    #move all of the contents of the lane forward and return the end of the lane and put a 0 at the start of the lane
    def move(self):
        new_contents = []
        new_contents.append(0)
        for i in range(self.len - 1):
            new_contents.append(self.contents[i])

        end = self.contents.pop()
        self.contents = new_contents
        return end