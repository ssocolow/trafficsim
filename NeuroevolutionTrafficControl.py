#import intersection functionality
from Intersection import Intersection
from Lane import Lane
from Car import Car
#import time functionality
import time
#get access to the other directory so we can import nn.py
import sys
sys.path.insert(1,'/home/simon/programming/Neural-Network-Python-Lib')
#import neural network functionality
import nn
#import random selection for neuroevolution
import random
#get csv functionality to store the data
import csv
#import visualization functionality
#import showsim
#import led_test
import math
#import genetic algorithm functionality
import ga

#how many neural nets are in each generation
POPSIZE = 500

#how many generations to run
EPOCHS = 100

#keep track of time
ts = time.time()

#make the toward lanes and the away lanes
toward = []
for i in range(7):
    toward.append(Lane(10,1))

away = []
for i in range(4):
    away.append(Lane(10,-1))

#make the intersection
I = Intersection(toward, away)

#store the networks' througputs and wait times
throughs = []
waits = []

#stores the best throughput and the best wait time for all the generations
best_throughs = []
best_waits = []

#store the best neural networks
saved_best_nets = []

#gets a neural net as input
#returns output array from neural net feedforward
def neuralNetDecide(net, time_):
    input_arr = []

    #put the normalized number of cars in each lane into the input array
    input_arr.extend(I.getCarCount())

    #if all the lights are red which means the phases are switching input a 1, else input a 0
    if I.phase == 0:
        input_arr.append(1)
    else:
        input_arr.append(0)

    #input the current phase normalized between 1 and 0
    input_arr.append(I.phase / 10)

    #input the normalized amount of time the Intersection has stayed on the current phase
    input_arr.append(I.time_on_phase / time_)

    #input the wait time of all the lanes which comes from the wait time of each car squared then summed and finally normalized
    input_arr.extend(I.squareThenAddWaits())

    #feed the inputs through the network and get an output
    output_arr = net.feedforward(input_arr)
    return output_arr


#run the simulation test on the network and return the fitness score
#takes a network, how long to run the simulation, and the probability of a car spawning as input
#assigns a score to the neural net
def RunSimulationTest(network, time_, prob):
    global waits
    global throughs

    #clear the intersection
    I.clearIntersection()

    for i in range(time_):
        #move the intersection
        I.move()
        #cars have a certain change of spawning
        r = random.random()
        if r < prob:
            I.addCar()

        #this is where the neural net decides what phase to switch to
        output_array = neuralNetDecide(network, time_)

        # #get a probability for each of the outputs
        # probs = ga.makeProbs(output_array)
        # light = ga.pickOneProbs(probs)

        #get the new phase
        newphase = output_array.index(max(output_array)) + 1

        #if the new phase is the same as the current phase, do nothing
        if newphase == I.phase:
            pass
        #otherwise, switch to the new phase
        else:
            I.changePhase(newphase)

    #store the throughput and Intersection wait time for each neural net
    throughs[num_of_gens].append(I.throughput)
    waits[num_of_gens].append(I.total_wait_time)

    #return the score
    lane_waits = I.getLaneWaitTimes()
    score = 1/sum(lane_waits)
    return score


#make a variable to hold the number of generations
num_of_gens = 0
#make an array to hold all of the nets
nets = []

#make an evolve function
def evolve():
    #use the global variables
    global num_of_gens
    global nets
    global throughs
    global waits

    #make an array inside the larger array to hold the throughput and wait times of all the nets in one generation
    throughs.append([])
    waits.append([])

    #if it is the first time, create the first nets
    if num_of_gens == 0:
        nets.append([])
        for i in range(POPSIZE):
            nets[0].append(nn.NeuralNetwork([[17],[32],[16],[5]]))

    #loop through all of the nets of the current generation
    for net in nets[num_of_gens]:
        net.score = RunSimulationTest(net, 200, 0.5)
        print(str(nets[num_of_gens].index(net)) + ' / ' + str(POPSIZE) + '          ' + 'gen ' + str(num_of_gens) + ' out of ' + str(EPOCHS))

    #get the data for the best of each generation
    best_waits.append(min(waits[num_of_gens]))
    best_throughs.append(max(throughs[num_of_gens]))

    #get ready to spawn the next generation
    nets.append([])

    #make the probabilities for the networks to be picked
    nets[num_of_gens + 1].extend(ga.nextGeneration(nets[num_of_gens]))

    #increment the number of generations
    num_of_gens += 1



#run evolve certain number of times
def runEvolve(n):
    for i in range(n):
        evolve()


runEvolve(EPOCHS)


print("This took " + str(time.time() - ts) + " seconds")

#save wait data to csv
with open('n_wait_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(waits)):
        writer.writerow(waits[i])

#save throughput data to csv
with open('n_through_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(throughs)):
        writer.writerow(throughs[i])

#save best brain to csv
with open('n_best_brain.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    b_net_gen_i = best_throughs.index(max(best_throughs))
    b_net_i = throughs[b_net_gen_i].index(max(throughs[b_net_gen_i]))
    writer.writerow(nets[b_net_gen_i][b_net_i].get_data())
