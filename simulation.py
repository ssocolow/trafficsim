#import intersection functionality
from Intersection import Intersection
from Lane import Lane
from Car import Car
#import time functionality
import time
#import neural network functionality
#import nn
#import visualization functionality
import showsim
import led_test

#make the toward lanes and the away lanes
toward = []
for i in range(7):
    toward.append(Lane(10,1))

away = []
for i in range(4):
    away.append(Lane(10,-1))

#make the intersection
I = Intersection(toward, away)

#make the neural networks
#nets = []
#
#for i in range(100):
#	nets.append(nn.NeuralNetwork([71],[5],[5],[5]))

#debugging
#for i in range(100):
#    I.addCar()

I.phase = 0
phase_count = 0
for i in range(100):
    if i % 20 == 0:
        phase_count += 1
        I.changePhase(phase_count)
    time.sleep(1)
    I.move()
    I.addCar()
    #I.print()
    print(I.phase)
    i = I.getInfoArrays()
    showsim.visualizeIntersection(i[0],i[1],i[2])
    led_test.turnAllOff()
    led_test.phaseState(I.phase)

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
