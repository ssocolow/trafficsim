
class Car:
    def __init__(self):
        self.wait_time = 0

    def tick(self):
        self.wait_time += 1



    # def __init__(self, pos, size):
    #     self.pos = matrix2d.Matrix.array_to_matrix(pos)
    #     self.size = size
    #     self.acceleration = matrix2d.Matrix(2,1)
    #     self.vel = matrix2d.Matrix(2,1)

    # def move(self):
    #     self.vel.add(self.acceleration)
    #     self.pos.add(self.vel)