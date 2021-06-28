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
		if len(self.point_vector) < 3:
			raise ValueError("Expected tuple of length three of greater")
		

	def draw(self, frame):
		pts = np.array([list(p) for p in self.point_vector], np.int32)
		pts = pts.reshape((-1,1,2))
		frame = cv2.polylines(frame, [pts], True, self.color, self.line_width)
		return frame

	def advance(self):
		
		for p in self.point_vector:
			p += self.velocity
			
		