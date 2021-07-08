# the Engine

import cv2
import numpy as np
import math
from random import randint
from circle import Circle
from polygon import Polygon
from rectangle import Rectangle
from point import Point
from globals import *


class Engine:
    def __init__(self):
        self.objects = []

        self.window_shape = (SCREEN_HEIGHT,SCREEN_WIDTH,3)

        self.collision_dict = {
            (Polygon, Polygon) : self.poly_poly_check,
            (Polygon, Circle) : self.poly_circ_check,
            (Circle, Polygon) : self.poly_circ_check,
            (Rectangle, Polygon) : self.poly_poly_check,
            (Polygon, Rectangle) : self.poly_poly_check,
            (Rectangle, Circle) : self.poly_circ_check,
            (Circle, Rectangle) : self.poly_circ_check,
            (Circle, Circle) : self.circ_circ_check
        }

        # SAMPLE SIMULATIONS:
        self.init_test_1()



    def init_test_1(self):
        # TEST circle
        pts = (Point(100,100),Point(140,100),Point(140,140),Point(100,140))
        poly = Polygon(pts,color=(255,100,150))
        poly.velocity.dx = 2
        poly.velocity.dy = -2
        self.objects.append(poly)

        rect = Rectangle(300, 400, 20, 20,(255,255,255))
        poly.velocity.dx = -.5
        poly.velocity.dy = 7
        self.objects.append(rect)


        for i in range(40):
            c = Circle(randint(0,SCREEN_WIDTH),randint(0,SCREEN_HEIGHT),randint(15,40),(randint(0,255),randint(0,255),randint(0,255)))
            c.velocity.dx = randint(-3,3)
            c.velocity.dy = randint(-3,3)
            self.objects.append(c)

    def run(self):
        for i in range(500):
            self.check_collisions()
            self.update()
            self.draw()
        cv2.destroyAllWindows()


    def draw(self):
        # make a new black frame
        frame = np.zeros(self.window_shape, dtype=np.uint8)

        # draw each object
        for obj in self.objects:
            obj.draw(frame)
        cv2.imshow("Physics Engine", frame)
        cv2.waitKey(1)


    def update(self):
        # Update each object one frame
        for obj in self.objects:
            obj.advance()

        self.check_collisions()

    def check_collisions(self):
        # Non-optimized collision checking - O(n^2) performance
        tested = set(())
        for obj1 in self.objects:
             for obj2 in self.objects:
                 tested.add((obj2, obj1))
                 #frozen = frozenset(pair)
                 if (obj1, obj2) in tested:
                     break
                 if obj1 == obj2:
                     break
                 self.collision_dict[(type(obj1),type(obj2))](obj1,obj2)
                 #tested.add(frozen)
        pass


    def poly_poly_check(self, poly1, poly2):
        # Collision check between two polygons
        pass

    def poly_circ_check(self, poly, circ):
        # Collision check between circle and polygon

        # corrects variable name to type associated
        if type(poly) != Polygon:
            poly, circ = circ, poly
        pass

    def circ_circ_check(self, circ1, circ2):
        
        #Checks bounding boxes around circles. 
        #Formula taken from https://gamedevelopment.tutsplus.com/tutorials/when-worlds-collide-simulating-circle-circle-collisions--gamedev-769
        if (circ1.center.x + circ1.radius + circ2.center.x > circ2.center.x
            and circ1.center.x < circ2.center.x + circ1.radius + circ2.radius
            and circ1.center.y + circ1.center.y + circ2.radius > circ2.center.y
            and circ1.center.y < circ2.center.y + circ1.radius + circ2.radius):
        
            # This formula is also the same as the article, but we came to it on our own. 
            # Collision check between two circles
            x = circ1.center.x - circ2.center.x
            y = circ1.center.y - circ2.center.y
            distance = math.sqrt((x**2 + y**2))
            
            #If circles are colliding
            if (distance <= circ1.radius + circ2.radius):
                newVelocity1x = (circ1.velocity.dx * (circ1.radius - circ2.radius) + (2 * circ2.radius * circ2.velocity.dx)) / (circ1.radius + circ2.radius)
                newVelocity2x = (circ2.velocity.dx * (circ2.radius - circ1.radius) + (2 * circ1.radius * circ1.velocity.dx)) / (circ2.radius + circ1.radius)
                newVelocity1y = (circ1.velocity.dy * (circ1.radius - circ2.radius) + (2 * circ2.radius * circ2.velocity.dy)) / (circ1.radius + circ2.radius)
                newVelocity2y = (circ2.velocity.dy * (circ2.radius - circ1.radius) + (2 * circ1.radius * circ1.velocity.dx)) / (circ2.radius + circ1.radius)

                circ1.velocity.dx = newVelocity1x 
                circ1.velocity.dy = newVelocity1y
                circ2.velocity.dx = newVelocity2x
                circ2.velocity.dy = newVelocity2y
            
                circ1.advance()
                circ2.advance()
        
        # !!!___TODO___!!! 
        # This should be the easiest to implement and could be implemented immediately
        pass



eng = Engine()
eng.run()