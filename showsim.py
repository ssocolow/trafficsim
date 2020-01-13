#import py5 functionality
from py5 import *

#make the canvas
canvas = createCanvas(500,500)

#store the length of the lanes as a global variable
LANE_LEN = 10

#array to store the toward lane ids
#has arrays inside the big array to store individual lane rectangles
toward_lane_ids = []

#make the arrays to hold the specific toward lane ids
for i in range(7):
    toward_lane_ids.append([])

#make the toward lane rectangles
for i in range(LANE_LEN):
    #make lanes 1 and 2
    toward_lane_ids[0].append(rect(250,(500-20*i),312,(500-20*(i+1)),color='white'))
    toward_lane_ids[1].append(rect(312,(500-20*i),374,(500-20*(i+1)),color='white'))
    #make lanes 3 and 4
    toward_lane_ids[2].append(rect((500-20*i),250,(500-20*(i+1)),188,color='white'))
    toward_lane_ids[3].append(rect((500-20*i),188,(500-20*(i+1)),126,color='white'))

#show the canvas
show()
