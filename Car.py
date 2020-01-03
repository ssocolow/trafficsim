import random

class Car:
    def __init__(self):
        self.wait_time = 0

        #store origin lane picker
        p = random.randint(1,100)

        #store away lane picker
        a = random.randint(1,100)

        self.origin = 0
        self.away = 0

        #calculate the origin lane and the respective away lane from the data
        if p <= 24:
            self.origin = 1
            if a <= 20:
                self.away = 1
            else:
                self.away = 2
        else if p <= 38:
            self.origin = 2
            self.away = 4
        else if p <= 49:
            self.origin = 3
            self.away = 3
        else if p <= 69:
            self.origin = 4
            if a <= 20:
                self.away = 1
            else:
                self.away = 2
        else if p <= 72:
            self.origin = 5
            if a <= 31:
                self.away = 2
            else if a <= 56:
                self.away = 3
            else if a <= 100:
                self.away = 4
        else if p <= 93:
            self.origin = 6
            if a <= 16:
                self.away = 1
            else if a <= 100:
                self.away = 4
        else if p <= 100:
            self.origin = 7
            self.away = 3



    def tick(self):
        self.wait_time += 1