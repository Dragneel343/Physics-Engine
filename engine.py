# the Engine

import cv2
import numpy as np

from random import randint
from circle import Circle
from polygon import Polygon
from rectangle import Rectangle
from point import Point
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
			(Circle, Circle) : self.circ_circ_check
		}

		# # SAMPLE SIMULATIONS:
		# self.init_test_1()



	def init_test_1(self):
		# TEST circle
		# Triangle
		pts = (Point(100,SCREEN_HEIGHT-100), \
			Point(150,SCREEN_HEIGHT-100), \
			Point(125,SCREEN_HEIGHT))
		poly = Polygon(pts,color=(255,100,150))
		# poly.velocity.dx = 2
		# poly.velocity.dy = -2
		poly.acceleration.ddy = 0
		self.objects.append(poly)

		# Rectangle
		rect = Rectangle(300, 400, 100, 80,(255,0,255))
		rect.velocity.dx = 1
		rect.velocity.dy = 7
		self.objects.append(rect)
		# Circles
		for i in range(25):
			c = Circle(randint(0,SCREEN_WIDTH),randint(0,SCREEN_HEIGHT),randint(10,20),(randint(0,255),randint(0,255),randint(0,255)))
			c.velocity.dx = randint(-3,3)
			c.velocity.dy = randint(-1,3)
			self.objects.append(c)

	def init_test_2(self):
		"""
		Checking collision between circle and polygons
		"""
		
		rect = Rectangle(SCREEN_WIDTH//2,(SCREEN_HEIGHT*3)/4, 400, 200,(255,0,255))
		self.objects.append(rect)

		c = Circle(0, 600, 25, (120,40,40))
		c.velocity.dx = 3
		c.velocity.dy = randint(-1,3)
		self.objects.append(c)


	def run_test_1(self):
		self.init_test_1()
		for i in range(800):
			self.update()
			self.draw()

	def run_test_2(self):
		self.init_test_2()
		for i in range(800):
			self.update()
			self.draw()

	def run(self):
		for i in range(800):
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
		was_checked = set()
		for obj1 in self.objects:
			for obj2 in self.objects:
				if obj1 is obj2 or (obj1, obj2) in was_checked:
					break
				else:
					self.collision_dict[ ( type(obj1), type(obj2) ) ](obj1,obj2)
					was_checked.add((obj2,obj1))
			self.obj_wall_check(obj1)

	def obj_wall_check(self, obj1):
		# Check horizontal collision
		if ( (obj1.get_left() <= 0) and (obj1.velocity.dx < 0) ) or ( (obj1.get_right() >= self.wall.width) and (obj1.velocity.dx > 0) ):
			obj1.on_wall_collision(col_type='h')
		# Check vertical collision
		if ( (obj1.get_bot() >= self.wall.height) and (obj1.velocity.dy < 0) ) or ( (obj1.get_top() <= 0) and (obj1.velocity.dy > 0)):
			obj1.on_wall_collision(col_type='v')

	def poly_poly_check(self, poly1, poly2):
		# Collision check between two polygons
		pass

	def poly_circ_check(self, poly, circ):
		"""
		Collision check between circle and polygon

		Used the following website as a guide in implementing this and related functions:
		http://www.jeffreythompson.org/collision-detection/poly-circle.php
		"""
		
		if type(poly) != Polygon: # corrects variable name to correct type
			poly, circ = circ, poly

		pv = poly.get_point_vector()
		count = 0
		for curr_i in range(len(pv)):
			next_i = curr_i + 1
			if next_i == len(pv):
				next_i = 0
			curr_p = pv[curr_i]
			next_p = pv[next_i]
			count += 1
			
			if self._line_circ_check(curr_p, next_p, circ):
				poly.on_collision()
				circ.on_collision()

	def _line_circ_check(self, p1, p2, circ):
		
		if self._point_circ_check(p1, circ) or self._point_circ_check(p2, circ):
			return True

		# dx = p1.x - p2.x
		# dy = p1.y - p2.y
		# line_len = ( dx**2 + dy**2) ** .5
	
		line_len = self._get_distance_between_points(p1, p2)

		# Calculate closest point on the line to the circle
		dot = ( ((circ.center.x - p1.x) * (p2.x - p1.x)) + ((circ.center.y - p1.y) * (p2.y - p1.y)) ) / (line_len**2)
		close_x = p1.x + (dot * (p2.x-p1.x))
		close_y = p1.y + (dot * (p2.y-p1.y))
		closest = Point(close_x, close_y)

		# Check if calculated point is on the line
		# if self._point_line_check(p1, p2, closest):
			
		# check if circle is on line
		if self._get_distance_between_points(circ.center, closest) <= circ.radius:
			
			if self._point_line_check(p1, p2, closest):
				return True
		# print("maybe true")
		# print(circ.center, p1, p2)
		# print(closest)
		# print()
		# return True
		return False
		

	def _point_circ_check(self, point, circ):
		
		dx = point.x - circ.center.x
		dy = point.y - circ.center.y
		dist = ( dx**2 + dy**2) ** .5
		return dist <= circ.radius

	def _point_line_check(self, p1, p2, check_p):
		d1 = self._get_distance_between_points(p1, check_p)
		d2 = self._get_distance_between_points(p2, check_p)
		line_len = self._get_distance_between_points(p1, p2)

		buff = .1

		return (d1 + d2 >= line_len - buff) and (d1 + d2 <= line_len + buff)

	def _get_distance_between_points(self, p1, p2):
		"""
		Helper function: returns the distance between two Point objects
		"""
		dx = p1.x - p2.x
		dy = p1.y - p2.y
		return ( (dx**2) + (dy**2) ) ** .5

	def circ_circ_check(self, circ1, circ2):
		# Collision check between two circles

		# !!!___TODO___!!! 
		# This should be the easiest to implement and could be implemented immediately
		pass



eng = Engine()
eng.run_test_1()