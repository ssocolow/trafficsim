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

        #phase0 is all red lights
        #for the purpose of the simulation, a yellow light is the same as a red light, aka cars don't enter the intersection
        self.phase0 = []

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

        self.phases = [self.phase0,self.phase1,self.phase2,self.phase3,self.phase4,self.phase5]

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
    #do right on red if the car can make it
    def moveRedLanes(self):
        #first check if there is a car in the last position of the lane which means that it has waited
        for lane in self.toward_lanes:
            if lane not in self.phases[self.phase]:
                if lane.contents[lane.len-1] != 0:
                    lane.contents[lane.len-1].has_waited = True

        #loop over all of the lanes that don't have a green light
        for lane in self.toward_lanes:
            if lane not in self.phases[self.phase]:
                lane.moveRed()




    #right on red functionality which checks if there is a car in the spot where the car in the red lane wants to be in the intersection
    #if there is no car there, then the car can safely move from the red lane to that spot in the intersection if it wants to go right

    #car has to stop before doing a right on red
    #in order to accomplish this, the car class will have a has_waited variable that will default to false and
    #will be changed to true after it sits in the last spot of a red lane once
    def rightOnRed(self):
        #loop through all of the red lanes
        for lane in self.toward_lanes:
            if lane not in self.phases[self.phase]:
                if (lane.contents[lane.len - 1] != 0):
                    if (lane.contents[lane.len - 1].movement == "right") and (lane.contents[lane.len - 1].has_waited):
                        #if there is a car going right and has waited in the last position of the red lane
                        car = lane.contents[lane.len - 1]
                        if self.okForRight(car):
                            #checks there is no car where the right on red person wants to go
                            car.startIntersectionMove()
                            self.iic.append(car)
                            lane.contents[lane.len - 1] = 0


    #checks there is no car where the right on red person wants to go
    def okForRight(self, car):
        self.mapInIntersectionModel()
        if car.away == 1:
            if self.in_intersection[2] == 0:
                return True
            else:
                return False
        if car.away == 2:
            if self.in_intersection[0] == 0:
                return True
            else:
                return False
        if car.away == 3:
            if self.in_intersection[11] == 0:
                return True
            else:
                return False
        if car.away == 4:
            if self.in_intersection[10] == 0:
                return True
            else:
                return False


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
        #have to make an array to store the cars that are going to be removed from self.iic because if we remove it during the for loop
        #then the array it is looping over will shrink by 1 and mess it up
        going_to_be_removed = []
        for car in self.iic:
            x = car.move()
            if x != None:
                self.away_lanes[x - 1].addx(car)
                going_to_be_removed.append(car)

        for car in going_to_be_removed:
            self.iic.remove(car)



    #map the locations of the cars in the intersection to the model of the intersection for visualization
    #put the cars in the right spots in the in_intersection array
    def mapInIntersectionModel(self):
            self.in_intersection = [0,0,0,0,0,0,0,0,0,0,0,0]
            for car in self.iic:
                #car is still in the intersection
                self.in_intersection[car.loc - 1] = car



    #functionality to move the lanes that have a green light
    #decide what to do based on which phase in on
    #move the lane that has the green light forward, then if it returns a car, put it into the in_intersection_cars array and set its in_intersection_index to 0
    #the in_intersection_index tells the car where it is on its path through the intersection (refrence moveIntersection())
    def moveGreenLanes(self):

        #if only lane 5 has a green light, move lane 5
        #add what comes out of lane 5 to the intersection and set the in_intersection_index of the car to 0
        if self.phase == 3:
            car = self.moveLane(self.phase3[0])
            if car != 0:
                car.startIntersectionMove()
                self.iic.append(car)


        if self.phase == 2:
            #this is lanes 2,3,4
            for i in range(3):
                car = self.moveLane(self.phase2[i])
                if car != 0:
                    car.startIntersectionMove()
                    self.iic.append(car)


        if self.phase == 1:
            #contains lanes 1,2,7
            for i in range(3):
                car = self.moveLane(self.phase1[i])
                if car != 0:
                    car.startIntersectionMove()
                    self.iic.append(car)


        if self.phase == 4:
            #contains lanes 6,7
            for i in range(2):
                car = self.moveLane(self.phase4[i])
                if car != 0:
                    car.startIntersectionMove()
                    self.iic.append(car)


        #this phase is the only yielding phase
        #lanes 3,4,6,7
        if self.phase == 5:
            #first, the lanes that don't have to worry about yielding go (4 and 7)
            car = self.moveLane(self.phase5[1])
            if car != 0:
                car.startIntersectionMove()
                self.iic.append(car)
            car = self.moveLane(self.phase5[3])
            if car != 0:
                car.startIntersectionMove()
                self.iic.append(car)

            #then check if 6 has a car that wants to do a left in the last position
            #if it doesn't, move the lane normally
            if self.phase5[2].contents[self.phase5[2].len - 1] == 0 or self.phase5[2].contents[self.phase5[2].len - 1].movement != 'left':
                car = self.moveLane(self.phase5[2])
                if car != 0:
                    car.startIntersectionMove()
                    self.iic.append(car)


            #if it does, check if it can take the full left safely and if it can move it, else do a move red lane
            #it can only take the full left safely if the third last (index 7 with a 10 length lane) spot of lane 3 is clear and
            #if the 5th last spot (index 5 with a 10 length lane) is clear
            #if it is waiting more than 10 steps, it will change to go forward
            else:
                if self.phase5[0].contents[self.phase5[0].len - 3] == 0 and self.phase5[1].contents[self.phase5[1].len - 5] == 0:
                    car = self.moveLane(self.phase5[2])
                    if car != 0:
                        car.startIntersectionMove()
                        self.iic.append(car)
                else:
                    self.phase5[2].contents[self.phase5[2].len - 1].yield_waiting_bool = True
                    self.phase5[2].moveRed()
                    #if it has been waiting too long, make it go forward
                    if self.phase5[2].contents[self.phase5[2].len - 1].yielding_time > 10:
                        self.phase5[2].contents[self.phase5[2].len - 1].tooLongWaiting()


            #now just need to do the same with lane 3 which is the left only lane
            #it can go if the second last element in lane 6 is 0 and if the fourth last element of lane 7 is 0
            if self.phase5[2].contents[self.phase5[2].len - 2] == 0 and self.phase5[3].contents[self.phase5[3].len - 4] == 0:
                car = self.moveLane(self.phase5[0])
                if car != 0:
                    car.startIntersectionMove()
                    self.iic.append(car)
            else:
                self.phase5[0].moveRed()



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

        #move the lanes that have a green light
        self.moveGreenLanes()

        #do right on red if the car can make it through the intersection without hitting anyone
        self.rightOnRed()

        #move all the cars in the lanes that have red lights forward until they stack
        self.moveRedLanes()

        #add primative or basic visualization of where the cars are in the intersection model by updating the in_intersection array
        self.mapInIntersectionModel()

	
    #a way to get information about the intersection for the visualizer
    #returns an array with arrays of the contents of all the lanes and the in_intersection
    def getInfoArrays(self):
		to = []
		for lane in self.toward_lanes:
			to.append(lane.contents)
		away = []
		for lane in self.away_lanes:
			away.append(lane.contents)
		_in = self.in_intersection.copy()
		return [to,_in,away]


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
