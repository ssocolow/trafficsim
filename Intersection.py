from Lane import Lane

#intersection class will have an array of lanes
#lanes going toward the intersection should put the cars at the end into the intersection, not in any lane, then should be put in their lane going away from intersection
class Intersection:
    def __init__(self, lanes_to_intersection, lanes_away_from_intersection):
        #store the arrays of lanes
        self.toward_lanes = lanes_to_intersection
        self.away_lanes = lanes_away_from_intersection

        #keep an array of the cars that are in the intersection
        #have to make sure the cars that are in the intersection go into the right lanes after
        #order them in the array so the first element goes into one lane, the second goes into another
        self.in_intersection = [0,0,0,0]

        #which phase the intersection is on
        self.phase = 0

        #make arrays with lanes going toward the intersection for each phase
        #these phases have yeilding conflicts that can arise (phase 1 through 3)

        #phase1 has lanes 1,2,5
        self.phase1 = [self.toward_lanes[0],self.toward_lanes[1],self.toward_lanes[4]]

        #phase2 hase lanes 3,4
        self.phase2 = [self.toward_lanes[2],self.toward_lanes[3]]

        #phase3 has lanes 4,6,7
        self.phase3 = [self.toward_lanes[3],self.toward_lanes[5],self.toward_lanes[6]]

        #these are the no conflict phases
        #phase4 hase lanes 6,7
        self.phase4 = [self.toward_lanes[5],self.toward_lanes[6]]

        #phase5 has lanes 1,2
        self.phase5 = [self.toward_lanes[0],self.toward_lanes[1]]

        #phase6 has lanes 3,4
        self.phase6 = [self.toward_lanes[2],self.toward_lanes[3]]

        #phase7 has lane 5
        self.phase7 = [self.toward_lanes[4]]

        #make away lanes, 1 is opposite lane 1 and 2, 2 is opposite 3 and 4, 3 is opposite 5, 4 is opposite 6 and 7
        self.away1 = self.away_lanes[0]
        self.away2 = self.away_lanes[1]
        self.away3 = self.away_lanes[2]
        self.away4 = self.away_lanes[3]

        #this will decide which away lane the car will go into (away lane 1,2,3,4)
        self.which_away_lane = 0

    #move forward in time once
    #each move will be equal to one second in real time
    #move all of the time counters in the cars forward once
    #starting with the non conflicting phases
    #add new cars to the intersection at the end
    def move(self):

        #have all the cars increase their wait time by 1 that are in the lanes going toward the intersection
        for lane in self.toward_lanes:
            for j in range(lane.len):
            #move the car counters foward
                if lane.contents[j] != 0:
                    lane.contents[j].tick()

        #move all of the cars that are going away from the intersection
        #then move the cars that are in the intersection into the right away lanes
        for lane in self.away_lanes:
            lane.move()

        #make the first element of the in_intersection array go into lane 1, the second in lane 2, ...
        self.away1.addx(self.in_intersection[0])
        self.away2.addx(self.in_intersection[1])
        self.away3.addx(self.in_intersection[2])
        self.away4.addx(self.in_intersection[3])

        #clear the intersection
        self.in_intersection = [0,0,0,0]

        if self.phase == 7:
            #this is only lane 5, which can turn into away lane 2,3,4
            #move lane 5 forward and put the end of lane 5 into the in_intersection array
            #which spot in the in_intersection array depends on which lane it will end up in
            self.in_intersection[self.which_away_lane] = self.phase7[0].move()

        if self.phase == 6:
            #this is lanes 3,4 where lane 3 has to turn into away lane 3, lane 4 can go to away lane 1 or 2
            self.in_intersection[2] = self.phase6[0].move()
            self.in_intersection[self.which_away_lane] = self.phase6[1].move()

        if self.phase == 5:
            #contains lanes 1,2 where lane 1 can go into away lane 1 or 2 and lane 2 has to go into away lane 4
            self.in_intersection[self.which_away_lane] = self.phase5[0].move()
            self.in_intersection[3] = self.phase5[1].move()

        if self.phase == 4:
            #contains lanes 6,7 where lane 6 can go into away lane 1 or 4 and lane 7 has to go into away lane 3
            self.in_intersection[self.which_away_lane] = self.phase4[0].move()
            self.in_intersection[2] = self.phase4[1].move()