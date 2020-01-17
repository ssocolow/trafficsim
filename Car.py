import random

class Car:
    def __init__(self):
        #store wait time
        self.wait_time = 0

        #location in the intersection 1 corresponds with the in intersection location 1
        #can be 1 through 12 inclusive
        self.loc = 0

        #these are all the paths through the intersection ordered by toward lanes then by left,forward,right
        #for example the first path is lane 1 going left
        #paths have numbers corresponding with where they are in the intersection model
        self.paths = [[12,9,5,4,1],[12,9,5,3],[10],[6,5,4,8,11],[3,2,1],[3],[2,4,8,9,10],[2,4,8,11],[1],[7,8,9,5,3],[7,8,9,10],[11]]

        #the car will know its path based on where it spawns and where it is going
        self.path = 0

        #store the index of where it is in its path through the intersection (the in intersection index)
        #when it is -1, it is not in the intersection
        #when it is 0, it is in the first position in its path through the intersection
        self.iii = -1

        #store the path index of the car that corresponds with the paths through the intersection
        self.path_index = -1

        #store origin lane picker
        p = random.randint(1,100)

        #store away lane picker
        a = random.randint(1,100)

        self.origin = 0
        self.away = 0

        #calculate the origin lane and the respective away lane from the data
        if p <= 24:
            self.origin = 1
            if a <= 20:
                self.away = 1
                self.path_index = 1
            else:
                self.away = 2
                self.path_index = 0
        elif p <= 38:
            self.origin = 2
            self.away = 4
            self.path_index = 2
        #keep implementing path
        elif p <= 49:
            self.origin = 3
            self.away = 3
            self.path_index = 3
        elif p <= 69:
            self.origin = 4
            if a <= 20:
                self.away = 1
                self.path_index = 5
            else:
                self.away = 2
                self.path_index = 4
        elif p <= 72:
            self.origin = 5
            if a <= 31:
                self.away = 2
                self.path_index = 8
            elif a <= 56:
                self.away = 3
                self.path_index = 7
            elif a <= 100:
                self.away = 4
                self.path_index = 6
        elif p <= 93:
            self.origin = 6
            if a <= 16:
                self.away = 1
                self.path_index = 9
            elif a <= 100:
                self.away = 4
                self.path_index = 10
        elif p <= 100:
            self.origin = 7
            self.away = 3
            self.path_index = 11

        #make an array with the numbers that correspond with how the car moves through the intersection
        self.path = self.paths[self.path_index]

        #store the length of the path (how many spots the car goes through when in the intersection) minus 1 so it can be checked against the index
        #the maximum value that self.iii can be is this
        self.path_len = len(self.path) - 1



    #function to increase wait time
    def tick(self):
        self.wait_time += 1

    #initialize the car for its path through the intersection by setting the iii to 0 and the self.loc to the right number
    def startIntersectionMove(self):
        self.iii = 0
        self.loc = self.path[self.iii]

    #moves the car through the intersection non conflicting/yielding
    #first set the self.iii to 0
    def move(self):
        if self.iii < self.path_len:
            self.iii += 1
            self.loc = self.path[self.iii]
        else:
            #add the car to the right away lane
            #in the intersection class this returns the away lane it should be moved to
            return self.away