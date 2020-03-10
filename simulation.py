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
#get csv functionality to store the data
#store 1 row per generation with columns of avg wait, avg throughput, best wait, best throughput
import csv
#import visualization functionality
#import showsim
#import led_test
import math

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
#gets cleared every epoch
throughs = []
waits = []

#stores average throughs and waits for all the generations
avg_throughs = []
avg_waits = []

#stores the best throughput and the best wait time for all the generations
best_throughs = []
best_waits = []

#store the best neural networks
saved_best_nets = []

#have a variable to find the best neural network in the generation
best_index = 0

#MAKE THE 0s 0.01 instead of 0 to avoid the overflow error maybe

#this will run the network through the simulation and return the total wait time generated
#to get the inputs to the neural network, we need arrays for each lane with a 1 or 0 for if a car is there or not
#we also need to get the wait time for each lane and divide it by 10 to make it closer to between 0 and 1
#and we need to see if the light is red or not, and if it is put a 1, if not put a 0


#gets a neural net as input
#returns output array from neural net feedforward
def neuralNetDecide(net):
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
    input_arr.append(I.time_on_phase / 200)

    #input the wait time of all the lanes which comes from the wait time of each car squared then summed
    input_arr.extend(I.squareThenAddWaits())

    #feed the inputs through the network and get an output
    output_arr = net.feedforward(input_arr)
    return output_arr


#get the wait times and then normalize them
#returns an array with numbers between 0 and 1 for all of the toward lanes based on their wait time
def getNormalizedWaitTime():
    lane_wait_times = I.getLaneWaitTimes()
    #make it not 0 to avoid the dividing by 0 error
    sum_ = 0.1
    for num in lane_wait_times:
        sum_ += num
    normalized_wait_times = []
    for num in lane_wait_times:
        #normalized_wait_times.append(math.log(num+1)/8)
        normalized_wait_times.append(num/sum_)
    return normalized_wait_times


#run the simulation test on the network and return the fitness score
def RunSimulationTest(network):
    #clear the intersection
    I.clearIntersection()
    for i in range(200):
        #move the intersection
        I.move()
        #every 2 time steps add a car
        if i % 2 == 0:
            I.addCar()

        #this is where the neural net decides what phase to switch to
        #decides the phase only if it has spent at least 10 time steps on the current phase
        if I.time_on_phase >= 10:
            if I.time_on_phase < 60:
                output_array = neuralNetDecide(network)
                newlight = output_array.index(max(output_array)) + 1
                if newlight == I.phase:
                    pass
                else:
                    I.changePhase(newlight)
            #put a limit on how long it can do one phase
            #if it goes over the limit, switch to the next highest index in the output array
            else:
                output_array = neuralNetDecide(network)
                output_array.remove(max(output_array))
                newlight = output_array.index(max(output_array)) + 1
                I.changePhase(newlight)

    #store the throughput and Intersection wait time for each neural net
    throughs.append(I.throughput)
    waits.append(I.total_wait_time)

    #return the fitness
    lane_waits = I.getLaneWaitTimes()
    fitness = 1/sum(lane_waits)
    return fitness



#do the neuroevolution with the epoch function
#have global storing variables
POPSIZE = 100
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

    #nets is going to have arrays which store generations in the big array
    nets.append([])

    #make the mutation rate smaller as more generations have passed
    if num_of_gens < 30:
        mut_rate = 0.2
    elif num_of_gens >= 30 & num_of_gens < 60:
        mut_rate = 0.1
    else:
        mut_rate = 0.05

    #fill the first array in nets with randomly initialized neural nets
    if num_of_gens == 0:
        for i in range(POPSIZE):
            nets[0].append(nn.NeuralNetwork([[17],[16],[16],[5]], mutation_rate = mut_rate))

    for i in range(POPSIZE):
        #run the simulation test on each neural net
        scores.append(RunSimulationTest(nets[num_of_gens][i]))
        total += scores[i]


    for i in range(POPSIZE):
        #get an array of probablilites for each neural net
        probabilities.append(scores[i] / total)


    temp_probs = probabilities.copy()

    #maybe the best should get 30 spots
    #second best get 15
    #third best get 10
    #after putting in these reserved spots, remove them from the temp_probs array so we can find the second best because it will now be the best
    for i in range(30):
        indicies_array.append(temp_probs.index(max(temp_probs)))

    for i in range(len(temp_probs)):
        if temp_probs[i] == max(temp_probs):
            temp_probs[i] = 0

    for i in range(15):
        indicies_array.append(temp_probs.index(max(temp_probs)))

    for i in range(len(temp_probs)):
        if temp_probs[i] == max(temp_probs):
            temp_probs[i] = 0

    for i in range(10):
        indicies_array.append(temp_probs.index(max(temp_probs)))

    for i in range(len(temp_probs)):
        if temp_probs[i] == max(temp_probs):
            temp_probs[i] = 0

    #add to the index array an amount of indicies equal to the nerual net's probability * 100
    #more indicies in the array mean a better chance at being chosen more for the next generation
    for i in range(POPSIZE):
        for j in range(round(probabilities[i] * 100)):
            indicies_array.append(i)

    #add another array to store the next generation
    nets.append([])

    #repopulate the next generation with random choices from the indicies array
    for i in range(POPSIZE):
        nets[num_of_gens + 1].append(nets[num_of_gens][random.choice(indicies_array)].copy().mutate())

    num_of_gens += 1
    return scores



#make a function to find the average of the array
def avg(arr):
    total = 0
    for num in arr:
        total += num
    return total / len(arr)


#run through a certain amount of generations
def evolve(how_many_gens):
    for i in range(how_many_gens):
        epoch()
        #scores.append(epoch())
        best_throughs.append(max(throughs))
        best_waits.append(min(waits))

        best_net_i = throughs.index(best_throughs[i])
        saved_best_nets.append(nets[i][best_net_i].get_data())

        avg_throughs.append(avg(throughs))
        avg_waits.append(avg(waits))

        print(avg_throughs)
        print(avg_waits)
        print(i)

        waits = []
        throughs = []




#make a function to implement a first come, first serve approach which is similar to what is used in real life
#when a car is detected in the last position in the lane (closest to the intersection), a phase containing that lane is added to the queue
#the yielding phase is always used (UP FOR DEBATE)

#it can't add the same phase that it is currently on to the queue

#takes in how many time steps to run for and the probablility of a car spawning on each time step and how long the phases should be
#returns Intersection's wait time and throughput

#store the lights that are in the different phases
phases = [[],[1,2,7],[2,3,4],[5],[6,7],[3,4,6,7]]

def firstComeFirstServe(ticks, prob, time_, debug):
    #make a queue and a storage for past phases variable so that we don't queue the past phase
    queue = []
    #make a past phase storage array so that I only add to the queue if the lane isn't part of the past phase
    past_phase = []

    #clear the intersection before starting
    I.clearIntersection()

    #make the past phase equal to the lanes in the current phase which is the default after clearing the intersection
    past_phase.extend(phases[I.phase])

    #start and run the simulation for a number of time steps equal to the ticks input
    for i in range(ticks):
        if debug:
            time.sleep(0.15)
            I.print()
            print(I.phase)
            print(queue)

        #move the intersection
        I.move()

        #generate a random number between 0 and 1 and if it is less than the inputted probablility, a car is added to the intersection
        r = random.random()
        if r < prob:
            I.addCar()

        # #only add car to the intersection if the i modulus prob is equal to 0 (if prob is 2 then every 2 time steps a car is added)
        # if i % prob == 0:
        #     I.addCar()

        #loop over all the toward lanes
        for i in range(7):
            #only add to the queue if the lane is not a right only lane
            if i != 1 and i != 6:
                #only add to the queue if the last spot in the lane (closest to the intersection) is a car
                if I.toward_lanes[i].contents[I.toward_lanes[i].len - 1] != 0:
                    #only add to the queue if the lane is not part of the past phase and is not part of the queue
                    if (i + 1) not in past_phase:
                        #if the lane is lane 1 add phase 1 to the queue only if phase 1 is not in queue
                        #also only add the phase to the queue if the phase is not the intersection's next phase (when it is switching)
                        if i == 0 and 1 not in queue and 1 != I.next_phase:
                            queue.append(1)
                        #if the lane is lane 3 add phase 2 to the queue only if phase 2 is not in queue
                        #also only add the phase to the queue if the phase is not the intersection's next phase (when it is switching)
                        if i == 2 and 2 not in queue and 2 != I.next_phase:
                            queue.append(2)
                        #add phase 5 to the queue if the lane is 4 only if phase 5 is not in queue
                        #also only add the phase to the queue if the phase is not the intersection's next phase (when it is switching)
                        if i == 3 and 5 not in queue and 5 != I.next_phase:
                            queue.append(5)
                        #add phase 3 to the queue if the lane is 5 only if phase 3 is not in queue
                        #also only add the phase to the queue if the phase is not the intersection's next phase (when it is switching)
                        if i == 4 and 3 not in queue and 3 != I.next_phase:
                            queue.append(3)
                        #add phase 5 to the queue if lane is 6 only if phase 5 is not in queue
                        #also only add the phase to the queue if the phase is not the intersection's next phase (when it is switching)
                        if i == 5 and not 5 in queue and 5 != I.next_phase:
                            queue.append(5)

        #switch the phase to the first phase in the queue
        if I.time_on_phase >= time_ and len(queue) != 0:
            next_phase = queue.pop(0)
            past_phase.clear()
            I.changePhase(next_phase)
            past_phase.extend(phases[I.phase])

    w = I.total_wait_time
    t = I.throughput
    return [w, t]



#make a function to get clock timed intersection data
#takes in an array with phases to run, how long the phases are on, how many time steps to run the simulation, the probablility for a car to spawn
#and a debug option

#returns an array with total intersection wait time and throughput
def clockTimed(phases_to_run, phase_length, time_steps, prob, debug):
    I.clearIntersection()
    phasecounter = 0
    for i in range(time_steps):
        if debug:
            time.sleep(0.5)
            I.print()
            print(I.phase)

        #move the intersection
        I.move()

        #generate a random number between 0 and 1 and if it is less than the inputted probablility, a car is added to the intersection
        r = random.random()
        if r < prob:
            I.addCar()

        if I.time_on_phase >= phase_length:
            if phasecounter != len(phases_to_run) - 1:
                phasecounter += 1
            else:
                phasecounter = 0
            I.changePhase(phases_to_run[phasecounter])

    w = I.total_wait_time
    t = I.throughput

    return [w,t]



def runClockTimed(until, repeats):
    f = []
    for i in range(until):
        avgws = []
        avgthroughs = []
        for j in range(repeats):
            out = clockTimed([1,5,1,5,3],i,200,0.25,0)
            avgws.append(out[0])
            avgthroughs.append(out[1])

        f.append([i,avg(avgws),avg(avgthroughs)])
        print(i)
    return f

##########data collection##########
#f = runClockTimed(50,60)
# f = []
# for i in range(100):
#     dat = clockTimed([1,2,3,4,5],9,200,0.5,0)
#     f.append([i, dat[0], dat[1]])
###################################


def drun(x, p, t):
    out = []
    for i in range(x):
        out.append(clockTimed([1,5,1,5,3],7,200,0.5,0))
    print(out)

def srun(p,t):
    out = []
    out.append(firstComeFirstServe(200,p,t,1))
    print(out)


def runFirstComeFirstServe(until, repeats):
    f = []
    for i in range(until):
        avgws = []
        avgthroughs = []
        for j in range(repeats):
            out = firstComeFirstServe(200,i/20,10,0)
            avgws.append(out[0])
            avgthroughs.append(out[1])

        f.append([i,avg(avgws),avg(avgthroughs)])
        print(i)
    return f

#f = runFirstComeFirstServe(40,60)
#write data to csv

# with open('data010.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for i in range(len(avg_waits)):
#         writer.writerow([i,avg_waits[i],avg_throughs[i],best_waits[i],best_throughs[i]])

# #find the best of the best
# index_ = best_waits.index(min(best_waits))
# with open('bestnet010.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow([saved_best_nets[index_]])

# print("This took " + str(time.time() - ts) + " seconds")

#make a csv to store first come first serve data
#each row has how many phase ticks, throughput, then wait time
with open('firstComeFirstServe.csv','w',newline='') as file:
    writer = csv.writer(file)
    for i in range(len(f)):
        writer.writerow([f[i][0],f[i][1],f[i][2]])