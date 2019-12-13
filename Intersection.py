from Lane import Lane

#intersection class will have an array of lanes
#lanes going toward the intersection should put the cars at the end into the intersection, not in any lane, then should be put in their lane going away from intersection
class Intersection:
    def __init__(self, lanes_to_intersection, lanes_away_from_intersection):
        #store the arrays of lanes
        self.toward_lanes = lanes_to_intersection
        self.away_lanes = lanes_away_from_intersection

        #which phase the intersection is on
        self.phase = 0

        #get lengths of the lanes for iteration later
        self.toward_len = len(self.toward_lanes)
        self.away_len = len(self.away_lanes)

    def move(self):
        in_intersection = []
        for i in range(self.toward_len):
            in_intersection.append(self.toward_lanes[i].move())