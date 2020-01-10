#import lane and car functionality
from Lane import Lane
from Car import Car

#intersection class will have an array of lanes
#lanes going toward the intersection should put the cars at the end into the intersection, not in any lane, then should be put in their lane going away from intersection
class Intersection:
    def __init__(self, lanes_to_intersection, lanes_away_from_intersection):
        #store the arrays of lanes
        self.toward_lanes = lanes_to_intersection
        self.away_lanes = lanes_away_from_intersection

        #keep an array of the cars that are in the intersection
        #have to make sure the cars that are in the intersection go into the right lanes after
        #check diagram to see which elements in the array represent where in the intersection model
        self.in_intersection = [0,0,0,0,0,0,0,0,0,0,0,0]

        #an array to store the in intersection cars
        self.iic = []

        #which phase the intersection is on 0 equals all red lights
        self.phase = 0

        #make arrays with lanes going toward the intersection for each phase
        #these phases don't have yeilding conflicts that can arise (phase 1 through 3)

        #phase1 has lanes 1,2,7 because they don't conflict
        self.phase1 = [self.toward_lanes[0],self.toward_lanes[1],self.toward_lanes[6]]

        #phase2 hase lanes 2,3,4
        self.phase2 = [self.toward_lanes[1],self.toward_lanes[2],self.toward_lanes[3]]

        #phase3 has lane 5
        self.phase3 = [self.toward_lanes[4]]

        #phase4 has lanes 6,7
        self.phase4 = [self.toward_lanes[5],self.toward_lanes[6]]

        #phase5 has lanes 3,4,6,7
        self.phase5 = [self.toward_lanes[2],self.toward_lanes[3],self.toward_lanes[5],self.toward_lanes[6]]

        #make away lanes, 1 is opposite lane 1 and 2, 2 is opposite 3 and 4, 3 is opposite 5, 4 is opposite 6 and 7
        self.away1 = self.away_lanes[0]
        self.away2 = self.away_lanes[1]
        self.away3 = self.away_lanes[2]
        self.away4 = self.away_lanes[3]

        #this approach of using the intersection to decide where the cars will go is now not in use
        #now the cars know where they will go
        # #this will decide which away lane the car will go into (away lane 1,2,3,4)
        # #have to rethink this because now cars know where to go
        # self.which_away_lane = 0

        #these are the paths from the lane to the intersection ordered by toward lanes then by left,forward,right
        #for example the first path is lane 1 going left
        #paths have numbers corresponding with where they are in the intersection
        self.paths = [[12,9,5,4,1],[12,9,5,3],[10],[6,5,4,8,11],[3,2,1],[3],[2,4,8,9,10],[2,4,8,11],[1],[7,8,9,5,3],[7,8,9,10],[11]]




    def tick_wait_time(self):
        #have all the cars increase their wait time by 1 that are in the lanes going toward the intersection
        for lane in self.toward_lanes:
            for j in range(lane.len):
            #move the car counters foward
                if lane.contents[j] != 0:
                    lane.contents[j].tick()



    #add a car to the beginning of one of the toward lanes after the toward lane is moved forward and it is checked that there isn't a car in the first spot
    def addCar(self):
        x = Car()
        if self.toward_lanes[x.origin - 1].contents[0] == 0:
            self.toward_lanes[x.origin - 1].addx(x)



    #cars still move up in lanes that have a red light, but the have to stop and wait behind each other
    def moveRedLanes(self):
        pass


    #move lane with a green light
    #gets one lane as an input
    #moves the lane forward 1 time step
    #returns a cars that has moved through the lane and is now in the intersection if the last element of the lane is a car
    #otherwise it returns a 0
    def moveLane(self, lane):
        endCar = lane.move()
        return endCar



    #move the inside of the intersection by moving the in_intersection_index of all the cars in the intersection up by 1
    #if it returns an away lane number, then the car is finished with the intersection
    def moveIntersection(self):
        for car in self.iic:
            x = car.move()
            if x != None:
                self.away_lanes[x - 1].addx(car)
                self.iic.remove(car)



    #move forward in time once
    #each move will be equal to some amount of real time (probably less than a second)
    #move all of the time counters in the cars forward once
    #starting with the non conflicting phases
    #add new cars to the intersection at the end
    #have to have a different move function which accounts for lanes that have red so can't go, but cars still come so they pile up
    #have to implement right on red
    def move(self):

        #increase the wait time of all of the cars in the toward lanes
        #need to tick cars in intersection
        self.tick_wait_time()

        #move all of the cars that are going away from the intersection
        #then move the cars that are in the intersection into the right away lanes
        for lane in self.away_lanes:
            lane.move()


        #archived
        # #put the in_intersection spots that go into the away lanes into their respective away lanes
        # self.away1.addx(self.in_intersection[2])
        # self.away2.addx(self.in_intersection[0])
        # self.away3.addx(self.in_intersection[10])
        # self.away4.addx(self.in_intersection[9])


        #move the cars in the intersection first so that the cars behind can come in
        self.moveIntersection()

        #if only lane 5 has a green light, move lane 5
        #add what comes out of lane 5 to the intersection and set the in_intersection_index of the car to 0
        if self.phase == 3:
            car = self.moveLane(self.phase3[0])
            if car != 0:
                car.iii = 0
                self.iic.append(car)

            #archived
            #this is only lane 5, which can turn into away lane 2,3,4
            #move lane 5 forward and put the end of lane 5 into the in_intersection array
            #which spot in the in_intersection array depends on which lane it will end up in

            # car = self.phase3[0].contents[self.phase3[0].len - 1]
            # self.in_intersection[self.which_away_lane] = self.phase3[0].move()

        if self.phase == 2:
            #this is lanes 2,3,4
            for i in range(3):
                car = self.moveLane(self.phase2[i])
                if car != 0:
                    car.iii = 0
                    self.iic.append(car)

            #archived
            # self.in_intersection[3] = self.phase2[0].move()
            # self.in_intersection[2] = self.phase2[1].move()
            # self.in_intersection[self.which_away_lane] = self.phase2[2].move()

        if self.phase == 1:
            #contains lanes 1,2,7
            for i in range(3):
                car = self.moveLane(self.phase3[0])
                if car != 0:
                    car.iii = 0
                    self.iic.append(car)

            # where lane 1 can go into away lane 1 or 2 and lane 2 has to go into away lane 4 and lane 7 has to go to away lane 3
            # self.in_intersection[self.which_away_lane] = self.phase1[0].move()
            # self.in_intersection[3] = self.phase1[1].move()
            # self.in_intersection[2] = self.phase1[2].move()

        if self.phase == 4:
            #contains lanes 6,7 where lane 6 can go into away lane 1 or 4 and lane 7 has to go into away lane 3
            self.in_intersection[self.which_away_lane] = self.phase4[0].move()
            self.in_intersection[2] = self.phase4[1].move()

        if self.phase == 5:
            self.in_intersection[self.which_away_lane] = self.phase5[0].move()

        self.moveRedLanes()




    #printing function to see everything in the intersection for debugging
    def print(self):
        print("Toward Lanes: ")

        for lane in self.toward_lanes:
            print(lane.contents)

        print("Away lanes: ")

        for lane in self.away_lanes:
            print(lane.contents)

        print("In the intersection: ")
        print(self.in_intersection)