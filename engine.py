# the Engine

import cv2
import numpy as np
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
		for i in range(150):
			c = Circle(randint(0,SCREEN_WIDTH),randint(0,SCREEN_HEIGHT),randint(15,40),(randint(0,255),randint(0,255),randint(0,255)))
			c.velocity.dx = randint(-3,3)
			c.velocity.dy = randint(-3,3)
			self.objects.append(c)

	def run(self):
		for i in range(500):
			self.update()
			self.draw()


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
		for obj1 in self.objects:
			for obj2 in self.objects:
				if obj1 == obj2:
					break
				self.collision_dict[(type(obj1),type(obj2))](obj1,obj2)


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
		# Collision check between two circles

		# !!!___TODO___!!! 
		# This should be the easiest to implement and could be implemented immediately
		pass



eng = Engine()
eng.run()