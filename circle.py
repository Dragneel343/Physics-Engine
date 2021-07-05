# Creat circle objects
# Hey Guys
from shape import Shape
import cv2

class Circle(Shape):
	def __init__(self, x=0, y=0, radius=5, color=(255,255,255)):
		super().__init__(x=x, y=y, color=color)
		self.radius = radius

	def draw(self, frame):
		
		frame = cv2.circle(frame, (self.center.x, self.center.y), self.radius, self.color, -1)
		return frame

	def on_collision(self):
		# TODO
		# Should adjust speed (magnitude of velocity) by a factor of .9 (loses some speed to simulate inelastic collision)
		pass

	

	def advance(self):
		super().advance()
		self.center += self.velocity

	def get_left(self):
		return self.center.x - self.radius

	def get_right(self):
		return self.center.x + self.radius
	
	def get_top(self):
		return self.center.y - self.radius
	
	def get_bot(self):
		return self.center.y + self.radius
	