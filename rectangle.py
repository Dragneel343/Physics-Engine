# Creates rectangle shapes.
from shape import Shape
from polygon import Polygon
from point import Point
import cv2
import numpy as np

class Rectangle(Polygon): # inherit Polygon?
	"""
	RECTANGLE:
	   - Params:
	     - 
	"""
	def __init__(self, x, y, height, width, color=(100,200,100), line_width=5):
		self.height = height
		self.width = width
		super().__init__((None, None, None, None), color, line_width, x, y)

		p1 = Point((height//2), (height//2))
		p2 = Point(-(height//2), (height//2))
		p3 = Point(-(height//2), -(height//2))
		p4 = Point((height//2), -(height//2))
		self._point_offsets = (p1,p2,p3,p4)
		pv = [] 
		for p in self._point_offsets:
			pv.append(p + self.center)

	def get_np_array(self):
		return np.array([list(self.center + p) for p in self._point_offsets], np.int32)


	def advance(self):
		super(Polygon, self).advance()
		self.center += self.velocity

		