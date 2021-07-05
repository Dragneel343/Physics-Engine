# the Engine

import cv2
import numpy as np
from random import randint
from circle import Circle
from polygon import Polygon
from rectangle import Rectangle
from wall import Wall
from point import Point
from globals import *


class Engine:
	def __init__(self):
		self.objects = []

		self.window_shape = (SCREEN_HEIGHT,SCREEN_WIDTH,3)
		self.wall = Wall(SCREEN_WIDTH,SCREEN_HEIGHT)
		self.collision_dict = {
			(Polygon, Polygon) : self.poly_poly_check,
			(Polygon, Circle) : self.poly_circ_check,
			(Circle, Polygon) : self.poly_circ_check,
			(Rectangle, Polygon) : self.poly_poly_check,
			(Polygon, Rectangle) : self.poly_poly_check,
			(Rectangle, Circle) : self.poly_circ_check,
			(Circle, Rectangle) : self.poly_circ_check,
			(Circle, Circle) : self.circ_circ_check,
			
		}

		# SAMPLE SIMULATIONS:
		self.init_test_1()



	def init_test_1(self):
		# TEST circle
		pts = (Point(100,100),Point(150,100),Point(125,150))
		poly = Polygon(pts,color=(255,100,150))
		poly.velocity.dx = .5
		poly.velocity.dy = -2
		self.objects.append(poly)

		rect = Rectangle(300, 400, 20, 20,(255,0,255))
		rect.velocity.dx = 1
		rect.velocity.dy = 7
		self.objects.append(rect)


		for i in range(50):
			c = Circle(randint(0,SCREEN_WIDTH),randint(0,SCREEN_HEIGHT),randint(15,40),(randint(0,255),randint(0,255),randint(0,255)))
			c.velocity.dx = randint(-3,3)
			c.velocity.dy = randint(-1,3)
			self.objects.append(c)

	def run(self):
		for i in range(1200):
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
		self.check_collisions()
		for obj in self.objects:
			obj.advance()

		

	def check_collisions(self):
		# Non-optimized collision checking - O(n^2) performance
		for obj1 in self.objects:
			for obj2 in self.objects:
				if obj1 == obj2:
					break
				self.collision_dict[ ( type(obj1), type(obj2) ) ](obj1,obj2)
			self.obj_wall_check(obj1)

	def obj_wall_check(self, obj1):
		# Check horizontal collision
		if ( (obj1.get_left() <= 0) and (obj1.velocity.dx < 0) ) or ( (obj1.get_right() >= self.wall.width) and (obj1.velocity.dx > 0) ):
			obj1.on_wall_collision(col_type='h')

		# Check vertical collision
		if ( (obj1.get_bot() >= self.wall.height) and (obj1.velocity.dy < 0) ) or ( (obj1.get_top() <= 0) and (obj1.velocity.dy > 0)):
			obj1.on_wall_collision(col_type='v')

	# def rect_wall_check(self, rect):
	# 	if rect.get_left() <= 0 or rect.get_right() >= self.wall.width:
	# 		rect.velocity.dx *= -1

	# 	if rect.get_bot() >= self.wall.height or rect.get_top() <= 0:
	# 		rect.velocity.dy *= -1

	# def circ_wall_check(self, circ):
	# 	if circ.get_left() <= 0 or circ.get_right() >= self.wall.width:
	# 		circ.velocity.dx *= -1

	# 	if circ.get_bot() >= self.wall.height or circ.get_top() <= 0:
	# 		circ.velocity.dy *= -1



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