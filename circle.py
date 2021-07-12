# Creat circle objects
# Hey Guys
from shape import Shape
from random import randint
import point
import cv2
from globals import SCREEN_HEIGHT, IDs

class Circle(Shape):
	def __init__(self, x=0, y=0, radius=5, color=(255,255,255), mass=None):
		super().__init__(x=x, y=y, color=color, mass=mass)
		self.radius = radius
		

	def draw(self, frame):
		frame = cv2.circle(frame, (self.center.x, self.center.y), self.radius, self.color, -1)
		return frame

	def on_collision(self):
		# TODO
		# Should adjust speed (magnitude of velocity) by a factor of .9 (loses some speed to simulate inelastic collision)
		super().on_collision()

	

	def advance(self):
		super().advance()
		self.center += self.velocity
		if self.center.y + self.radius >= SCREEN_HEIGHT:
			self.center.y = SCREEN_HEIGHT - self.radius

	def get_left(self):
		return self.center.x - self.radius

	def get_right(self):
		return self.center.x + self.radius
	
	def get_top(self):
		return self.center.y - self.radius
	
	def get_bot(self):
		return self.center.y + self.radius
	
	@property
	def mass(self):
		if self._mass == None:
			return self.radius * 2
		else:
			return self._mass

	@mass.setter
	def mass(self,mass):
		self._mass = mass

	