# the Engine

from usershape import UserShape
import cv2
import numpy as np
import math
import pynput
from pynput import keyboard
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
		self.userobject = UserShape(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,25)
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
		# pts = (Point(100,SCREEN_HEIGHT-100), \
		# 	Point(150,SCREEN_HEIGHT-100), \
		# 	Point(125,SCREEN_HEIGHT))
		# poly = Polygon(pts,color=(255,100,150))
		# # poly.velocity.dx = 2
		# # poly.velocity.dy = -2
		# poly.acceleration.ddy = 0
		# self.objects.append(poly)

		# # Rectangle
		# rect = Rectangle(300, 400, 100, 80,(255,0,255))
		# rect.velocity.dx = 1
		# rect.velocity.dy = 7
		# self.objects.append(rect)
		# Circles
		for i in range(50):
			c = Circle(randint(0,SCREEN_WIDTH),randint(0,SCREEN_HEIGHT),randint(10,25),(randint(0,255),randint(0,255),randint(0,255)))
			c.velocity.dx = randint(-10,10)
			c.velocity.dy = randint(-1,10)
			self.objects.append(c)


	def run_test_1(self):
		self.init_test_1()
		for i in range(200):
			self.update()
			self.draw()

	def run(self):
		for i in range(800):
			self.update()
			self.draw()


	def draw(self):
		# make a new black frame
		frame = np.zeros(self.window_shape, dtype=np.uint8)
		self.userobject.draw(frame)

		# draw each object
		for obj in self.objects:
			obj.draw(frame)
		cv2.imshow("Physics Engine", frame)
		cv2.waitKey(17)


	def update(self):
		# Updates User Movement
		with keyboard.Events() as events:
			event = events.get(.1)
			if event is not None:
				self.userobject.Movement(event)
			# else:
			# 	print('Received event {}'.format(event))

		# Update each object one frame
		self.check_collisions()
		for obj in self.objects:
			obj.advance()

		

		

	def check_collisions(self):
		# Non-optimized collision checking - O(n^2) performance
		total = 0
		optimized = 0

		was_checked = set()
		for obj1 in self.objects:
			for obj2 in self.objects:
				if obj1 is obj2:
					# optimized += 1
					break
				if obj1 in was_checked and obj2 in was_checked:
					# optimized += 1
					break
				else:
					if self.collision_dict[ ( type(obj1), type(obj2) ) ](obj1,obj2):
						was_checked.add(obj1)
						was_checked.add(obj2)
					total += 1
			self.obj_wall_check(obj1)

		was_checked = None
		# print(total)
		# print(optimized)
		# # print()
		# # print(was_checked)
		# # print()
		# input()
		

	def obj_wall_check(self, obj1):
		# Check horizontal collision
		if ( (obj1.get_left() <= 0) and (obj1.velocity.dx < 0) ) or ( (obj1.get_right() >= self.wall.width) and (obj1.velocity.dx > 0) ):
			obj1.on_wall_collision(col_type='h', wall=self.wall)
		# Check vertical collision
		if ( (obj1.get_bot() >= self.wall.height) and (obj1.velocity.dy < 0) ) or ( (obj1.get_top() <= 0) and (obj1.velocity.dy > 0)):
			obj1.on_wall_collision(col_type='v', wall=self.wall)

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
				return True
		return False

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

	def circ_circ_check(self, circ1, circ2, efficiency=.9):
		# This formula is also the same as the article, but we came to it on our own. 
		# Collision check between two circles
		x = circ1.center.x - circ2.center.x
		y = circ1.center.y - circ2.center.y
		distance = math.sqrt((x**2 + y**2))
		
		#If circles are colliding
		if (distance <= circ1.radius + circ2.radius):

			# move circles from overlapped position
			mid_x = (circ1.center.x + circ2.center.x) / 2
			mid_y = (circ1.center.y + circ2.center.y) / 2
			if distance == 0:
				distance = .001
				
			
			# Calculate new velocity
			normal_x = (circ1.center.x - circ2.center.x) / distance
			normal_y = (circ1.center.y - circ2.center.y) / distance
			
			tan_x = -normal_y
			tan_y = normal_x

			dot_tan_1 = circ1.velocity.dx * tan_x + circ1.velocity.dy * tan_y
			dot_tan_2 = circ2.velocity.dx * tan_x + circ2.velocity.dy * tan_y
			
			dot_norm_1 = circ1.velocity.dx * normal_x + circ1.velocity.dy * normal_y
			dot_norm_2 = circ2.velocity.dx * normal_x + circ2.velocity.dy * normal_y
			
			moment_1 = efficiency * (dot_norm_1 * (circ1.mass - circ2.mass) + 2 * circ2.mass * dot_norm_2) / (circ1.mass + circ2.mass)
			moment_2 = efficiency * (dot_norm_2 * (circ2.mass - circ1.mass) + 2 * circ1.mass * dot_norm_1) / (circ1.mass + circ2.mass)

			if abs(circ1.velocity.dy) < .15 and abs(circ2.velocity.dy) < .15:
				circ1.center.y = mid_y + (circ1.radius * y) / distance
				circ2.center.y = mid_y + (circ2.radius * -y) / distance
			else:
				circ1.velocity.dy = tan_y * dot_tan_1 + normal_y * moment_1
				circ2.velocity.dy = tan_y * dot_tan_2 + normal_y * moment_2
			
			if abs(circ1.velocity.dx) < .15 and abs(circ2.velocity.dx) < .15:
				circ1.center.x = mid_x + (circ1.radius * x) / distance
				circ2.center.x = mid_x + (circ2.radius * -x) / distance
			else:
				circ1.velocity.dx = tan_x * dot_tan_1 + normal_x * moment_1	
				circ2.velocity.dx = tan_x * dot_tan_2 + normal_x * moment_2
	

			# circ1.velocity.dx = tan_x * dot_tan_1 + normal_x * moment_1
			# circ1.velocity.dy = tan_y * dot_tan_1 + normal_y * moment_1
			# circ2.velocity.dx = tan_x * dot_tan_2 + normal_x * moment_2
			# circ2.velocity.dy = tan_y * dot_tan_2 + normal_y * moment_2
			
			# circ1.center += circ1.velocity
			# circ2.center += circ2.velocity
			
			circ1.center.x = mid_x + (circ1.radius * x) / distance
			circ1.center.y = mid_y + (circ1.radius * y) / distance
			circ2.center.x = mid_x + (circ2.radius * -x) / distance
			circ2.center.y = mid_y + (circ2.radius * -y) / distance
					
			return True
		return False
				


eng = Engine()
eng.run_test_1()