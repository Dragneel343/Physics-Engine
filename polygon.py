from shape import Shape
import cv2
import numpy as np


class Polygon(Shape):
	"""
	POLYGON:
	  - Params:
		- point-vector: a tuple of point objects of length 3 or greater
		- x,y: (optional) center of object used for translations and point of rotation
		- color: (optional) tuple (B,G,R)
	"""
	def __init__(self, point_vector, color=(255,255,255), line_width=5, x=0, y=0):
		super().__init__(x=x, y=y, color=color)
		self.line_width = line_width
		self.point_vector = point_vector
		if len(self.point_vector) < 3 and self.point_vector[0] != None:
			raise ValueError("Expected tuple of length three of greater")
		

	def draw(self, frame):
		pts = self.get_np_array()
		pts = pts.reshape((-1,1,2))
		frame = cv2.polylines(frame, [pts], True, self.color, self.line_width)
		return frame

	def get_np_array(self):
		return np.array([list(p) for p in self.point_vector], np.int32)

	def advance(self):
		super().advance()
		for p in self.point_vector:
			p += self.velocity

	def get_left(self):
		temp = [p.x for p in self.point_vector]
		return min(temp)
	
	def get_right(self):
		temp = [p.x for p in self.point_vector]
		return max(temp)
	
	def get_top(self):
		temp = [p.y for p in self.point_vector]
		return min(temp)
	
	def get_bot(self):
		temp = [p.y for p in self.point_vector]
		return max(temp)

	def get_point_vector(self):
		return self.point_vector
	
			
		