import numpy as np
import math as m
import copy
from array import array
import matplotlib.pyplot as plot
from sklearn.linear_model import Ridge
import cma
import turtle
from turtle import *


################################################################################################################
        #             Turtle Implementation        #
        ############################################
#  Create screen and turtle variables
out_screen = Screen()
my_turtle = Turtle("turtle")
my_turtle.speed(-1)

#  Create two lists to store X and Y coordinates
x_coords = []
y_coords = []

#  Draw function
def turtle_draw(x, y):
    my_turtle.ondrag(None)
    my_turtle.setheading(my_turtle.towards(x, y))
    my_turtle.goto(x, y)
    my_turtle.ondrag(turtle_draw)

    #  Ensure 0 is always positive
    if(x == -0.0):
        x = 0.0

    #  Append the x coordinate to the end of the list
    x_coords.append(x)

    #  Ensure 0 is always positive
    if(y == -0.0):
        y = 0.0

    #  Append the y coordinate to the end of the list
    y_coords.append(y)

#  The main function
def test_turtle():
    turtle.listen()

    my_turtle.ondrag(turtle_draw)

    out_screen.mainloop()

test_turtle()
#################################################################################################################################


#################################################################################################################################
        #         Implementatio of DMP             #
        ############################################
class DMP(object):

    def __init__(self,w,x_coords,y_coords, pastor_mod = False):
####################################################
        #             Data Collection              #
        ############################################
        self.pastor_mod = pastor_mod
        #initial values
        self.x0 = 0                                              #initial position
        self.goal = 20                                              #goal position
        self.step = 0.1                                          #The amount of steps in taken in a particular time frame

####################################################
        #      Sin function Implementation         #
        ############################################
        #for x in range(len(step)):
        self.x_asix_of_sin = np.arange(self.x0,self.goal,self.step)          #position of each step in the x axis in term of time

        #amplitude of the sine curve of a variable like time, that will be the value y; it is also collecting samples at te same time
        self.y_asix_of_sin = np.sin(self.x_asix_of_sin)                               #position
        self.k = 100
        self.d = 2.0 * np.sqrt(self.k)
        self.w = w

        #converges_for_sin
        self.start = self.d / 3  # where it starts converges_for_sin to 0 but won't equal 0
        self.l = 1000.0
        self.b = 20.0 / np.pi

###########################################
        #             Turtle              #
        ###################################
        self.xT = x_coords
        self.yT = y_coords


####################################################
        #             Tan function                 #
        ############################################
        #for x in range(len(step)):
        self.x_asix_of_tan = np.arange(self.x0,self.goal,self.step)          #position of each step in the x axis in term of time

        #amplitude of the sine curve of a variable like time, that will be the value y; it is also collecting samples at te same time
        self.y_asix_of_tan = np.tan(self.x_asix_of_tan)                               #position



####################################################
        #   Black_Box for sin, turtle and tan      #
        ############################################


        #black-box implementation
        #self.BlackBox = cma.fmin(self.w, self.x0)








###################################################################
        #     Implimentation DMP Learning For Sin Functions       #
        ###########################################################

    def spring_damping_for_sin(self):

        #Think of it as the slope of the function as it goes through

            return self.k * (self.goal - self.y_asix_of_sin) - self.k * (self.goal - self.x0) * self.s + self.k

    def converges_for_sin(self):

        phases = np.exp(-self.start * (((np.linspace(0, 1, len(self.x_asix_of_sin))))))
        #print(phases)
        return phases #it displays the exponential converges_for_sin

    def duplicate_for_sin(self):

            #Vertically stack the array with y coordinates and x coordinates divided by the ammount of steps in secs
            original_matrix_1 = np.vstack((np.zeros([1, (self.goal*10)], dtype = int), (self.y_asix_of_sin / self.step)))
            original_matrix_2 = np.vstack((np.zeros([1, self.goal*10], dtype = int), original_matrix_1 / self.step))

            F = self.step * self.step * original_matrix_1 - self.d * (self.k * (original_matrix_1 ) - self.step * original_matrix_1)
            temp = np.zeros([200, (self.goal*10)], dtype = int)

            temp[:F.shape[0],:F.shape[1]] = F
            design = np.array([self._features_for_sin() for self.s in self.converges_for_sin()])
            print(design)
            lr = Ridge(alpha=1.0, fit_intercept=False)
            lr.fit(design, temp)
            self.w = lr.coef_


            #Think of it as the x-asis of the duplicate_for_sin
            return self.w

    def shape_path_for_sin(self, scale=False):

        #creating a 2d vector base on the duplicate_for_sin
        f = np.dot(self.w, self._features_for_sin())

        return f

    def reproduction_for_sin(self, o = None, shape = True, avoidance=False, verbose=0):

        #if verbose <= 1:
            #print("Trajectory with x0 = %s, g = %s, self.step=%.2f, step=%.3f" % (self.x0, self.goal, self.step, self.step))

        #puts evething that was from X to x; from array to matrix
        x = copy.copy(self.y_asix_of_sin)
        temp_matrix_of_x1 = copy.copy(x)
        temp_matrix_of_x2 = copy.copy(x)

        original_matrix_1 = [copy.copy(temp_matrix_of_x1)]
        original_matrix_2 = [copy.copy(temp_matrix_of_x2)]

        #reproducing the x-asis
        t = 0.1 * self.step
        ti = 0

        S = self.converges_for_sin()
        while t < self.step:
            t += self.step6
            ti += 1
            self.s = S[ti]

            x += self.step * temp_matrix_of_x1
            temp_matrix_of_x1 += self.step * temp_matrix_of_x2

            sd = self.spring_damping_for_sin()
            # the weighted shape base on the movement
            f = self.shape_path_for_sin() if shape else 0.
            C = self.step.obstacle_for_sin(o, x, temp_matrix_of_x1) if avoidance else 0.0

            #print(temp_matrix_of_x2)

            #Everything that you implemented in the  matrix that was temperary will initialize will be put into the none temperary matrix
            if ti % self.step > 0:
                temp_matrix_of_x1 = np.append(copy.copy(x),copy.copy(self.y_asix_of_sin))
                original_matrix_1 = np.append(copy.copy(self.y_asix_of_sin),copy.copy(temp_matrix_of_x1))
                original_matrix_2 = np.append(copy.copy(self.y_asix_of_sin),copy.copy(temp_matrix_of_x2))

            #return the matrix as array when returning
            return np.array(self.y_asix_of_sin), np.array(x), np.array(original_matrix_1)


    def obstacle_for_sin(self, o, original_matrix_1):

        if self.y_asix_of_sin.ndim == 1:
            self.y_asix_of_sin = self.y_asix_of_sin[np.newaxis, np.newaxis, :]
        if original_matrix_1.ndim == 1:
            original_matrix_1 = original_matrix_1[np.newaxis, np.newaxis, :]

        C = np.zeros_like(self.y_asix_of_sin)
        R = np.array([[np.cos(np.pi / 2.0), -np.sin(np.pi / 2.0)],
                        [np.sin(np.pi / 2.0),  np.cos(np.pi / 2.0)]])

        for i in xrange(self.y_asix_of_sin.shape[0]):
            for j in xrange(self.y_asix_of_sin.shape[1]):
                obstacle_diff = o - self.y_asix_of_sin[i, j]
                theta = (np.arccos(obstacle_diff.dot(original_matrix_1[i, j]) / (np.linalg.norm(obstacle_diff) * np.linalg.norm(original_matrix_1[i, j]) + 1e-10)))
                C[i, j] = (self.l * R.dot(original_matrix_1[i, j]) * theta * np.exp(-self.b * theta))

        return np.squeeze(C)

    def _features_for_sin(self):

        #getting the y asis base on the x asis, since the amplitude just asolates between 1 and -1
        c = self.converges_for_sin()

        #calculate the discrete difference along the y asis
        h= np.diff(c)
        h = np.hstack((h, [h[-1]]))
        phi = np.exp(-h * (self.s - c) ** 2)
        return self.s * phi / phi.sum()

#################################################################
                    #    Sin Implenentaion                      #
#################################################################


def main():
#########################################################################################
    #title of the sine curve
    plot.title('Demonstration')

    #give x axis a label, it is the time
    plot.xlabel('Time represented as t')

    #give y asix a label, it is the amplitude
    plot.ylabel('Amplitude - sin(time)')

    plot.grid(True, which='both')
#########################################################################################

    w = [None]
    dmp = DMP(w,x_coords,y_coords,True)

    dmp.x_coords = x_coords
    dmp.y_coords = y_coords

    w = dmp.duplicate_for_sin()
    dmp.w = w
    array1, array2, array3 = dmp.reproduction_for_sin(dmp)

    array1_a = np.sin(array1)
    plot.plot(dmp.x_asix_of_sin,array1)
    plot.axhline(y=0, color='green')

    array1_b = np.sin(array2)
    plot.plot(dmp.x_asix_of_sin,array2)
    plot.axhline(y=0, color='red')

    #array1_c = np.sin(array3)
    #plot.plot(dmp.time,array3)
    plot.axhline(y=0, color='purple')
    plot.show()


if __name__ == "__main__":
    main()
