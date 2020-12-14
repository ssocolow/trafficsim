#be able to get py5
import sys
sys.path.append("/home/simon/programming/py5")
#import py5 functionality
from py5 import *
import time

#make the canvas
canvas = createCanvas(500,500)

#store the length of the lanes as a global variable
LANE_LEN = 10

#arrays to store the toward and away lane ids
#has arrays inside the big array to store individual lane rectangles
toward_lane_ids = []
away_lane_ids = []

#array to store the in intersection spots
iis = []

iis.append(rect(167,167,209,250,color='white'))
iis.append(rect(209,167,250,209,color='white'))

iis.append(rect(250,167,334,209,color='white'))
iis.append(rect(209,209,250,250,color='white'))

iis.append(rect(250,209,292,250,color='white'))
iis.append(rect(292,209,334,250,color='white'))

iis.append(rect(167,250,209,292,color='white'))
iis.append(rect(209,250,250,292,color='white'))

iis.append(rect(250,250,292,292,color='white'))
iis.append(rect(292,250,334,334,color='white'))

iis.append(rect(167,292,250,334,color='white'))
iis.append(rect(250,292,292,334,color='white'))


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
    toward_lane_ids[2].append(rect((500-lbs*i),250,(500-lbs*(i+1)),209,color='white'))
    toward_lane_ids[3].append(rect((500-lbs*i),209,(500-lbs*(i+1)),167,color='white'))
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

for lane in away_lane_ids:
    lane.reverse()

#show the canvas
#show()

def getColor(car):
    if car.origin == 1:
        return 'blue'
    if car.origin == 2:
        return 'red'
    if car.origin == 3:
        return 'green'
    if car.origin == 4:
        return 'yellow'
    if car.origin == 5:
        return 'orange'
    if car.origin == 6:
        return 'purple'
    if car.origin == 7:
        return 'black'

#draw the canvas
def visualizeIntersection(to,_in,away):
    #clear the visualization
    for i in range(7):
        for j in range(10):
            canvas.itemconfigure(toward_lane_ids[i][j],fill='white')
    for i in range(4):
        for j in range(10):
            canvas.itemconfigure(away_lane_ids[i][j],fill='white')
    for i in range(12):
        canvas.itemconfigure(iis[i],fill='white')
    
    #draw the color for the car
    for i in range(7):
        for j in range(10):
            if to[i][j] != 0:
                canvas.itemconfigure(toward_lane_ids[i][j],fill=getColor(to[i][j]))
    for i in range(4):
        for j in range(10):
            if away[i][j] != 0:
                canvas.itemconfigure(away_lane_ids[i][j],fill=getColor(away[i][j]))
    for i in range(12):
        if _in[i] != 0:
            canvas.itemconfigure(iis[i],fill=getColor(_in[i]))
    draw()
				
#for i in range(10):
#	time.sleep(1)
#	canvas.itemconfigure(toward_lane_ids[0][i],fill='red')
#	if i != 0:
#		canvas.itemconfigure(toward_lane_ids[0][i-1],fill='white')
#	draw()
