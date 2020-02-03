#import intersection functionality
from Intersection import Intersection
from Lane import Lane
from Car import Car
#import time functionality
import time
#get access to the other directory so we can import nn.py
import sys
sys.path.insert(1,'/home/ubuntu/environment/Neural-Network-Python-Lib')
#import neural network functionality
import nn
#import random selection for neuroevolution
import random
#import visualization functionality
#import showsim
#import led_test


#make the toward lanes and the away lanes
toward = []
for i in range(7):
    toward.append(Lane(10,1))

away = []
for i in range(4):
    away.append(Lane(10,-1))

#make the intersection
I = Intersection(toward, away)

#the nets array is now controlled by the epoch function
# #make the neural networks
# nets = []
# for i in range(100):
#     nets.append(nn.NeuralNetwork([[78],[16],[16],[5]]))

#MAKE THE 0s 0.01 instead of 0 to avoid the overflow error maybe

#this will run the network through the simulation and return the total wait time generated
#to get the inputs to the neural network, we need arrays for each lane with a 1 or 0 for if a car is there or not
#we also need to get the wait time for each lane and divide it by 10 to make it closer to between 0 and 1
#and we need to see if the light is red or not, and if it is put a 1, if not put a 0
def RunSimulationTest(network):
    I.clearIntersection()
    for i in range(200):
        #time.sleep(1)
        I.move()
        if i % 2 == 0:
            I.addCar()

        input_arr = I.get10InfoArrays()
        input_arr.extend(I.getLaneWaitTimes())
        if I.phase != 0:
            input_arr.append(0)
        else:
            input_arr.append(1)

        output_arr = network.feedforward(input_arr)
        newlight = output_arr.index(max(output_arr))

        if newlight == I.phase:
            pass
        else:
            I.changePhase(newlight)
    return I.total_wait_time





#debugging
#for i in range(100):
#    I.addCar()

I.phase = 1
time_count = 0
phase_count = 1
saved_wait = []
saved_through = []
for j in range(100):
    for i in range(200):
        time_count += 1
        if i == 0:
            I.changePhase(1)
        if time_count % 20 == 0:
            if phase_count != 5:
                phase_count += 1
                I.changePhase(phase_count)
            else:
                phase_count = 1
                I.changePhase(phase_count)
        #time.sleep(1)
        I.move()
        if i % 2 == 0:
            I.addCar()
        #print(I.phase)
    saved_wait.append(I.total_wait_time)
    saved_through.append(I.throughput)
    I.clearIntersection()
    #showsim.visualizeIntersection(i[0],i[1],i[2])
    #led_test.turnAllOff()
    #led_test.phaseState(I.phase)

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


#have global storing variables
POPSIZE = 200
nets = []
num_of_gens = 0

def epoch():
    #use the global variables
    global nets
    global num_of_gens

    #array to store scores
    scores = []

    #sum of all the scores
    total = 0

    #an array to store an amount of index numbers for each neural net according to their probability
    indicies_array = []

    #array with probablilites of each network based on its score / total score
    probabilities = []

    #nets is going to have arrays which have generations in the big array
    nets.append([])

    #fill the first array in nets with randomly initialized neural nets
    if num_of_gens == 0:
        for i in range(POPSIZE):
            nets[0].append(nn.NeuralNetwork([[78],[16],[16],[5]], mutation_rate = 0.15))

    for i in range(POPSIZE):
        #get the score of each network by finding absolute value of the difference between the network's output and the target
        #this will give us a smaller number for a better score, so to have a higher number for a higher score, we can do 1 divided by the score so lower score becomes higher score
        scores.append(1 / RunSimulationTest(nets[num_of_gens][i]))
        total += scores[i]

    for i in range(POPSIZE):
        #get an array of probablilites for each neural net
        probabilities.append(scores[i] / total)

    for i in range(POPSIZE):
        for j in range(round(probabilities[i] * 100)):
            indicies_array.append(i)

    #add another array to store the next generation
    nets.append([])

    for i in range(POPSIZE):
        nets[num_of_gens + 1].append(nets[num_of_gens][random.choice(indicies_array)].copy().mutate())

    num_of_gens += 1
    return scores


#scores = epoch()