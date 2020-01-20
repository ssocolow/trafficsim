#import py5 functionality
from py5 import *

#make the canvas
canvas = createCanvas(500,500)

#store the length of the lanes as a global variable
LANE_LEN = 10

#arrays to store the toward and away lane ids
#has arrays inside the big array to store individual lane rectangles
toward_lane_ids = []
away_lane_ids = []

#make the arrays to hold the specific toward lane ids
for i in range(7):
    toward_lane_ids.append([])

for i in range(4):
    away_lane_ids.append([])
    
#lane block size is 500/3 then divided by how many spots in the lane
lbs = 167/LANE_LEN

#make the lane rectangles
for i in range(LANE_LEN):
    #make toward lanes 1 and 2
    toward_lane_ids[0].append(rect(250,(500-lbs*i),292,(500-lbs*(i+1)),color='white'))
    toward_lane_ids[1].append(rect(292,(500-lbs*i),334,(500-lbs*(i+1)),color='white'))
    #make toward lanes 3 and 4
    toward_lane_ids[2].append(rect((500-lbs*i),250,(500-lbs*(i+1)),208,color='white'))
    toward_lane_ids[3].append(rect((500-lbs*i),208,(500-lbs*(i+1)),166,color='white'))
    #make toward lane 5
    toward_lane_ids[4].append(rect(250,(lbs*i),167,(lbs*(i+1)),color='white'))
    #make toward lanes 6 and 7
    toward_lane_ids[5].append(rect((lbs*i),250,(lbs*(i+1)),292,color='white'))
    toward_lane_ids[6].append(rect((lbs*i),292,(lbs*(i+1)),334,color='white'))



    #make away lanes 3 and 4
    away_lane_ids[2].append(rect(167,(500-lbs*i),250,(500-lbs*(i+1)),color='white'))
    away_lane_ids[3].append(rect((500-lbs*i),250,(500-lbs*(i+1)),333,color='white'))

    #make away lane 1
    away_lane_ids[0].append(rect(250,(lbs*i),333,(lbs*(i+1)),color='white'))
    
    #make away lane 2
    away_lane_ids[1].append(rect((lbs*i),167,(lbs*(i+1)),250,color='white'))

#show the canvas
show()
