#import intersection functionality
from Intersection import Intersection
from Lane import Lane
from Car import Car
import time

#make the toward lanes and the away lanes
toward = []
for i in range(7):
    toward.append(Lane(10,1))

away = []
for i in range(4):
    away.append(Lane(10,-1))

#make the intersection
I = Intersection(toward, away)

#debugging
for i in range(100):
    I.addCar()

I.phase = 1

for i in range(20):
    time.sleep(1)
    I.move()
    I.print()

# for car in I.iic:
#     print(car.origin)

# I.print()
# going_to_be_removed = []
# for i in range(len(I.iic)):
#     x = I.iic[i].move()
#     print("results of being moved " + str(x))
#     if x != None:
#         I.away_lanes[x - 1].addx(I.iic[i])
#         going_to_be_removed.append(I.iic[i])

# for i in range(len(going_to_be_removed)):
#     I.iic.remove(going_to_be_removed[i])

# for car in I.iic:
#     print(car.origin)

# I.mapInIntersectionModel()

# I.print()