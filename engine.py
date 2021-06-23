# the Engine

import cv2
import numpy as np
from random import randint
from circle import Circle
from globals import *


class Engine:
	def __init__(self):
		self.objects = []

		self.window_shape = (SCREEN_HEIGHT,SCREEN_WIDTH,3)

		# SAMPLE SIMULATIONS:
		self.init_test_1()


	def init_test_1(self):
		# TEST circle
		for i in range(1000):
			c = Circle(randint(0,SCREEN_WIDTH),randint(0,SCREEN_HEIGHT),randint(5,20),(randint(0,255),randint(0,255),randint(0,255)))
			c.velocity.dx = randint(-3,3)
			c.velocity.dy = randint(-3,3)
			self.objects.append(c)

	def run(self):
		for i in range(1000):
			self.update()
			self.draw()


	def draw(self):
		frame = np.zeros(self.window_shape, dtype=np.uint8)
		for obj in self.objects:
			obj.draw(frame)
		cv2.imshow("Physics Engine", frame)
		cv2.waitKey(1)


	def update(self):
		for obj in self.objects:
			obj.advance()

eng = Engine()


eng.run()